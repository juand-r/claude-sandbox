/* Exact search for word grids, filling the most constrained line first.
 *
 * Same problem as solver.c: every row must be one of the ROWS sentences and
 * every column one of the COLS sentences. solver.c fills cells in row-major
 * order. This program works like a crossword filler: at each step it counts,
 * for every unfinished line (row or column), the sentences that agree with the
 * cells already filled, picks the line with the fewest, and tries each of its
 * candidates. If any line has no candidate the branch is abandoned.
 *
 * Usage: fill ROWS COLS COSTS n_rows n_cols max_repeats max_cost
 *             max_solutions max_nodes seed part n_parts
 *   ROWS: one sentence per line as n_cols space-separated word ids
 *   COLS: one sentence per line as n_rows space-separated word ids
 *   COSTS: one integer per word id; the sum over all cells must be <= max_cost
 *   max_repeats: number of cells allowed to hold a word already in the grid
 *   max_solutions, max_nodes: stop limits (0 = no limit)
 *   seed: 0 = candidates in input order; otherwise shuffled
 *   part, n_parts: only try first-row candidates whose index is congruent to
 *     part modulo n_parts (to split the search over processes)
 * Output: one grid per line, n_rows*n_cols word ids in row-major order.
 * The first line filled is always row 0.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXN 8

typedef struct {
    int n, len;       /* number of sentences, words per sentence */
    int *sent;        /* sent[id * len + pos] */
    int *off[MAXN];   /* posting lists: ids with word w at position pos are */
    int *ids[MAXN];   /*   ids[pos][off[pos][w] .. off[pos][w + 1]) */
} Set;

static int n_words; /* number of distinct word ids = max id + 1 */

static void load(Set *s, const char *path, int len) {
    FILE *f = fopen(path, "r");
    if (!f) { perror(path); exit(1); }
    int cap = 1 << 20;
    s->len = len; s->n = 0; s->sent = malloc(sizeof(int) * cap * len);
    for (;;) {
        if (s->n == cap) { cap *= 2; s->sent = realloc(s->sent, sizeof(int) * cap * len); }
        int ok = 1;
        for (int i = 0; i < len; i++) if (fscanf(f, "%d", &s->sent[s->n * len + i]) != 1) ok = 0;
        if (!ok) break;
        for (int i = 0; i < len; i++) if (s->sent[s->n * len + i] >= n_words) n_words = s->sent[s->n * len + i] + 1;
        s->n++;
    }
    fclose(f);
}

static void index_set(Set *s) {
    for (int pos = 0; pos < s->len; pos++) {
        int *off = calloc(n_words + 2, sizeof(int));
        for (int i = 0; i < s->n; i++) off[s->sent[i * s->len + pos] + 2]++;
        for (int w = 0; w < n_words; w++) off[w + 2] += off[w + 1];
        int *ids = malloc(sizeof(int) * (s->n + 1));
        for (int i = 0; i < s->n; i++) ids[off[s->sent[i * s->len + pos] + 1]++] = i;
        s->off[pos] = off; s->ids[pos] = ids; /* now off[w]..off[w+1] */
    }
}

static Set R, C;
static int n_rows, n_cols, n_slots, max_repeats, max_cost, part, n_parts;
static long max_solutions, max_nodes, n_solutions, n_nodes, nodes_at_depth[2 * MAXN + 1];
static int grid[MAXN][MAXN];      /* word id or -1 */
static int slot_done[2 * MAXN];   /* slots 0..n_rows-1 are rows, then columns */
static int *used, *cost, repeats, total_cost;
static int *buf[2 * MAXN + 1];    /* candidate ids per depth */
static unsigned long long rng;
static int shuffle;

static unsigned next_rand(void) {
    rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
    return (unsigned)(rng >> 16);
}

static int stop(void) {
    return (max_solutions && n_solutions >= max_solutions) || (max_nodes && n_nodes >= max_nodes);
}

static Set *slot_set(int s) { return s < n_rows ? &R : &C; }
static int *slot_cell(int s, int pos) { return s < n_rows ? &grid[s][pos] : &grid[pos][s - n_rows]; }

/* Sentences of slot s that agree with its filled cells. Stores up to `limit`
 * of them in out (if out != NULL) and returns how many were found, stopping
 * once more than `limit` are seen. A slot with no filled cell matches all. */
