/* extend.c: grids whose rows and columns are SEQUENCES of sentences.
 *
 * A line (row or column) is valid if it can be cut into consecutive pieces
 * that are all in the sentence set. The cuts of different lines are
 * independent. Some cells may be fixed in advance (the seed), which is how a
 * grid is extended: fix the old grid in the top-left corner and fill the rest.
 *
 * Usage:
 *   extend SENTS SEED n_rows n_cols max_repeats max_solutions max_nodes
 *          seed restart_nodes
 *
 *   SENTS  one sentence per line, as word ids separated by spaces
 *          (2 to MAX_LEN words). Used for rows and columns alike.
 *   SEED   n_rows * n_cols integers in row-major order; -1 = free cell.
 *   max_repeats    how many cells may hold a word already used elsewhere
 *   max_solutions  stop after this many grids (0 = no limit)
 *   max_nodes      stop after this many search nodes (0 = no limit)
 *   seed           0: fixed candidate order, plain depth-first search.
 *                  otherwise: random candidate order, and the search starts
 *                  over after every solution and after restart_nodes nodes
 *                  without one.
 *
 * Output: one grid per line on stdout (word ids, row-major). A summary goes
 * to stderr.
 *
 * Method: cells are filled in row-major order. For every line we keep the set
 * of trie nodes reachable by reading the line so far under any valid cutting
 * (at most MAX_LEN nodes: one per possible start of the current sentence),
 * plus a flag that says whether the line so far can end exactly here.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LEN 7     /* longest sentence */
#define MIN_LEN 2     /* shortest sentence */
#define MAX_SIDE 64

typedef struct {
    int word;
    int first_child, n_children;
    unsigned char terminal;
    unsigned char depth_mask; /* bit d: a sentence ends d words below this node */
} Node;

typedef struct {
    int n;
    int nodes[MAX_LEN];
    int can_break;            /* the line read so far is a valid sequence */
} State;

static Node *nodes;
static int n_nodes;
static int **sents, *sent_len, n_sents, n_words;

static int n_rows, n_cols, max_repeats;
static long max_solutions, max_nodes, restart_nodes;
static long n_solutions, total_nodes, nodes_since_restart, n_restarts;
static int random_mode, stop_all, restart_now;

static int *seed_cell, *grid, *use_count, repeats_used;
static State row_state[MAX_SIDE][MAX_SIDE + 1], col_state[MAX_SIDE][MAX_SIDE + 1];
static int *stamp, stamp_now;
static int **cand_buf;

static int cmp_sent(const void *a, const void *b) {
    int i = *(const int *)a, j = *(const int *)b;
    int n = sent_len[i] < sent_len[j] ? sent_len[i] : sent_len[j];
    for (int k = 0; k < n; k++)
        if (sents[i][k] != sents[j][k]) return sents[i][k] - sents[j][k];
    return sent_len[i] - sent_len[j];
}

/* Build the trie node for the sentences order[lo..hi) that share their first
 * `depth` words. Children are stored contiguously and sorted by word. */
static void build(int node, int *order, int lo, int hi, int depth) {
    while (lo < hi && sent_len[order[lo]] == depth) { nodes[node].terminal = 1; lo++; }
    int count = 0;
    for (int i = lo; i < hi; i++)
        if (i == lo || sents[order[i]][depth] != sents[order[i - 1]][depth]) count++;
    nodes[node].first_child = n_nodes;
    nodes[node].n_children = count;
    int first = n_nodes;
    n_nodes += count;
    int c = 0;
    for (int i = lo; i < hi;) {
        int j = i;
        while (j < hi && sents[order[j]][depth] == sents[order[i]][depth]) j++;
        nodes[first + c].word = sents[order[i]][depth];
        nodes[first + c].terminal = 0;
        build(first + c, order, i, j, depth + 1);
        c++;
        i = j;
    }
    unsigned char mask = nodes[node].terminal ? 1 : 0;
    for (int k = 0; k < count; k++) mask |= (unsigned char)(nodes[first + k].depth_mask << 1);
    nodes[node].depth_mask = mask;
}

