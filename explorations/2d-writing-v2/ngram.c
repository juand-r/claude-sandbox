/* Search for word grids whose lines are admissible under n-gram rules.
 *
 * A line (row or column) w_1 .. w_L is admissible for order k (k < L) if
 *   - w_1 .. w_k is in the set P of k-grams that begin a sentence,
 *   - every window w_i .. w_{i+k-1} with 1 < i < L-k+1 is in the set M of
 *     k-grams seen anywhere in a sentence, and
 *   - w_{L-k+1} .. w_L is in the set F of k-grams that end a sentence.
 * With L = k + 1 this says: the first k words begin a real sentence and the
 * last k words end one. The admissible lines are far too many to list, so the
 * search works on the k-gram sets directly. Cells are filled in row-major
 * order; the candidates for a cell are the words allowed by both its row and
 * its column.
 *
 * Usage: ngram RP RM RF CP CM CF COSTS n_rows n_cols k max_repeats max_cost
 *              max_solutions max_nodes seed restart_nodes part n_parts
 *   RP RM RF: k-gram files for rows (one k-gram per line, word ids);
 *   CP CM CF: the same for columns
 *   COSTS: one integer per word id; the sum over all cells must be <= max_cost
 *   max_repeats: number of cells allowed to hold a word already in the grid
 *   max_solutions, max_nodes: stop limits (0 = no limit)
 *   seed: 0 = candidates in id order; otherwise shuffled at each cell
 *   restart_nodes: with seed != 0 and restart_nodes > 0, start again from the
 *     empty grid after this many nodes or as soon as one grid is found, so
 *     that the output is a varied sample (grids may repeat in the output)
 *   part, n_parts: only search grids whose first two words hash to part
 * Output: one grid per line, n_rows*n_cols word ids in row-major order.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXN 8

typedef struct { int *word, *child, *start, *count; int n_nodes, n_edges; } Trie;

static int g_len, n_words;

static int cmp_gram(const void *a, const void *b) {
    const int *x = a, *y = b;
    for (int i = 0; i < g_len; i++) if (x[i] != y[i]) return x[i] < y[i] ? -1 : 1;
    return 0;
}

static int build(Trie *t, int *s, int len, int lo, int hi, int depth) {
    int node = t->n_nodes++;
    if (depth == len) { t->start[node] = 0; t->count[node] = 0; return node; }
    int n_children = 0;
    for (int i = lo; i < hi; i++)
        if (i == lo || s[i * len + depth] != s[(i - 1) * len + depth]) n_children++;
    int first = t->n_edges, k = 0, i = lo;
    t->n_edges += n_children;
    t->start[node] = first; t->count[node] = n_children;
    while (i < hi) {
        int j = i;
        while (j < hi && s[j * len + depth] == s[i * len + depth]) j++;
        t->word[first + k] = s[i * len + depth];
        t->child[first + k] = build(t, s, len, i, j, depth + 1);
        k++; i = j;
    }
    return node;
}

static Trie load(const char *path, int len) {
    FILE *f = fopen(path, "r");
    if (!f) { perror(path); exit(1); }
    int cap = 1 << 20, n = 0, *s = malloc(sizeof(int) * cap * len);
    for (;;) {
        if (n == cap) { cap *= 2; s = realloc(s, sizeof(int) * cap * len); }
        int ok = 1;
        for (int i = 0; i < len; i++) if (fscanf(f, "%d", &s[n * len + i]) != 1) ok = 0;
        if (!ok) break;
        for (int i = 0; i < len; i++) if (s[n * len + i] >= n_words) n_words = s[n * len + i] + 1;
        n++;
    }
    fclose(f);
    g_len = len;
    qsort(s, n, sizeof(int) * len, cmp_gram);
    /* drop duplicate k-grams */
    int m = 0;
    for (int i = 0; i < n; i++)
        if (i == 0 || cmp_gram(s + (size_t)i * len, s + (size_t)(m - 1) * len) != 0)
            memmove(s + (size_t)m++ * len, s + (size_t)i * len, sizeof(int) * len);
    Trie t;
    size_t size = (size_t)m * len + 2;
    t.word = malloc(sizeof(int) * size); t.child = malloc(sizeof(int) * size);
    t.start = malloc(sizeof(int) * size); t.count = malloc(sizeof(int) * size);
    t.n_nodes = 0; t.n_edges = 0;
    build(&t, s, len, 0, m, 0);
    free(s);
    return t;
}

