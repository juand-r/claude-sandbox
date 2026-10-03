/* 1-D HashLife core for Rule 110 (see hashlife.py, which wraps it).

   Nodes are uint32 ids into one array. A leaf (level 6) holds 64 cells in
   a uint64 (bit i = cell i, left to right); an inner node of level k joins
   two level-(k-1) nodes. Nodes are hash-consed (equal content at equal
   level is one id) and result(n, j), the centre half of n after 2^j steps
   (j <= level - 2), is memoized. Same algorithm as the pure-Python
   version it replaced (trash/hashlife_py.py). */

#include <stdint.h>
#include <stdlib.h>
#include <string.h>

#define LEAF 6
#define NONE 0xFFFFFFFFu

typedef struct { uint64_t v; uint32_t a, b; uint8_t k; } Node;

static Node *nodes = 0;
static uint64_t n_nodes = 0, cap_nodes = 0;

/* open-addressing tables: key -> id + 1 (0 = empty) */
typedef struct { uint64_t *keys; uint32_t *vals; uint64_t cap, used; } Table;
static Table t_leaf, t_join, t_res;

static uint64_t mix(uint64_t x) {           /* splitmix64 finalizer */
    x ^= x >> 30; x *= 0xbf58476d1ce4e5b9ULL;
    x ^= x >> 27; x *= 0x94d049bb133111ebULL;
    return x ^ (x >> 31);
}

static int table_init(Table *t, uint64_t cap) {
    t->keys = calloc(cap, sizeof(uint64_t));
    t->vals = calloc(cap, sizeof(uint32_t));
    t->cap = cap; t->used = 0;
    return t->keys && t->vals;
}

static void table_free(Table *t) {
    free(t->keys); free(t->vals);
    t->keys = 0; t->vals = 0; t->cap = t->used = 0;
}

static uint32_t table_get(Table *t, uint64_t key) {
    uint64_t m = t->cap - 1, i = mix(key) & m;
    while (t->vals[i]) {
        if (t->keys[i] == key) return t->vals[i] - 1;
        i = (i + 1) & m;
    }
    return NONE;
}

static int table_put(Table *t, uint64_t key, uint32_t val);

static int table_grow(Table *t) {
    Table n;
    if (!table_init(&n, t->cap * 2)) return 0;
    for (uint64_t i = 0; i < t->cap; i++)
        if (t->vals[i]) table_put(&n, t->keys[i], t->vals[i] - 1);
    table_free(t);
    *t = n;
    return 1;
}

static int table_put(Table *t, uint64_t key, uint32_t val) {
    if (2 * (t->used + 1) > t->cap && !table_grow(t)) return 0;
    uint64_t m = t->cap - 1, i = mix(key) & m;
    while (t->vals[i]) {
        if (t->keys[i] == key) { t->vals[i] = val + 1; return 1; }
        i = (i + 1) & m;
    }
    t->keys[i] = key; t->vals[i] = val + 1; t->used++;
    return 1;
}

static int failed = 0;     /* set on allocation failure; checked by Python */

static uint32_t new_node(uint8_t k, uint32_t a, uint32_t b, uint64_t v) {
    if (n_nodes == cap_nodes) {
        uint64_t c = cap_nodes ? 2 * cap_nodes : (1 << 16);
        Node *p = realloc(nodes, c * sizeof(Node));
        if (!p || c > NONE) { failed = 1; return NONE; }
        nodes = p; cap_nodes = c;
    }
    nodes[n_nodes].k = k; nodes[n_nodes].a = a; nodes[n_nodes].b = b;
    nodes[n_nodes].v = v;
    return (uint32_t)n_nodes++;
}

int hl_reset(void) {
    free(nodes); nodes = 0; n_nodes = cap_nodes = 0;
    table_free(&t_leaf); table_free(&t_join); table_free(&t_res);
    failed = 0;
    return table_init(&t_leaf, 1 << 12) && table_init(&t_join, 1 << 16)
        && table_init(&t_res, 1 << 16);
}

int hl_failed(void) { return failed; }

uint32_t hl_leaf(uint64_t v) {
    uint32_t id = table_get(&t_leaf, v);
    if (id != NONE) return id;
    id = new_node(LEAF, NONE, NONE, v);
    if (id == NONE || !table_put(&t_leaf, v, id)) { failed = 1; return NONE; }
    return id;
}

uint32_t hl_join(uint32_t a, uint32_t b) {
    uint64_t key = ((uint64_t)a << 32) | b;
    uint32_t id = table_get(&t_join, key);
    if (id != NONE) return id;
    if (nodes[a].k != nodes[b].k) { failed = 1; return NONE; }
    id = new_node(nodes[a].k + 1, a, b, 0);
    if (id == NONE || !table_put(&t_join, key, id)) { failed = 1; return NONE; }
    return id;
}