static int child(int node, int word) {
    int lo = nodes[node].first_child, hi = lo + nodes[node].n_children;
    while (lo < hi) {
        int mid = (lo + hi) / 2;
        if (nodes[mid].word < word) lo = mid + 1; else hi = mid;
    }
    return (lo < nodes[node].first_child + nodes[node].n_children && nodes[lo].word == word) ? lo : -1;
}

/* Can a line with `remaining` free cells still be completed from `node`?
 * The current sentence must end d cells from here, and the rest must be 0
 * cells or at least MIN_LEN cells. */
static int node_feasible(int node, int remaining) {
    unsigned char mask = nodes[node].depth_mask;
    for (int d = 0; d <= MAX_LEN && d <= remaining; d++)
        if ((mask >> d & 1) && (remaining - d == 0 || remaining - d >= MIN_LEN)) return 1;
    return 0;
}

/* Advance a line state by one word. Returns 0 if the line cannot be
 * completed any more. Nodes that cannot be completed are dropped. */
static int advance(const State *prev, int word, int remaining, State *next) {
    next->n = 0;
    next->can_break = 0;
    for (int i = 0; i <= prev->n; i++) {
        int from;
        if (i < prev->n) from = prev->nodes[i];
        else if (prev->can_break) from = 0;   /* start a new sentence */
        else break;
        int to = child(from, word);
        if (to < 0 || !node_feasible(to, remaining)) continue;
        next->nodes[next->n++] = to;
        if (nodes[to].terminal && (remaining == 0 || remaining >= MIN_LEN)) next->can_break = 1;
    }
    return remaining == 0 ? next->can_break : next->n > 0;
}

static long state_fanout(const State *s) {
    long total = s->can_break ? nodes[0].n_children : 0;
    for (int i = 0; i < s->n; i++) total += nodes[s->nodes[i]].n_children;
    return total;
}

/* Words that can follow state s, without duplicates, into out. */
static int successors(const State *s, int *out) {
    int n = 0;
    stamp_now++;
    for (int i = 0; i <= s->n; i++) {
        int from;
        if (i < s->n) from = s->nodes[i];
        else if (s->can_break) from = 0;
        else break;
        int lo = nodes[from].first_child, hi = lo + nodes[from].n_children;
        for (int k = lo; k < hi; k++) {
            int w = nodes[k].word;
            if (stamp[w] != stamp_now) { stamp[w] = stamp_now; out[n++] = w; }
        }
    }
    return n;
}

static void emit(void) {
    for (int i = 0; i < n_rows * n_cols; i++) printf("%d%c", grid[i], i + 1 < n_rows * n_cols ? ' ' : '\n');
    fflush(stdout);
    n_solutions++;
    if (max_solutions && n_solutions >= max_solutions) stop_all = 1;
    if (random_mode) restart_now = 1;
}

static void search(int cell) {
    if (cell == n_rows * n_cols) { emit(); return; }
    total_nodes++;
    nodes_since_restart++;
    if (max_nodes && total_nodes >= max_nodes) { stop_all = 1; return; }
    if (random_mode && restart_nodes && nodes_since_restart >= restart_nodes) { restart_now = 1; return; }

    int r = cell / n_cols, c = cell % n_cols;
    const State *rs = &row_state[r][c], *cs = &col_state[c][r];
    int *cand = cand_buf[cell], n_cand;
    if (seed_cell[cell] >= 0) {
        cand[0] = seed_cell[cell];
        n_cand = 1;
    } else {
        n_cand = successors(state_fanout(rs) <= state_fanout(cs) ? rs : cs, cand);
        if (random_mode)
            for (int i = n_cand - 1; i > 0; i--) {
                int j = rand() % (i + 1), t = cand[i];
                cand[i] = cand[j]; cand[j] = t;
            }
    }
    for (int i = 0; i < n_cand; i++) {
        int w = cand[i];
        int repeat = use_count[w] > 0;
        if (repeat && repeats_used >= max_repeats) continue;
        if (!advance(rs, w, n_cols - 1 - c, &row_state[r][c + 1])) continue;
        if (!advance(cs, w, n_rows - 1 - r, &col_state[c][r + 1])) continue;
        grid[cell] = w;
        use_count[w]++;
        repeats_used += repeat;
        search(cell + 1);
        use_count[w]--;
        repeats_used -= repeat;
        if (stop_all || restart_now) return;
    }
}