/* Child of `node` labelled w, or -1. */
static int step(const Trie *t, int node, int w) {
    int lo = t->start[node], hi = lo + t->count[node];
    while (lo < hi) { int mid = (lo + hi) / 2; if (t->word[mid] < w) lo = mid + 1; else hi = mid; }
    return (lo < t->start[node] + t->count[node] && t->word[lo] == w) ? t->child[lo] : -1;
}

typedef struct { Trie P, M, F; int len; } Dir; /* k-gram sets for one direction */
static Dir RD, CD;
static int n_rows, n_cols, K, max_repeats, max_cost, part, n_parts;
static long max_solutions, max_nodes, n_solutions, n_nodes, restart_nodes, restart_at;
static int grid[MAXN][MAXN], col_node[MAXN], *used, *cost, repeats, total_cost;
static int *scratch[MAXN * MAXN];
static unsigned long long rng;
static int shuffle;

static unsigned next_rand(void) {
    rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
    return (unsigned)(rng >> 16);
}
static int finished(void) {
    return (max_solutions && n_solutions >= max_solutions) || (max_nodes && n_nodes >= max_nodes);
}
static int found; /* a grid was found since the last restart */
static int stop(void) { return finished() || (restart_nodes && (found || n_nodes >= restart_at)); }

/* Node whose children are the words allowed at position pos (>= K) of a line,
 * given the K-1 words before it (ctx[0..K-2]); -1 if there are none. */
static int context_node(const Dir *d, int pos, const int *ctx, const Trie **trie) {
    const Trie *t = pos == d->len - 1 ? &d->F : &d->M;
    int node = 0;
    for (int i = 0; i < K - 1 && node >= 0; i++) node = step(t, node, ctx[i]);
    *trie = t;
    return node;
}

static void fill(int r, int c, int row_node) {
    if (r == n_rows) {
        for (int i = 0; i < n_rows; i++)
            for (int j = 0; j < n_cols; j++)
                printf("%d%c", grid[i][j], i + 1 == n_rows && j + 1 == n_cols ? '\n' : ' ');
        n_solutions++; found = 1;
        return;
    }
    n_nodes++;
    const Trie *rt = &RD.P, *ct = &CD.P;
    int rn = row_node, cn = col_node[c], ctx[MAXN];
    if (c >= K) {
        for (int i = 0; i < K - 1; i++) ctx[i] = grid[r][c - K + 1 + i];
        rn = context_node(&RD, c, ctx, &rt);
    }
    if (r >= K) {
        for (int i = 0; i < K - 1; i++) ctx[i] = grid[r - K + 1 + i][c];
        cn = context_node(&CD, r, ctx, &ct);
    }
    if (rn < 0 || cn < 0) return;
    int ra = rt->start[rn], rb = ra + rt->count[rn], ca = ct->start[cn], cb = ca + ct->count[cn];
    if (ra == rb || ca == cb) return;
    /* intersect the two sorted word lists: walk the shorter, search the longer */
    int *cw = scratch[r * n_cols + c], k = 0;
    int row_short = rb - ra <= cb - ca;
    const int *sw = row_short ? rt->word : ct->word, *lw = row_short ? ct->word : rt->word;
    int sa = row_short ? ra : ca, sb = row_short ? rb : cb, la = row_short ? ca : ra, lb = row_short ? cb : rb;
    for (int i = sa; i < sb; i++) {
        int w = sw[i], lo = la, hi = lb;
        while (lo < hi) { int mid = (lo + hi) / 2; if (lw[mid] < w) lo = mid + 1; else hi = mid; }
        la = lo;
        if (lo < lb && lw[lo] == w) {
            cw[3 * k] = w;
            cw[3 * k + 1] = rt->child[row_short ? i : lo];
            cw[3 * k + 2] = ct->child[row_short ? lo : i];
            k++;
        }
    }
    if (shuffle)
        for (int i = k - 1; i > 0; i--) {
            int j = next_rand() % (i + 1), tmp[3];
            memcpy(tmp, cw + 3 * i, sizeof tmp); memcpy(cw + 3 * i, cw + 3 * j, sizeof tmp); memcpy(cw + 3 * j, tmp, sizeof tmp);
        }
    for (int i = 0; i < k && !stop(); i++) {
        int w = cw[3 * i];
        if (r == 0 && c == 1 && ((unsigned)grid[0][0] * 2654435761u + (unsigned)w) % (unsigned)n_parts != (unsigned)part) continue;
        int rep = used[w] > 0;
        if (repeats + rep > max_repeats || total_cost + cost[w] > max_cost) continue;
        grid[r][c] = w;
        /* look ahead: the next cell of this column (and of this row) must have
           a context that occurs at all */
        const Trie *t;
        if (r + 1 < n_rows && r + 1 >= K) {
            for (int j = 0; j < K - 1; j++) ctx[j] = grid[r - K + 2 + j][c];
            if (context_node(&CD, r + 1, ctx, &t) < 0) continue;
        }
        if (c + 1 < n_cols && c + 1 >= K) {
            for (int j = 0; j < K - 1; j++) ctx[j] = grid[r][c - K + 2 + j];
            if (context_node(&RD, c + 1, ctx, &t) < 0) continue;
        }
        repeats += rep; used[w]++; total_cost += cost[w];
        int saved = col_node[c];
        if (r < K) col_node[c] = cw[3 * i + 2];
        if (c + 1 < n_cols) fill(r, c + 1, c < K ? cw[3 * i + 1] : 0);
        else fill(r + 1, 0, 0);
        col_node[c] = saved;
        used[w]--; repeats -= rep; total_cost -= cost[w];
    }
}

