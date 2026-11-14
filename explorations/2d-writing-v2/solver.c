/* Exact search for word grids whose rows and columns are all listed sentences.
 *
 * Usage: solver ROWS COLS n_rows n_cols max_repeats max_solutions max_nodes seed
 *   ROWS: file with one sentence per line as n_cols space-separated word ids
 *   COLS: file with one sentence per line as n_rows space-separated word ids
 *   max_repeats: number of cells allowed to hold a word already in the grid
 *   max_solutions, max_nodes: stop limits (0 = no limit)
 *   seed: 0 = try candidates in id order; otherwise shuffle them at each cell
 * Output: one grid per line, n_rows*n_cols word ids in row-major order.
 *
 * Cells are filled in row-major order. Rows and columns are stored as tries;
 * the candidates for a cell are the words that are children of both the row's
 * trie node and the column's trie node.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXN 8

typedef struct { int *word; int *child; int *start; int *count; int n_nodes; int n_edges; } Trie;

static int g_len;
static int cmp_sent(const void *a, const void *b) {
    const int *x = a, *y = b;
    for (int i = 0; i < g_len; i++) if (x[i] != y[i]) return x[i] < y[i] ? -1 : 1;
    return 0;
}

/* Build node for sentences [lo,hi) which share their first `depth` words. */
static int build(Trie *t, int *s, int len, int lo, int hi, int depth) {
    int node = t->n_nodes++;
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
    t.start = malloc(sizeof(int) * m); t.count = malloc(sizeof(int) * m);
    t.n_nodes = 0; t.n_edges = 0;
    build(&t, s, len, 0, n, 0);
    free(s);
    return t;
}

static Trie R, C;
static int n_rows, n_cols, max_repeats;
static long max_solutions, max_nodes, n_solutions, n_nodes;
static int grid[MAXN * MAXN], col_node[MAXN], *used, repeats;
static unsigned long long rng;
static int shuffle;

static unsigned next_rand(void) {
    rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
    return (unsigned)(rng >> 16);
}

static int stop(void) {
    return (max_solutions && n_solutions >= max_solutions) || (max_nodes && n_nodes >= max_nodes);
}

static void fill(int r, int c, int row_node) {
    if (r == n_rows) {
        for (int i = 0; i < n_rows * n_cols; i++) printf("%d%c", grid[i], i + 1 == n_rows * n_cols ? '\n' : ' ');
        n_solutions++;
        return;
    }
    n_nodes++;
    int cn = col_node[c];
    int ra = R.start[row_node], rb = ra + R.count[row_node];
    int ca = C.start[cn], cb = ca + C.count[cn];
    /* intersect two sorted child lists */
    int cap = (rb - ra < cb - ca ? rb - ra : cb - ca);
    if (cap == 0) return;
    int *cw = malloc(sizeof(int) * 3 * cap), k = 0;
    while (ra < rb && ca < cb) {
        if (R.word[ra] < C.word[ca]) ra++;
        else if (R.word[ra] > C.word[ca]) ca++;
        else { cw[3 * k] = R.word[ra]; cw[3 * k + 1] = R.child[ra]; cw[3 * k + 2] = C.child[ca]; k++; ra++; ca++; }
    }
    if (shuffle)
        for (int i = k - 1; i > 0; i--) {
            int j = next_rand() % (i + 1), tmp[3];
            memcpy(tmp, cw + 3 * i, sizeof tmp); memcpy(cw + 3 * i, cw + 3 * j, sizeof tmp); memcpy(cw + 3 * j, tmp, sizeof tmp);
        }
    for (int i = 0; i < k && !stop(); i++) {
        int w = cw[3 * i];
        int rep = used[w] > 0;
        if (repeats + rep > max_repeats) continue;
        repeats += rep; used[w]++;
        grid[r * n_cols + c] = w;
        col_node[c] = cw[3 * i + 2];
        if (c + 1 < n_cols) fill(r, c + 1, cw[3 * i + 1]);
        else fill(r + 1, 0, 0);
        col_node[c] = cn;
        used[w]--; repeats -= rep;
    }
    free(cw);
}

int main(int argc, char **argv) {
    if (argc != 9) { fprintf(stderr, "usage: solver ROWS COLS n_rows n_cols max_repeats max_solutions max_nodes seed\n"); return 1; }
    n_rows = atoi(argv[3]); n_cols = atoi(argv[4]); max_repeats = atoi(argv[5]);
    max_solutions = atol(argv[6]); max_nodes = atol(argv[7]);
    long seed = atol(argv[8]);
    shuffle = seed != 0; rng = 0x9E3779B97F4A7C15ULL ^ (unsigned long long)seed;
    int max_word = 0;
    R = load(argv[1], n_cols, &max_word);
    C = load(argv[2], n_rows, &max_word);
    used = calloc(max_word + 1, sizeof(int));
    fill(0, 0, 0);
    fprintf(stderr, "solutions %ld nodes %ld%s\n", n_solutions, n_nodes, stop() ? " (stopped at limit)" : " (exhaustive)");
    return 0;
}