int main(int argc, char **argv) {
    if (argc != 10) {
        fprintf(stderr, "usage: extend SENTS SEED n_rows n_cols max_repeats max_solutions max_nodes seed restart_nodes\n");
        return 2;
    }
    n_rows = atoi(argv[3]); n_cols = atoi(argv[4]); max_repeats = atoi(argv[5]);
    max_solutions = atol(argv[6]); max_nodes = atol(argv[7]);
    int seed = atoi(argv[8]);
    restart_nodes = atol(argv[9]);
    random_mode = seed != 0;
    srand(seed);
    if (n_rows > MAX_SIDE || n_cols > MAX_SIDE) { fprintf(stderr, "grid too large\n"); return 2; }

    FILE *f = fopen(argv[1], "r");
    if (!f) { perror(argv[1]); return 1; }
    int cap = 1 << 16, buf[64], n = 0, x;
    long total_words = 0;
    sents = malloc(cap * sizeof *sents);
    sent_len = malloc(cap * sizeof *sent_len);
    char line[1024];
    while (fgets(line, sizeof line, f)) {
        n = 0;
        for (char *p = strtok(line, " \n"); p; p = strtok(NULL, " \n")) {
            if (n >= 64) { fprintf(stderr, "sentence too long\n"); return 1; }
            x = atoi(p);
            buf[n++] = x;
            if (x + 1 > n_words) n_words = x + 1;
        }
        if (n < MIN_LEN || n > MAX_LEN) { fprintf(stderr, "bad sentence length %d\n", n); return 1; }
        if (n_sents == cap) {
            cap *= 2;
            sents = realloc(sents, cap * sizeof *sents);
            sent_len = realloc(sent_len, cap * sizeof *sent_len);
        }
        sents[n_sents] = malloc(n * sizeof(int));
        memcpy(sents[n_sents], buf, n * sizeof(int));
        sent_len[n_sents++] = n;
        total_words += n;
    }
    fclose(f);

    int *order = malloc(n_sents * sizeof *order);
    for (int i = 0; i < n_sents; i++) order[i] = i;
    qsort(order, n_sents, sizeof *order, cmp_sent);
    nodes = calloc(total_words + 1, sizeof *nodes);
    n_nodes = 1;
    nodes[0].word = -1;
    build(0, order, 0, n_sents, 0);

    int n_cells = n_rows * n_cols;
    seed_cell = malloc(n_cells * sizeof(int));
    grid = malloc(n_cells * sizeof(int));
    f = fopen(argv[2], "r");
    if (!f) { perror(argv[2]); return 1; }
    for (int i = 0; i < n_cells; i++) {
        if (fscanf(f, "%d", &seed_cell[i]) != 1) { fprintf(stderr, "seed file too short\n"); return 1; }
        if (seed_cell[i] >= n_words) { fprintf(stderr, "seed word not in any sentence\n"); return 1; }
    }
    fclose(f);

    use_count = calloc(n_words, sizeof(int));
    stamp = calloc(n_words, sizeof(int));
    cand_buf = malloc(n_cells * sizeof *cand_buf);
    for (int i = 0; i < n_cells; i++) cand_buf[i] = malloc((seed_cell[i] >= 0 ? 1 : n_words) * sizeof(int));
    for (int r = 0; r < n_rows; r++) { row_state[r][0].n = 0; row_state[r][0].can_break = 1; }
    for (int c = 0; c < n_cols; c++) { col_state[c][0].n = 0; col_state[c][0].can_break = 1; }

    do {
        restart_now = 0;
        nodes_since_restart = 0;
        search(0);
        if (restart_now) n_restarts++;
    } while (restart_now && !stop_all);

    fprintf(stderr, "solutions %ld nodes %ld restarts %ld (%s)\n", n_solutions, total_nodes,
            n_restarts, stop_all ? "stopped at limit" : "exhaustive");
    return 0;
}