static int matches(int s, int limit, int *out) {
    Set *set = slot_set(s);
    int len = set->len, best_pos = -1, best_len = 0, word[MAXN];
    for (int pos = 0; pos < len; pos++) {
        word[pos] = *slot_cell(s, pos);
        if (word[pos] < 0) continue;
        int l = set->off[pos][word[pos] + 1] - set->off[pos][word[pos]];
        if (best_pos < 0 || l < best_len) { best_pos = pos; best_len = l; }
    }
    int count = 0;
    if (best_pos < 0) {
        if (out) for (int i = 0; i < set->n && i < limit; i++) out[i] = i;
        return set->n;
    }
    const int *list = set->ids[best_pos] + set->off[best_pos][word[best_pos]];
    for (int i = 0; i < best_len; i++) {
        const int *sent = set->sent + (size_t)list[i] * len;
        int ok = 1;
        for (int pos = 0; pos < len; pos++)
            if (word[pos] >= 0 && sent[pos] != word[pos]) { ok = 0; break; }
        if (!ok) continue;
        if (count < limit && out) out[count] = list[i];
        if (++count > limit) break;
    }
    return count;
}

static void fill(int depth) {
    n_nodes++; nodes_at_depth[depth]++;
    int best = -1, best_count = 0;
    if (depth == 0) { best = 0; best_count = R.n; }
    else for (int s = 0; s < n_slots; s++) {
        if (slot_done[s]) continue;
        int count = matches(s, best < 0 ? R.n + C.n : best_count, NULL);
        if (count == 0) return;
        if (best < 0 || count < best_count) { best = s; best_count = count; }
    }
    if (best < 0) {
        for (int r = 0; r < n_rows; r++)
            for (int c = 0; c < n_cols; c++)
                printf("%d%c", grid[r][c], r + 1 == n_rows && c + 1 == n_cols ? '\n' : ' ');
        n_solutions++;
        return;
    }
    int *cand = buf[depth];
    matches(best, best_count, cand);
    if (shuffle)
        for (int i = best_count - 1; i > 0; i--) {
            int j = next_rand() % (i + 1), t = cand[i]; cand[i] = cand[j]; cand[j] = t;
        }
    Set *set = slot_set(best);
    slot_done[best] = 1;
    for (int i = 0; i < best_count && !stop(); i++) {
        if (depth == 0 && i % n_parts != part) continue;
        const int *sent = set->sent + (size_t)cand[i] * set->len;
        int placed[MAXN], n_placed = 0, ok = 1;
        for (int pos = 0; pos < set->len && ok; pos++) {
            int *cell = slot_cell(best, pos);
            if (*cell >= 0) continue;
            int w = sent[pos], rep = used[w] > 0;
            if (repeats + rep > max_repeats || total_cost + cost[w] > max_cost) { ok = 0; break; }
            *cell = w; used[w]++; repeats += rep; total_cost += cost[w];
            placed[n_placed++] = pos;
        }
        if (ok) fill(depth + 1);
        for (int k = n_placed - 1; k >= 0; k--) {
            int *cell = slot_cell(best, placed[k]);
            int w = *cell;
            used[w]--; repeats -= used[w] > 0; total_cost -= cost[w];
            *cell = -1;
        }
    }
    slot_done[best] = 0;
}

int main(int argc, char **argv) {
    if (argc != 13) {
        fprintf(stderr, "usage: fill ROWS COLS COSTS n_rows n_cols max_repeats max_cost "
                        "max_solutions max_nodes seed part n_parts\n");
        return 1;
    }
    n_rows = atoi(argv[4]); n_cols = atoi(argv[5]); n_slots = n_rows + n_cols;
    max_repeats = atoi(argv[6]); max_cost = atoi(argv[7]);
    max_solutions = atol(argv[8]); max_nodes = atol(argv[9]);
    long seed = atol(argv[10]);
    part = atoi(argv[11]); n_parts = atoi(argv[12]);
    shuffle = seed != 0; rng = 0x9E3779B97F4A7C15ULL ^ (unsigned long long)seed;
    load(&R, argv[1], n_cols);
    load(&C, argv[2], n_rows);
    index_set(&R); index_set(&C);
    used = calloc(n_words, sizeof(int));
    cost = calloc(n_words, sizeof(int));
    FILE *f = fopen(argv[3], "r");
    if (!f) { perror(argv[3]); return 1; }
    for (int i = 0; i < n_words; i++)
        if (fscanf(f, "%d", &cost[i]) != 1) { fprintf(stderr, "cost file too short\n"); return 1; }
    fclose(f);
    int max_n = R.n > C.n ? R.n : C.n;
    for (int i = 0; i <= n_slots; i++) buf[i] = malloc(sizeof(int) * (max_n + 1));
    memset(grid, -1, sizeof grid);
    fill(0);
    fprintf(stderr, "nodes per depth:");
    for (int i = 0; i <= n_slots; i++) fprintf(stderr, " %ld", nodes_at_depth[i]);
    fprintf(stderr, "\nsolutions %ld nodes %ld%s\n", n_solutions, n_nodes,
            stop() ? " (stopped at limit)" : " (exhaustive)");
    return 0;
}