int hl_level(uint32_t n) { return nodes[n].k; }
uint32_t hl_a(uint32_t n) { return nodes[n].a; }
uint32_t hl_b(uint32_t n) { return nodes[n].b; }
uint64_t hl_value(uint32_t n) { return nodes[n].v; }
uint64_t hl_count(void) { return n_nodes; }
uint64_t hl_results(void) { return t_res.used; }

uint32_t hl_center(uint32_t n) {
    uint32_t a = nodes[n].a, b = nodes[n].b;
    if (nodes[n].k == LEAF + 1)
        return hl_leaf((nodes[a].v >> 32) | (nodes[b].v << 32));
    return hl_join(nodes[a].b, nodes[b].a);
}

typedef unsigned __int128 u128;

static u128 step128(u128 x, int steps) {
    for (int s = 0; s < steps; s++) {
        u128 left = x << 1, right = x >> 1;
        x = (x | right) & ~(left & x & right);
    }
    return x;
}

uint32_t hl_result(uint32_t n, int j) {
    int k = nodes[n].k;
    if (j < 0 || j > k - 2) { failed = 1; return NONE; }
    uint64_t key = ((uint64_t)n << 8) | (uint64_t)j;
    uint32_t r = table_get(&t_res, key);
    if (r != NONE) return r;
    uint32_t a = nodes[n].a, b = nodes[n].b;
    if (k == LEAF + 1) {
        u128 x = (u128)nodes[a].v | ((u128)nodes[b].v << 64);
        x = step128(x, 1 << j);
        r = hl_leaf((uint64_t)(x >> 32));
    } else {
        uint32_t m = hl_join(nodes[a].b, nodes[b].a);
        uint32_t r1, r2, r3;
        if (j == k - 2) {
            r1 = hl_result(a, j - 1); r2 = hl_result(m, j - 1); r3 = hl_result(b, j - 1);
            uint32_t s1 = hl_result(hl_join(r1, r2), j - 1);
            uint32_t s2 = hl_result(hl_join(r2, r3), j - 1);
            r = hl_join(s1, s2);
        } else {
            r1 = hl_center(a); r2 = hl_center(m); r3 = hl_center(b);
            uint32_t s1 = hl_result(hl_join(r1, r2), j);
            uint32_t s2 = hl_result(hl_join(r2, r3), j);
            r = hl_join(s1, s2);
        }
    }
    if (failed || !table_put(&t_res, key, r)) { failed = 1; return NONE; }
    return r;
}

/* Leaf values of node n for leaf indices [first, first + count), in order. */
static void leaves(uint32_t n, uint64_t base, uint64_t first, uint64_t count,
                   uint64_t *out) {
    int k = nodes[n].k;
    uint64_t size = 1ULL << (k - LEAF);
    if (base + size <= first || base >= first + count) return;
    if (k == LEAF) { out[base - first] = nodes[n].v; return; }
    leaves(nodes[n].a, base, first, count, out);
    leaves(nodes[n].b, base + size / 2, first, count, out);
}

void hl_leaves(uint32_t n, uint64_t first, uint64_t count, uint64_t *out) {
    leaves(n, 0, first, count, out);
}

/* A node from 2^m consecutive leaf values. */
uint32_t hl_from_words(const uint64_t *words, uint64_t count) {
    if (count == 0 || (count & (count - 1))) { failed = 1; return NONE; }
    uint32_t *ids = malloc(count * sizeof(uint32_t));
    if (!ids) { failed = 1; return NONE; }
    for (uint64_t i = 0; i < count; i++) ids[i] = hl_leaf(words[i]);
    for (uint64_t c = count; c > 1; c /= 2)
        for (uint64_t i = 0; i < c / 2; i++) ids[i] = hl_join(ids[2 * i], ids[2 * i + 1]);
    uint32_t r = ids[0];
    free(ids);
    return failed ? NONE : r;
}

/* Garbage collection: keep only the DAG of root (ids are renumbered). */
static uint32_t *remap;
static Node *old;

static uint32_t copy(uint32_t n) {
    if (remap[n] != NONE) return remap[n];
    uint32_t r = old[n].k == LEAF ? hl_leaf(old[n].v)
                                  : hl_join(copy(old[n].a), copy(old[n].b));
    remap[n] = r;
    return r;
}

uint32_t hl_gc(uint32_t root) {
    uint64_t n_old = n_nodes;
    old = nodes; nodes = 0; n_nodes = cap_nodes = 0;
    remap = malloc(n_old * sizeof(uint32_t));
    if (!remap) { failed = 1; return NONE; }
    memset(remap, 0xFF, n_old * sizeof(uint32_t));
    table_free(&t_leaf); table_free(&t_join); table_free(&t_res);
    if (!(table_init(&t_leaf, 1 << 12) && table_init(&t_join, 1 << 16)
          && table_init(&t_res, 1 << 16))) { failed = 1; return NONE; }
    uint32_t r = copy(root);
    free(remap); free(old);
    return failed ? NONE : r;
}