int main(int argc, char **argv) {
    if (argc != 19) {
        fprintf(stderr, "usage: ngram RP RM RF CP CM CF COSTS n_rows n_cols k max_repeats max_cost "
                        "max_solutions max_nodes seed restart_nodes part n_parts\n");
        return 1;
    }
    n_rows = atoi(argv[8]); n_cols = atoi(argv[9]); K = atoi(argv[10]);
    if (K < 2 || K >= n_rows || K >= n_cols) { fprintf(stderr, "need 2 <= k < n_rows, n_cols\n"); return 1; }
    max_repeats = atoi(argv[11]); max_cost = atoi(argv[12]);
    max_solutions = atol(argv[13]); max_nodes = atol(argv[14]);
    long seed = atol(argv[15]);
    restart_nodes = seed ? atol(argv[16]) : 0;
    part = atoi(argv[17]); n_parts = atoi(argv[18]);
    shuffle = seed != 0; rng = 0x9E3779B97F4A7C15ULL ^ (unsigned long long)seed;
    RD.P = load(argv[1], K); RD.M = load(argv[2], K); RD.F = load(argv[3], K); RD.len = n_cols;
    CD.P = load(argv[4], K); CD.M = load(argv[5], K); CD.F = load(argv[6], K); CD.len = n_rows;
    used = calloc(n_words, sizeof(int));
    cost = calloc(n_words, sizeof(int));
    FILE *f = fopen(argv[7], "r");
    if (!f) { perror(argv[7]); return 1; }
    for (int i = 0; i < n_words; i++)
        if (fscanf(f, "%d", &cost[i]) != 1) { fprintf(stderr, "cost file too short\n"); return 1; }
    fclose(f);
    for (int i = 0; i < n_rows * n_cols; i++) scratch[i] = malloc(sizeof(int) * 3 * (n_words + 1));
    long restarts = 0;
    do {
        restart_at = n_nodes + restart_nodes; found = 0;
        fill(0, 0, 0);
        restarts++;
    } while (restart_nodes && !finished());
    fprintf(stderr, "solutions %ld nodes %ld restarts %ld%s\n", n_solutions, n_nodes, restarts - 1,
            finished() ? " (stopped at limit)" : " (exhaustive)");
    return 0;
}
