/* Exact search for word grids whose rows and columns are all listed sentences.
 *
 * Usage: solver ROWS COLS COSTS n_rows n_cols max_repeats max_cost
 *               max_solutions max_nodes seed temp restart_nodes part n_parts [block]
 *   ROWS: file with one sentence per line as n_cols space-separated word ids
 *   COLS: file with one sentence per line as n_rows space-separated word ids
 *   COSTS: file with one integer cost per word id (line i = cost of word i)
 *   max_repeats: number of cells allowed to hold a word already in the grid
 *   max_cost: upper bound on the sum of word costs over all cells
 *   max_solutions, max_nodes: stop limits (0 = no limit)
 *   seed: 0 = try candidates in id order; otherwise use a random order (below)
 *   temp: with seed != 0. temp < 0: uniform shuffle at each cell. temp >= 0:
 *     order candidates by log(#row sentences below the candidate's row node)
 *     + log(#column sentences below its column node) + temp * Gumbel noise,
 *     largest first. This prefers words that leave many completions open.
 *   restart_nodes: with seed != 0 and restart_nodes > 0, abandon the current
 *     search after this many nodes and start again from the empty grid with
 *     fresh randomness. Grids may then be output more than once.
 *   part, n_parts: only search the grids whose first two words (row 0) hash
 *     to part modulo n_parts (to split the search over processes)
 *   block (optional, default 0): cell order. 0 = row by row. 1 = grow a
 *     top-left square block (2x2, then 3x3, ...), which applies row and
 *     column constraints evenly and fails earlier.
 * Output: one grid per line, n_rows*n_cols word ids in row-major order.
 *
 * Rows and columns are stored as tries. Cells are filled in a fixed order (row
 * by row, or growing a top-left block); the candidates for a cell are the
 * words that are children of both its row's trie node and its column's.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define MAXN 8

typedef struct { int *word; int *child; int *start; int *count; int *size; int *mincost; int n_nodes; int n_edges; } Trie;

static int g_len;
static int cmp_sent(const void *a, const void *b) {
    const int *x = a, *y = b;
    for (int i = 0; i < g_len; i++) if (x[i] != y[i]) return x[i] < y[i] ? -1 : 1;
    return 0;
}

/* Build node for sentences [lo,hi) which share their first `depth` words. */
static int build(Trie *t, int *s, int len, int lo, int hi, int depth) {
    int node = t->n_nodes++;
    t->size[node] = hi - lo; /* number of sentences below this node */
    if (depth == len) { t->start[node] = 0; t->count[node] = 0; return node; }
    int n_children = 0;
    for (int i = lo; i < hi; i++)
        if (i == lo || s[i * len + depth] != s[(i - 1) * len + depth]) n_children++;
    int first = t->n_edges;
    t->n_edges += n_children;
    t->start[node] = first; t->count[node] = n_children;
    int k = 0, i = lo;
    while (i < hi) {
        int j = i;
        while (j < hi && s[j * len + depth] == s[i * len + depth]) j++;
        t->word[first + k] = s[i * len + depth];
        t->child[first + k] = build(t, s, len, i, j, depth + 1);
        k++; i = j;
    }
    return node;
}

static Trie load(const char *path, int len, int *max_word) {
    FILE *f = fopen(path, "r");
    if (!f) { perror(path); exit(1); }
    int cap = 1 << 20, n = 0, *s = malloc(sizeof(int) * cap * len);
    for (;;) {
        if (n == cap) { cap *= 2; s = realloc(s, sizeof(int) * cap * len); }
        int ok = 1;
        for (int i = 0; i < len; i++) if (fscanf(f, "%d", &s[n * len + i]) != 1) ok = 0;
        if (!ok) break;
        for (int i = 0; i < len; i++) if (s[n * len + i] > *max_word) *max_word = s[n * len + i];
        n++;
    }
    fclose(f);
    g_len = len;
    qsort(s, n, sizeof(int) * len, cmp_sent);
    Trie t;
    size_t m = (size_t)n * len + 2;
    t.word = malloc(sizeof(int) * m); t.child = malloc(sizeof(int) * m);
    t.start = malloc(sizeof(int) * m); t.count = malloc(sizeof(int) * m); t.size = malloc(sizeof(int) * m);
    t.n_nodes = 0; t.n_edges = 0;
    build(&t, s, len, 0, n, 0);
    free(s);
    return t;
}

static Trie R, C;
static int n_rows, n_cols, max_repeats;
static long max_solutions, max_nodes, n_solutions, n_nodes;
static long nodes_at_row[MAXN]; /* search nodes per row, for diagnostics */
static int grid[MAXN * MAXN], col_node[MAXN], *used, repeats;
static int *cost, max_cost, total_cost, part, n_parts;
static int *scratch[MAXN * MAXN]; /* candidate buffer for each cell */
static unsigned long long rng;
static int shuffle;
static double temp;
static long restart_nodes, restart_at; /* restart when n_nodes reaches restart_at */
typedef struct { double key; int v[3]; } Cand;
static Cand *cands[MAXN * MAXN];
static int cmp_cand(const void *a, const void *b) { /* descending key */
    double x = ((const Cand *)a)->key, y = ((const Cand *)b)->key;
    return x > y ? -1 : x < y;
}

static unsigned next_rand(void) {
    rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
    return (unsigned)(rng >> 16);
}

/* mincost[node] = smallest total word cost of any completion below the node.
 * The columns partition the unfilled cells, so the sum of mincost over the
 * current column nodes is a lower bound on the cost still to come. */
static int col_bound;
static int fill_mincost(Trie *t, int node) {
    int best = 0;
    for (int e = t->start[node]; e < t->start[node] + t->count[node]; e++) {
        int v = cost[t->word[e]] + fill_mincost(t, t->child[e]);
        if (e == t->start[node] || v < best) best = v;
    }
    return t->mincost[node] = best;
}

static int stop(void) {
    return (max_solutions && n_solutions >= max_solutions) || (max_nodes && n_nodes >= max_nodes)
        || (restart_nodes && n_nodes >= restart_at);
}

static int finished(void) {
    return (max_solutions && n_solutions >= max_solutions) || (max_nodes && n_nodes >= max_nodes);
}

/* Cell order. seq_r[i], seq_c[i] is the i-th cell to fill. Any order works in
 * which each cell comes after the cells to its left and above it. */
static int seq_r[MAXN * MAXN], seq_c[MAXN * MAXN], row_node[MAXN];

static void make_order(int block) {
    int n = 0;
    if (!block) {
        for (int r = 0; r < n_rows; r++) for (int c = 0; c < n_cols; c++) { seq_r[n] = r; seq_c[n++] = c; }
        return;
    }
    /* Grow a top-left block: after the k x k block, add column k (top to
       bottom), then row k (left to right, including the corner). Once one
       dimension is exhausted, the remaining columns or rows follow. */
    int big = n_rows > n_cols ? n_rows : n_cols;
    for (int k = 0; k < big; k++) {
        if (k < n_cols) for (int r = 0; r < k && r < n_rows; r++) { seq_r[n] = r; seq_c[n++] = k; }
        if (k < n_rows) for (int c = 0; c <= k && c < n_cols; c++) { seq_r[n] = k; seq_c[n++] = c; }
    }
}

static void fill(int idx) {
    if (idx == n_rows * n_cols) {
        for (int i = 0; i < n_rows * n_cols; i++) printf("%d%c", grid[i], i + 1 == n_rows * n_cols ? '\n' : ' ');
        n_solutions++;
        return;
    }
    int r = seq_r[idx], c = seq_c[idx], rn = row_node[r];
    n_nodes++; nodes_at_row[r]++;
    int cn = col_node[c];
    int ra = R.start[rn], rb = ra + R.count[rn];
    int ca = C.start[cn], cb = ca + C.count[cn];
    if (ra == rb || ca == cb) return;
    /* Intersect two sorted child lists: walk the shorter one and binary-search
       the longer one. */
    int *cw = scratch[r * n_cols + c], k = 0;
    int row_is_short = rb - ra <= cb - ca;
    const int *sw = row_is_short ? R.word : C.word, *lw = row_is_short ? C.word : R.word;
    int sa = row_is_short ? ra : ca, sb = row_is_short ? rb : cb;
    int la = row_is_short ? ca : ra, lb = row_is_short ? cb : rb;
    for (int i = sa; i < sb; i++) {
        int w = sw[i], lo = la, hi = lb;
        while (lo < hi) { int mid = (lo + hi) / 2; if (lw[mid] < w) lo = mid + 1; else hi = mid; }
        la = lo;
        if (lo < lb && lw[lo] == w) {
            cw[3 * k] = w;
            cw[3 * k + 1] = R.child[row_is_short ? i : lo];
            cw[3 * k + 2] = C.child[row_is_short ? lo : i];
            k++;
        }
    }
    if (shuffle && temp < 0) {
        for (int i = k - 1; i > 0; i--) {
            int j = next_rand() % (i + 1), tmp[3];
            memcpy(tmp, cw + 3 * i, sizeof tmp); memcpy(cw + 3 * i, cw + 3 * j, sizeof tmp); memcpy(cw + 3 * j, tmp, sizeof tmp);
        }
    } else if (shuffle) {
        Cand *cd = cands[r * n_cols + c];
        for (int i = 0; i < k; i++) {
            double u = (next_rand() + 1.0) / 4294967297.0;
            cd[i].key = log((double)R.size[cw[3 * i + 1]]) + log((double)C.size[cw[3 * i + 2]]) - temp * log(-log(u));
            memcpy(cd[i].v, cw + 3 * i, sizeof cd[i].v);
        }
        qsort(cd, k, sizeof(Cand), cmp_cand);
        for (int i = 0; i < k; i++) memcpy(cw + 3 * i, cd[i].v, sizeof cd[i].v);
    }
    for (int i = 0; i < k && !stop(); i++) {
        int w = cw[3 * i];
        if (idx == 1 && ((unsigned)grid[0] * 2654435761u + (unsigned)w) % (unsigned)n_parts != (unsigned)part) continue;
        int rep = used[w] > 0;
        int new_bound = col_bound - C.mincost[cn] + C.mincost[cw[3 * i + 2]];
        if (repeats + rep > max_repeats || total_cost + cost[w] + new_bound > max_cost) continue;
        int old_bound = col_bound;
        col_bound = new_bound;
        repeats += rep; used[w]++; total_cost += cost[w];
        grid[r * n_cols + c] = w;
        row_node[r] = cw[3 * i + 1];
        col_node[c] = cw[3 * i + 2];
        fill(idx + 1);
        row_node[r] = rn;
        col_node[c] = cn;
        used[w]--; repeats -= rep; total_cost -= cost[w];
        col_bound = old_bound;
    }
}

int main(int argc, char **argv) {
    if (argc != 15 && argc != 16) {
        fprintf(stderr, "usage: solver ROWS COLS COSTS n_rows n_cols max_repeats max_cost "
                        "max_solutions max_nodes seed temp restart_nodes part n_parts\n");
        return 1;
    }
    n_rows = atoi(argv[4]); n_cols = atoi(argv[5]);
    max_repeats = atoi(argv[6]); max_cost = atoi(argv[7]);
    max_solutions = atol(argv[8]); max_nodes = atol(argv[9]);
    long seed = atol(argv[10]);
    temp = atof(argv[11]); restart_nodes = seed ? atol(argv[12]) : 0;
    part = atoi(argv[13]); n_parts = atoi(argv[14]);
    make_order(argc == 16 && atoi(argv[15]));
    shuffle = seed != 0; rng = 0x9E3779B97F4A7C15ULL ^ (unsigned long long)seed;
    int max_word = 0;
    R = load(argv[1], n_cols, &max_word);
    C = load(argv[2], n_rows, &max_word);
    used = calloc(max_word + 1, sizeof(int));
    cost = calloc(max_word + 1, sizeof(int));
    FILE *f = fopen(argv[3], "r");
    if (!f) { perror(argv[3]); return 1; }
    for (int i = 0; i <= max_word; i++)
        if (fscanf(f, "%d", &cost[i]) != 1) { fprintf(stderr, "cost file too short\n"); return 1; }
    fclose(f);
    C.mincost = malloc(sizeof(int) * C.n_nodes);
    fill_mincost(&C, 0);
    col_bound = n_cols * C.mincost[0];
    /* A cell has at most as many candidates as there are distinct words. */
    for (int i = 0; i < n_rows * n_cols; i++) {
        scratch[i] = malloc(sizeof(int) * 3 * (max_word + 1));
        cands[i] = malloc(sizeof(Cand) * (max_word + 1));
    }
    long restarts = 0;
    do {
        restart_at = n_nodes + restart_nodes;
        fill(0);
        restarts++;
    } while (restart_nodes && !finished());
    fprintf(stderr, "nodes per row:");
    for (int i = 0; i < n_rows; i++) fprintf(stderr, " %ld", nodes_at_row[i]);
    fprintf(stderr, "\n");
    fprintf(stderr, "solutions %ld nodes %ld restarts %ld%s\n", n_solutions, n_nodes, restarts - 1,
            finished() ? " (stopped at limit)" : " (exhaustive)");
    return 0;
}
