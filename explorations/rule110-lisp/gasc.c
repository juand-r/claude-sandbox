/* Event loop of the gas engine in C (see gas.py for the method, gasc.py
   for the Python side, which owns all cell-level work).

   C knows orbits and memoized composites only by their geometry: an
   orbit's per-phase left offsets and widths, a composite entry's per-step
   left offsets and widths and the pieces it splits into. Merges are looked
   up by signature (the two items' orbit/entry and phase, and the gap);
   an unknown signature or a sentinel event stops the loop and returns to
   Python (the event stays queued), which resolves it and resumes.

   Items: particle (orbit id, anchor t0/x0: phase 0 at time t0 has its left
   edge at x0), composite (entry id, start ts, left edge xs at ts; stored in
   t0/x0), or sentinel (L or R: bound(t) = b0 +- num*t/den). */

#include <stdint.h>
#include <stdlib.h>
#include <string.h>

#define MIN_GAP 2
#define BOUND_GAP 64           /* see gas.py: groupable */
#define MAX_GROUP_W 256
#define MARGIN 256
#define TILE 14
#define SHIFT 4

enum { DEAD = 0, PART = 1, COMP = 2, SENL = 3, SENR = 4 };
enum { EV_C = 0, EV_M = 1, EV_S = 2 };
enum { OK = 0, NEED_MERGE = 1, NEED_SIDE = 2, NEED_PIECE = 3, NEED_UNIT = 4, ERR = -1 };

typedef struct {
    int64_t t0, x0;
    int64_t tc;            /* creation time (0: an untouched layout row) */
    uint64_t ptok, uid;
    int32_t id, prev, next;
    int8_t kind, cL;
} Item;

typedef struct { int32_t p, d, base; double v, lo_min, hi_max; } Orbit;
typedef struct { int32_t T, base, pbase, np; } Entry;
typedef struct { int64_t off; int32_t kind, id, phase, phL; } Piece;
typedef struct { int64_t t; uint64_t seq, tok; int32_t a, b; int32_t kind; } Event;

static Item *items; static int64_t n_items, cap_items;
static int32_t free_head = -1, head = -1, tail = -1;
static uint64_t next_tok = 1, next_seq = 1;
static Orbit *orbits; static int64_t n_orbits, cap_orbits;
static int32_t *o_off, *o_w; static int8_t *o_phl, *o_phr;
static int64_t n_oarr, cap_oarr;
static Entry *entries; static int64_t n_entries, cap_entries;
static int32_t *e_off, *e_w; static int8_t *e_phl, *e_phr;
/* per step s of an entry: the smallest left edge and the largest right
   boundary (left + width) over steps s..T, relative like e_off */
static int32_t *e_lmin, *e_rmax;
static int64_t n_earr, cap_earr;
static Piece *pieces; static int64_t n_pieces, cap_pieces;
static Event *heap; static int64_t n_heap, cap_heap;
static int64_t now;
static int64_t n_events;
static int64_t sen_b0[2], sen_num[2], sen_den[2];
static int failed;
/* merge counts by family (A: speed 2/3, C: 0, E: -4/15, X: other or a
   composite), for profiling */
static int64_t fam_count[4][4];

/* -- the rope (PLAN.md phase 10b): debris absorbed from the left end of
   the gas, kept outside the event list as units (debris items closer
   than the ossifier span), and the ossifiers (groups of A gliders) in
   transit through it. The front ossifier is swept unit by unit; each
   crossing (the ossifier's gliders and the unit's items, from the time the
   lead glider comes within G_ENTRY of the unit until the last event) is
   looked up by its exact relative configuration, and simulated by Python
   (NEED_UNIT) when new. At its last crossing's end the ossifier is
   emitted right after the left sentinel (the wake). Failure codes 40-49
   are rope checks (fail loudly). */
#define UMAX 64
#define OMAX 8
#define G_ENTRY 32
typedef struct { int32_t n; int32_t it[UMAX]; int64_t tlast; } Unit;
typedef struct { int32_t n; int32_t it[OMAX]; int64_t prog, t; } Oss;
static int rope_on;
static Unit *units; static int64_t n_units, cap_units;
static Oss *oss; static int64_t n_oss, cap_oss;
static int64_t wake = INT64_MAX;
static int64_t rope_cross, rope_miss;
/* crossing memo: key = [n_g, n_u, (orbit, phase, offset)...], result =
   [dt_lo, dt_hi, n_g, n_u, (orbit, phase, offset)...] in an int32 pool */
typedef struct { uint64_t h; int64_t kpos, rpos; int32_t klen, used; } UEnt;
static UEnt *utab; static uint64_t ucap, uused;
static int32_t *upool; static int64_t n_upool, cap_upool;
static int32_t ukey[2 + 3 * (UMAX + OMAX)]; static int32_t ukey_len;
static int64_t ureq_tau, ureq_ref;

static int64_t dbg[8192]; static int64_t n_dbg;   /* unclean A x E merges (t, x) */
int64_t gc_debug(int64_t *out) { memcpy(out, dbg, 2 * n_dbg * sizeof(int64_t)); return n_dbg; }

/* pending request for Python */
static int32_t req_a, req_b, req_k; static int64_t req_t;

#define GROW(arr, n, cap, need) do { \
    if ((n) + (need) > (cap)) { \
        int64_t c_ = (cap) ? 2 * (cap) : 1024; \
        while (c_ < (n) + (need)) c_ *= 2; \
        void *p_ = realloc((arr), c_ * sizeof(*(arr))); \
        if (!p_) { failed = 1; return ERR; } \
        (arr) = p_; (cap) = c_; } } while (0)

/* merge signatures: open addressing, (k1, k2) -> result index + 1 */
typedef struct { uint64_t k1, k2; int32_t kind, id, phase, dx; int32_t used; } MEnt;
static MEnt *mtab; static uint64_t mcap, mused;

static uint64_t mix(uint64_t x) {
    x ^= x >> 30; x *= 0xbf58476d1ce4e5b9ULL;
    x ^= x >> 27; x *= 0x94d049bb133111ebULL;
    return x ^ (x >> 31);
}

static MEnt *mfind(uint64_t k1, uint64_t k2) {
    uint64_t m = mcap - 1, i = mix(k1 ^ mix(k2)) & m;
    while (mtab[i].used) {
        if (mtab[i].k1 == k1 && mtab[i].k2 == k2) return &mtab[i];
        i = (i + 1) & m;
    }
    return &mtab[i];
}

static int mgrow(void) {
    MEnt *old = mtab; uint64_t oc = mcap;
    mcap = oc ? 2 * oc : (1 << 12);
    mtab = calloc(mcap, sizeof(MEnt));
    if (!mtab) { failed = 1; return 0; }
    mused = 0;
    for (uint64_t i = 0; i < oc; i++)
        if (old[i].used) { *mfind(old[i].k1, old[i].k2) = old[i]; mused++; }
    free(old);
    return 1;
}

/* -- item geometry -------------------------------------------------------- */

static inline int64_t fdiv(int64_t a, int64_t b) {   /* floor division, b > 0 */
    int64_t q = a / b;
    return (a % b != 0 && a < 0) ? q - 1 : q;
}

/* phase/step, left edge, width at time t */
static inline void state(const Item *it, int64_t t, int32_t *ph, int64_t *lo, int32_t *w) {
    if (it->kind == PART) {
        const Orbit *o = &orbits[it->id];
        int64_t j = t - it->t0, k = fdiv(j, o->p);
        int32_t s = (int32_t)(j - k * o->p);
        *ph = s; *lo = it->x0 + k * o->d + o_off[o->base + s]; *w = o_w[o->base + s];
    } else {
        const Entry *e = &entries[it->id];
        int32_t s = (int32_t)(t - it->t0);
        *ph = s; *lo = it->x0 + e_off[e->base + s]; *w = e_w[e->base + s];
    }
}

static inline int64_t end_of(const Item *it) {
    return it->kind == COMP ? it->t0 + entries[it->id].T : INT64_MAX;
}

static int64_t gcd64(int64_t a, int64_t b) { while (b) { int64_t r = a % b; a = b; b = r; } return a; }

/* Pair tables: for orbits oa, ob at phases pa, pb (at some time t), the
   gap at t + i is G + h[i] for i in [0, L), G = lb - la (left edges at t),
   and it grows by delta per joint period L. Cached by (oa, ob, pa, pb). */
typedef struct { uint64_t key; int32_t L, delta, hmin, base; int32_t used; } PEnt;
static PEnt *ptab; static uint64_t pcap, pused;
static int32_t *pool; static int64_t n_pool, cap_pool;

static int pgrow(void) {
    PEnt *old = ptab; uint64_t oc = pcap;
    pcap = oc ? 2 * oc : (1 << 12);
    ptab = calloc(pcap, sizeof(PEnt));
    if (!ptab) { failed = 1; return 0; }
    for (uint64_t i = 0; i < oc; i++)
        if (old[i].used) {
            uint64_t m = pcap - 1, j = mix(old[i].key) & m;
            while (ptab[j].used) j = (j + 1) & m;
            ptab[j] = old[i];
        }
    free(old);
    return 1;
}

static const PEnt *pair_table(int32_t ia, int32_t ib, int32_t pa, int32_t pb) {
    uint64_t key = ((uint64_t)ia << 48) | ((uint64_t)ib << 32) | ((uint64_t)pa << 16) | (uint64_t)pb;
    if (4 * (pused + 1) > 3 * pcap && !pgrow()) return 0;
    uint64_t m = pcap - 1, j = mix(key) & m;
    while (ptab[j].used) {
        if (ptab[j].key == key) return &ptab[j];
        j = (j + 1) & m;
    }
    const Orbit *oa = &orbits[ia], *ob = &orbits[ib];
    int64_t L = oa->p / gcd64(oa->p, ob->p) * ob->p;
    if (n_pool + L > cap_pool) {
        int64_t c = cap_pool ? 2 * cap_pool : (1 << 16);
        while (c < n_pool + L) c *= 2;
        int32_t *q = realloc(pool, c * sizeof(int32_t));
        if (!q) { failed = 1; return 0; }
        pool = q; cap_pool = c;
    }
    PEnt *e = &ptab[j];
    e->key = key; e->used = 1; pused++;
    e->L = (int32_t)L; e->base = (int32_t)n_pool;
    e->delta = (int32_t)(ob->d * (L / ob->p) - oa->d * (L / oa->p));
    int32_t hmin = INT32_MAX;
    int32_t oa0 = o_off[oa->base + pa], ob0 = o_off[ob->base + pb];
    for (int64_t i = 0; i < L; i++) {
        int64_t ja = pa + i, jb = pb + i;
        int32_t sa = (int32_t)(ja % oa->p), sb = (int32_t)(jb % ob->p);
        int64_t xa = (ja / oa->p) * oa->d + o_off[oa->base + sa] - oa0;
        int64_t xb = (jb / ob->p) * ob->d + o_off[ob->base + sb] - ob0;
        int32_t h = (int32_t)(xb - xa - o_w[oa->base + sa]);
        pool[n_pool + i] = h;
        if (h < hmin) hmin = h;
    }
    e->hmin = hmin;
    n_pool += L;
    return e;
}

static int64_t collision_periodic(const Item *a, const Item *b, int64_t t) {
    int32_t pa, pb, wa, wb; int64_t la, lb;
    state(a, t, &pa, &la, &wa); state(b, t, &pb, &lb, &wb);
    const PEnt *e = pair_table(a->id, b->id, pa, pb);
    if (!e) return -2;
    int64_t G = lb - la;
    const int32_t *h = pool + e->base;
    if (G + e->hmin >= MIN_GAP) {
        if (e->delta >= 0) return -1;                   /* never */
        /* first period n* in which some phase dips below MIN_GAP, then
           the first such phase */
        int64_t D = -e->delta;
        int64_t q = (G + e->hmin - MIN_GAP) / D;        /* >= 0 */
        int64_t thr = (q + 1) * D - G + MIN_GAP;        /* h_i < thr */
        for (int32_t i = 0; i < e->L; i++)
            if (h[i] < thr) return t + i + (q + 1) * e->L;
        failed = 6;                                      /* unreachable */
        return -2;
    }
    for (int32_t i = 0; i < e->L; i++)
        if (G + h[i] < MIN_GAP) return t + i;
    failed = 6;
    return -2;
}

/* an item's edges stepped one time unit at a time */
typedef struct { int64_t x; int32_t s, w; const Item *it; } Cursor;

static inline void cur_init(Cursor *c, const Item *it, int64_t t) {
    c->it = it;
    state(it, t, &c->s, &c->x, &c->w);
}

static inline void cur_next(Cursor *c) {
    const Item *it = c->it;
    if (it->kind == PART) {
        const Orbit *o = &orbits[it->id];
        int32_t s = c->s + 1;
        int64_t x = c->x - o_off[o->base + c->s];
        if (s == o->p) { s = 0; x += o->d; }
        c->s = s; c->x = x + o_off[o->base + s]; c->w = o_w[o->base + s];
    } else {
        const Entry *e = &entries[it->id];
        int64_t x0 = c->x - e_off[e->base + c->s];
        c->s++;
        c->x = x0 + e_off[e->base + c->s]; c->w = e_w[e->base + c->s];
    }
}

/* first time >= t with fewer than MIN_GAP cells between a and b, or -1
   (-2: failure) */
static int64_t collision(const Item *a, const Item *b, int64_t t) {
    if (a->kind == PART && b->kind == PART) return collision_periodic(a, b, t);
    int64_t ea = end_of(a), eb = end_of(b);
    int64_t horizon = ea < eb ? ea : eb;
    int64_t n = horizon - t + 1;
    Cursor ca, cb;
    cur_init(&ca, a, t); cur_init(&cb, b, t);
    if (cb.x - ca.x - ca.w >= MIN_GAP + 2 * n) return -1;     /* light cone */
    /* a lower bound on the gap, linear in i: skip the steps before it
       can fall under MIN_GAP */
    double ba, va, bb, vb;
    if (a->kind == PART) {
        const Orbit *o = &orbits[a->id];
        /* linear path at t: period anchor + v s (the orbit's bounds are
           relative to it) */
        ba = (double)(ca.x - o_off[o->base + ca.s]) + o->v * ca.s + o->hi_max; va = o->v;
    } else {
        const Entry *e = &entries[a->id];
        ba = (double)(a->x0 + e_rmax[e->base + ca.s]); va = 0;
    }
    if (b->kind == PART) {
        const Orbit *o = &orbits[b->id];
        bb = (double)(cb.x - o_off[o->base + cb.s]) + o->v * cb.s + o->lo_min; vb = o->v;
    } else {
        const Entry *e = &entries[b->id];
        bb = (double)(b->x0 + e_lmin[e->base + cb.s]); vb = 0;
    }
    double lb0 = bb - ba, closing = va - vb;
    int64_t i0 = 0;
    if (lb0 >= MIN_GAP) {
        if (closing <= 0) return -1;
        double di = (lb0 - MIN_GAP) / closing - 1;          /* -1: rounding */
        if (di >= (double)n) return -1;
        if (di > 0) i0 = (int64_t)di;
    }
    if (i0) { cur_init(&ca, a, t + i0); cur_init(&cb, b, t + i0); }
    for (int64_t i = i0;; i++) {
        if (cb.x - ca.x - ca.w < MIN_GAP) return t + i;
        if (i + 1 >= n) return -1;
        cur_next(&ca); cur_next(&cb);
    }
}

static inline int64_t sen_bound(int side, int64_t t) {    /* side 0: L, 1: R */
    int64_t m = fdiv(sen_num[side] * t, sen_den[side]);
    return side == 0 ? sen_b0[0] + m : sen_b0[1] - m;
}

/* conservative time from which the item next to a sentinel may come
   within MARGIN of it, or -1 */
static int64_t sentinel_time(const Item *a, const Item *b, int64_t t) {
    int left = a->kind == SENL;

    const Item *it = left ? b : a;
    int32_t ph, w; int64_t l;
    state(it, t, &ph, &l, &w);
    double v, lo, hi; int64_t end = -1;
    if (it->kind == PART) {
        const Orbit *o = &orbits[it->id];
        double lin = (double)(l - o_off[o->base + ph]) + o->v * ph;
        v = o->v; lo = lin + o->lo_min; hi = lin + o->hi_max;
    } else {
        lo = (double)l; hi = (double)(l + w); end = end_of(it);
        v = left ? -1.0 : 1.0;
    }
    int side = left ? 0 : 1;
    double vmax = (double)sen_num[side] / (double)sen_den[side];
    double gap, closing;
    if (left) { gap = lo - (double)sen_bound(0, t) - MARGIN; closing = vmax - v; }
    else { gap = (double)sen_bound(1, t) - hi - MARGIN; closing = v + vmax; }
    if (it->kind == PART) {
        /* exact: a particle moving with the side never gets closer */
        const Orbit *o = &orbits[it->id];
        int64_t c = left ? sen_num[0] * o->p - (int64_t)o->d * sen_den[0]
                         : (int64_t)o->d * sen_den[1] + sen_num[1] * o->p;
        if (c <= 0) return -1;
    } else if (closing <= 0) return -1;
    if (gap <= 0) return t;
    int64_t tc = t + (int64_t)(gap / closing);
    if (end >= 0 && tc > end) return -1;
    return tc;
}

/* the left sentinel's event: an emission at the wake time, or (an error
   when the rope is on) something approaching */
static int64_t sentinel_event(const Item *a, const Item *b, int64_t t) {
    int64_t tc = sentinel_time(a, b, t);
    if (a->kind == SENL && rope_on && wake != INT64_MAX) {
        int64_t w = wake > t ? wake : t;
        if (tc < 0 || w <= tc) return w;
    }
    return tc;
}

/* -- heap ------------------------------------------------------------------- */

static inline int ev_less(const Event *x, const Event *y) {
    return x->t < y->t || (x->t == y->t && x->seq < y->seq);
}

static int push(int64_t t, int kind, int32_t a, int32_t b, uint64_t tok) {
    GROW(heap, n_heap, cap_heap, 1);
    Event e = { t, next_seq++, tok, a, b, kind };
    int64_t i = n_heap++;
    while (i > 0) {
        int64_t p = (i - 1) / 2;
        if (!ev_less(&e, &heap[p])) break;
        heap[i] = heap[p]; i = p;
    }
    heap[i] = e;
    return OK;
}

static void pop(void) {
    Event e = heap[--n_heap];
    int64_t i = 0;
    for (;;) {
        int64_t c = 2 * i + 1;
        if (c >= n_heap) break;
        if (c + 1 < n_heap && ev_less(&heap[c + 1], &heap[c])) c++;
        if (!ev_less(&heap[c], &e)) break;
        heap[i] = heap[c]; i = c;
    }
    if (n_heap) heap[i] = e;
}

/* -- list -------------------------------------------------------------------- */

static int32_t alloc_item(void) {
    if (free_head >= 0) {
        int32_t i = free_head;
        free_head = items[i].next;
        return i;
    }
    if (n_items == cap_items) {
        int64_t c = cap_items ? 2 * cap_items : 1024;
        Item *p = realloc(items, c * sizeof(Item));
        if (!p) { failed = 1; return -1; }
        items = p; cap_items = c;
    }
    return (int32_t)n_items++;
}

static void free_item(int32_t i) {
    items[i].kind = DEAD; items[i].ptok = 0; items[i].uid = 0;
    items[i].next = free_head; free_head = i;
}

static int groupable(const Item *a, const Item *b, int64_t t) {
    if (a->kind != PART || b->kind != PART) return 0;
    if (orbits[a->id].d != 0 || orbits[b->id].d != 0) return 0;
    int32_t pa, pb, wa, wb; int64_t la, lb;
    state(a, t, &pa, &la, &wa); state(b, t, &pb, &lb, &wb);
    int64_t g = lb - la - wa;
    return g >= 0 && g < BOUND_GAP && lb + wb - la <= MAX_GROUP_W;
}

static int schedule_pair(int32_t a, int64_t t) {
    Item *ia = &items[a];
    int32_t b = ia->next;
    if (b < 0 || ia->kind == SENR) return OK;
    ia->ptok = next_tok++;
    Item *ib = &items[b];
    int64_t tc; int kind;
    if (ia->kind == SENL || ib->kind == SENR) {
        if (ia->kind == SENL && ib->kind == SENR) { failed = 2; return ERR; }
        tc = sentinel_event(ia, ib, t); kind = EV_M;
    } else if (groupable(ia, ib, t)) { tc = t; kind = EV_C; }   /* join now */
    else { tc = collision(ia, ib, t); kind = EV_C; }
    if (tc == -2) return ERR;
    if (tc >= 0) return push(tc, kind, a, b, ia->ptok);
    return OK;
}

static int schedule_item(int32_t i, int64_t t) {
    Item *it = &items[i];
    if (it->kind == COMP && push(end_of(it), EV_S, i, -1, it->uid) != OK) return ERR;
    return schedule_pair(i, t);
}

/* replace items first..last (adjacent, left to right) by the n new ones
   in idx[] (already filled, unlinked) and schedule */
static int replace(int32_t first, int32_t last, const int32_t *idx, int n, int64_t t) {
    int32_t left = items[first].prev, right = items[last].next;
    for (int32_t i = first;; ) {
        int32_t nx = items[i].next;
        free_item(i);
        if (i == last) break;
        i = nx;
    }
    int32_t prev = left;
    for (int k = 0; k < n; k++) {
        items[idx[k]].prev = prev;
        if (prev < 0) head = idx[k]; else items[prev].next = idx[k];
        prev = idx[k];
    }
    if (prev < 0) head = right; else items[prev].next = right;
    if (right < 0) tail = prev; else items[right].prev = prev;
    for (int k = 0; k < n; k++)
        if (schedule_item(idx[k], t) != OK) return ERR;
    if (left >= 0 && schedule_pair(left, t) != OK) return ERR;
    return OK;
}

static int32_t new_item(int kind, int32_t id, int64_t t0, int64_t x0, int cL, int64_t tc) {
    int32_t i = alloc_item();
    if (i < 0) return -1;
    Item *it = &items[i];
    it->kind = (int8_t)kind; it->id = id; it->t0 = t0; it->x0 = x0; it->tc = tc;
    it->cL = (int8_t)cL; it->ptok = 0; it->uid = next_tok++;
    it->prev = it->next = -1;
    return i;
}

static inline int mod14(int64_t x) { int r = (int)(x % TILE); return r < 0 ? r + TILE : r; }

/* item for a piece of kind/id/phase at left edge lo, time t */
static int32_t piece_item(int kind, int32_t id, int32_t phase, int64_t lo, int64_t t, int cL) {
    if (kind == PART) {
        const Orbit *o = &orbits[id];
        return new_item(PART, id, t - phase, lo - o_off[o->base + phase], cL, t);
    }
    return new_item(COMP, id, t, lo, cL, t);
}

static void signature(const Item *a, const Item *b, int64_t t, uint64_t *k1, uint64_t *k2,
                      int64_t *la, int32_t *wa, int64_t *lb) {
    int32_t pa, pb, wb;
    state(a, t, &pa, la, wa); state(b, t, &pb, lb, &wb);
    int64_t g = *lb - *la - *wa;
    *k1 = ((uint64_t)a->kind << 62) | ((uint64_t)(uint32_t)a->id << 32) | (uint64_t)(uint32_t)pa;
    *k2 = ((uint64_t)b->kind << 62) | ((uint64_t)(uint32_t)b->id << 32) | ((uint64_t)pb << 8)
          | (uint64_t)(g & 255);
}


static int family(const Item *it) {
    if (it->kind != PART) return 3;
    const Orbit *o = &orbits[it->id];
    if (3 * o->d == 2 * o->p) return 0;
    if (o->d == 0) return 1;
    if (15 * o->d == -4 * o->p) return 2;
    return 3;
}

void gc_family_counts(int64_t *out) { memcpy(out, fam_count, sizeof(fam_count)); }

static int do_merge(int32_t a, int32_t b, int64_t t) {
    uint64_t k1, k2; int64_t la, lb; int32_t wa;
    signature(&items[a], &items[b], t, &k1, &k2, &la, &wa, &lb);
    int64_t g = lb - la - wa;
    if (g < 0 || (g >= MIN_GAP && !groupable(&items[a], &items[b], t))) {
        req_a = a; req_b = b; req_t = t; failed = 3; return ERR;
    }
    MEnt *m = mfind(k1, k2);
    if (!m->used) { req_a = a; req_b = b; req_t = t; return NEED_MERGE; }
    fam_count[family(&items[a])][family(&items[b])]++;
    if (family(&items[a]) == 0 && family(&items[b]) == 2 && n_dbg < 4096 && m->kind == COMP) {
        const Entry *e_ = &entries[m->id];
        int clean = e_->np == 2;
        if (clean) {
            const Piece *p0 = &pieces[e_->pbase], *p1 = p0 + 1;
            clean = p0->kind == PART && p1->kind == PART && p0->id >= 0 && p1->id >= 0 &&
                    15 * orbits[p0->id].d == -4 * orbits[p0->id].p &&
                    3 * orbits[p1->id].d == 2 * orbits[p1->id].p;
        }
        if (!clean) { dbg[2 * n_dbg] = t; dbg[2 * n_dbg + 1] = lb; n_dbg++; }
    }
    int32_t n = piece_item(m->kind, m->id, m->phase, la + m->dx, t, items[a].cL);
    if (n < 0) return ERR;
    return replace(a, b, &n, 1, t);
}

static int do_split(int32_t a, int64_t t) {
    Item *it = &items[a];
    const Entry *e = &entries[it->id];
    int32_t idx_buf[64], *idx = idx_buf;
    if (e->np > 64 && !(idx = malloc(e->np * sizeof(int32_t)))) { failed = 1; return ERR; }
    int64_t xs = it->x0;
    for (int k = 0; k < e->np; k++)
        if (pieces[e->pbase + k].id < 0) {      /* not simulated yet */
            req_a = a; req_k = k; req_t = t;
            return NEED_PIECE;
        }
    for (int k = 0; k < e->np; k++) {
        const Piece *p = &pieces[e->pbase + k];
        int64_t lo = xs + p->off;
        idx[k] = piece_item(p->kind, p->id, p->phase, lo, t, mod14(p->phL - lo - SHIFT * t));
        if (idx[k] < 0) { if (idx != idx_buf) free(idx); return ERR; }
    }
    if (e->np == 0) {                     /* vanished: just unlink */
        int32_t left = it->prev, right = it->next;
        free_item(a);
        if (left < 0) head = right; else items[left].next = right;
        if (right < 0) tail = left; else items[right].prev = left;
        if (left >= 0) return schedule_pair(left, t);
        return OK;
    }
    int r = replace(a, a, idx, e->np, t);
    if (idx != idx_buf) free(idx);
    return r;
}

/* -- rope ------------------------------------------------------------------- */

static int is_fam(const Item *it, int f) {
    return it->kind == PART && family(it) == f;
}

/* first time >= t at which fewer than thr cells separate a and b (both
   particles, a left of b), or -1 (-2: failure) */
static int64_t gap_below(const Item *a, const Item *b, int64_t t, int64_t thr) {
    int32_t pa, pb, wa, wb; int64_t la, lb;
    state(a, t, &pa, &la, &wa); state(b, t, &pb, &lb, &wb);
    const PEnt *e = pair_table(a->id, b->id, pa, pb);
    if (!e) return -2;
    int64_t G = lb - la;
    const int32_t *h = pool + e->base;
    if (G + e->hmin >= thr) {
        if (e->delta >= 0) return -1;
        int64_t D = -e->delta;
        int64_t q = (G + e->hmin - thr) / D;
        int64_t lim = (q + 1) * D - G + thr;
        for (int32_t i = 0; i < e->L; i++)
            if (h[i] < lim) return t + i + (q + 1) * e->L;
        failed = 6; return -2;
    }
    for (int32_t i = 0; i < e->L; i++)
        if (G + h[i] < thr) return t + i;
    failed = 6; return -2;
}

static uint64_t hash_ints(const int32_t *k, int32_t n) {
    uint64_t h = 0x9e3779b97f4a7c15ULL;
    for (int32_t i = 0; i < n; i++) h = mix(h ^ (uint64_t)(uint32_t)k[i]) + (uint64_t)i;
    return h;
}

static int ugrow(void) {
    UEnt *old = utab; uint64_t oc = ucap;
    ucap = oc ? 2 * oc : (1 << 12);
    utab = calloc(ucap, sizeof(UEnt));
    if (!utab) { failed = 1; return 0; }
    for (uint64_t i = 0; i < oc; i++)
        if (old[i].used) {
            uint64_t m = ucap - 1, j = old[i].h & m;
            while (utab[j].used) j = (j + 1) & m;
            utab[j] = old[i];
        }
    free(old);
    return 1;
}

static UEnt *ufind(const int32_t *k, int32_t n, uint64_t h) {
    uint64_t m = ucap - 1, j = h & m;
    while (utab[j].used) {
        if (utab[j].h == h && utab[j].klen == n &&
            !memcmp(upool + utab[j].kpos, k, n * sizeof(int32_t))) return &utab[j];
        j = (j + 1) & m;
    }
    return &utab[j];
}

static int upool_add(const int32_t *x, int64_t n, int64_t *pos) {
    if (n_upool + n > cap_upool) {
        int64_t c = cap_upool ? 2 * cap_upool : (1 << 16);
        while (c < n_upool + n) c *= 2;
        int32_t *q = realloc(upool, c * sizeof(int32_t));
        if (!q) { failed = 1; return 0; }
        upool = q; cap_upool = c;
    }
    memcpy(upool + n_upool, x, n * sizeof(int32_t));
    *pos = n_upool; n_upool += n;
    return 1;
}

/* the particle orbit/phase at left edge lo, time t, into item i */
static void set_state(int32_t i, int32_t orb, int32_t ph, int64_t lo, int64_t t) {
    Item *it = &items[i];
    const Orbit *o = &orbits[orb];
    it->kind = PART; it->id = orb; it->t0 = t - ph;
    it->x0 = lo - o_off[o->base + ph];
    it->cL = (int8_t)mod14(o_phl[o->base + ph] - lo - SHIFT * t); it->tc = t;
}

static int64_t right_edge(const Item *it, int64_t t) {
    int32_t ph, w; int64_t l;
    state(it, t, &ph, &l, &w);
    return l + w;
}

static int64_t left_edge(const Item *it, int64_t t) {
    int32_t ph, w; int64_t l;
    state(it, t, &ph, &l, &w);
    return l;
}

/* sweep the front ossifier to the end of the rope; OK, NEED_UNIT (the
   key is pending: gc_unit_request / gc_set_unit) or ERR */
static int unit_sweep(void) {
    if (!n_oss) return OK;
    Oss *o = &oss[n_oss - 1];
    while (o->prog < n_units) {
        Unit *u = &units[o->prog];
        const Item *lead = &items[o->it[o->n - 1]];
        int64_t tau = gap_below(lead, &items[u->it[0]], o->t, G_ENTRY);
        if (tau == -2) return ERR;
        if (tau < 0) { failed = 40; return ERR; }
        if (tau <= u->tlast) { req_t = tau; failed = 41; return ERR; }
        /* key: gliders then items, at tau, offsets from the unit's first item */
        int64_t ref = left_edge(&items[u->it[0]], tau);
        int32_t *k = ukey; int32_t n = 0;
        k[n++] = o->n; k[n++] = u->n;
        for (int q = 0; q < o->n + u->n; q++) {
            const Item *it = &items[q < o->n ? o->it[q] : u->it[q - o->n]];
            int32_t ph, w; int64_t l;
            state(it, tau, &ph, &l, &w);
            k[n++] = it->id; k[n++] = ph; k[n++] = (int32_t)(l - ref);
        }
        ukey_len = n;
        if (4 * (uused + 1) > 3 * ucap && !ugrow()) return ERR;
        uint64_t h = hash_ints(k, n);
        UEnt *ue = ufind(k, n, h);
        if (!ue->used) { ureq_tau = tau; ureq_ref = ref; return NEED_UNIT; }
        const int32_t *r = upool + ue->rpos;
        int64_t T = tau + ((int64_t)(uint32_t)r[0] | ((int64_t)r[1] << 32));
        int32_t ng = r[2], nu = r[3];
        if (ng != o->n || nu > UMAX || nu < 1) { failed = 42; return ERR; }
        r += 4;
        for (int q = 0; q < ng; q++, r += 3) set_state(o->it[q], r[0], r[1], ref + r[2], T);
        /* the unit's items: reuse, allocate or free item slots */
        for (int q = nu; q < u->n; q++) free_item(u->it[q]);
        for (int q = u->n; q < nu; q++) {
            int32_t i = alloc_item();
            if (i < 0) return ERR;
            items[i].prev = items[i].next = -1; items[i].ptok = 0; items[i].uid = next_tok++;
            u->it[q] = i;
        }
        u->n = nu;
        for (int q = 0; q < nu; q++, r += 3) set_state(u->it[q], r[0], r[1], ref + r[2], T);
        for (int q = 0; q < nu; q++)
            if (!is_fam(&items[u->it[q]], 2)) { failed = 43; return ERR; }
        /* the crossing must end before the lead glider nears the next unit */
        if (o->prog + 1 < n_units) {
            const Item *nx = &items[units[o->prog + 1].it[0]];
            int64_t g = left_edge(nx, T) - right_edge(&items[o->it[o->n - 1]], T);
            if (g <= G_ENTRY) { req_t = T; failed = 44; return ERR; }
        }
        u->tlast = T;
        o->t = T;
        o->prog++;
        rope_cross++;
    }
    return OK;
}

/* the left sentinel's event with the rope on: emit the front ossifier if
   due, sweep the next one, set the wake. NEED_SIDE: no ossifier in transit
   (Python pushes the train's next); NEED_UNIT: an unknown crossing. The
   event stays queued for all requests. */
static int rope_event(int32_t sen, int64_t t) {
    if (wake != INT64_MAX && t < wake) { failed = 45; return ERR; }   /* something approached */
    if (n_oss && oss[n_oss - 1].prog == n_units && oss[n_oss - 1].t == t) {
        Oss *o = &oss[n_oss - 1];
        int32_t right = items[sen].next;
        if (right >= 0 && items[right].kind != SENR &&
            left_edge(&items[right], t) - right_edge(&items[o->it[o->n - 1]], t) < MIN_GAP) {
            failed = 46; return ERR;
        }
        int32_t prev = sen;
        for (int q = 0; q < o->n; q++) {          /* link left to right */
            int32_t i = o->it[q];
            items[i].prev = prev; items[prev].next = i; prev = i;
        }
        items[prev].next = right;
        if (right >= 0) items[right].prev = prev; else tail = prev;
        n_oss--;
        wake = INT64_MAX;
        for (int q = 0; q < o->n; q++)
            if (schedule_item(o->it[q], t) != OK) return ERR;
    }
    if (!n_oss) return NEED_SIDE;
    int r = unit_sweep();
    if (r != OK) return r;
    if (oss[n_oss - 1].t < t) { failed = 47; return ERR; }       /* exit in the past */
    /* the bound follows the last unit, which crossings only move left:
       b0 - 4t/15 covers its items' right edges from now on */
    if (n_units && sen_num[0] == -4 && sen_den[0] == 15) {
        const Unit *u = &units[n_units - 1];
        int64_t b = INT64_MIN;
        for (int q = 0; q < u->n; q++) {
            const Item *it = &items[u->it[q]];
            const Orbit *o = &orbits[it->id];
            double x = (double)it->x0 + 4.0 * (double)it->t0 / 15.0 + o->hi_max;
            int64_t bq = (int64_t)x + 3;
            if (bq > b) b = bq;
        }
        if (b < sen_b0[0]) sen_b0[0] = b;
    }
    wake = oss[n_oss - 1].t;
    return schedule_pair(sen, t);
}

int32_t gc_rope_on(void) { return rope_on; }

/* rope sizes: units, ossifiers, wake, crossings, memo entries, misses */
void gc_rope_info(int64_t *out) {
    out[0] = n_units; out[1] = n_oss; out[2] = wake; out[3] = rope_cross;
    out[4] = (int64_t)uused; out[5] = rope_miss;
}

/* the pending crossing: its key (returns its length), tau and ref */
int32_t gc_unit_request(int32_t *key, int64_t *tau, int64_t *ref) {
    memcpy(key, ukey, ukey_len * sizeof(int32_t));
    *tau = ureq_tau; *ref = ureq_ref;
    return ukey_len;
}

/* its result: dt, then [n_g, n_u, (orbit, phase, offset)...] at tau + dt */
int gc_set_unit(int64_t dt, const int32_t *res, int32_t n) {
    if (4 * (uused + 1) > 3 * ucap && !ugrow()) return ERR;
    uint64_t h = hash_ints(ukey, ukey_len);
    UEnt *ue = ufind(ukey, ukey_len, h);
    if (ue->used) { failed = 48; return ERR; }
    int32_t head2[2] = { (int32_t)(uint32_t)(dt & 0xffffffff), (int32_t)(dt >> 32) };
    int64_t kpos, rpos, tmp;
    if (!upool_add(ukey, ukey_len, &kpos) || !upool_add(head2, 2, &rpos) ||
        !upool_add(res, n, &tmp)) return ERR;
    ue->h = h; ue->kpos = kpos; ue->rpos = rpos; ue->klen = ukey_len; ue->used = 1;
    uused++; rope_miss++;
    return OK;
}

/* move the n items right of the left sentinel into the rope: E particles
   into units (a new unit where the gap to the previous item is at least
   sep), groups of A gliders (closer than sep) into ossifiers ahead of all
   in transit. Python chooses n (gasc.CGas.rope_absorb). Wakes the
   sentinel now. */
int gc_rope_absorb(int64_t n, int64_t sep) {
    if (head < 0 || items[head].kind != SENL) { failed = 30; return ERR; }
    int32_t i = items[head].next;
    int64_t last_r = INT64_MIN;          /* right edge of the last E absorbed */
    int64_t last_a = INT64_MIN;          /* left edge of the last A absorbed */
    if (n_units) {
        Unit *u = &units[n_units - 1];
        last_r = right_edge(&items[u->it[u->n - 1]], now);
    }
    for (int64_t c = 0; c < n; c++) {
        if (i < 0) { failed = 31; return ERR; }
        Item *it = &items[i];
        int32_t nx = it->next;
        it->ptok = 0; it->prev = it->next = -1;      /* its events are void */
        int64_t l = left_edge(it, now);
        if (is_fam(it, 2)) {
            if (!n_units || l - last_r >= sep) {
                GROW(units, n_units, cap_units, 1);
                units[n_units].n = 0; units[n_units].tlast = 0; n_units++;
            }
            Unit *u = &units[n_units - 1];
            if (u->n == UMAX) { failed = 32; return ERR; }
            u->it[u->n++] = i;
            if (it->tc > u->tlast) u->tlast = it->tc;
            last_r = right_edge(it, now);
        } else if (is_fam(it, 0)) {
            if (!n_oss || l - last_a >= sep || oss[n_oss - 1].prog != n_units) {
                GROW(oss, n_oss, cap_oss, 1);
                oss[n_oss].n = 0; oss[n_oss].prog = n_units; oss[n_oss].t = now; n_oss++;
            }
            Oss *o = &oss[n_oss - 1];
            if (o->n == OMAX) { failed = 33; return ERR; }
            o->it[o->n++] = i;
            last_a = l;
        } else { failed = 34; return ERR; }
        i = nx;
    }
    items[head].next = i;
    if (i >= 0) items[i].prev = head; else tail = head;
    rope_on = 1;
    wake = now;
    return schedule_pair(head, now);
}

/* put a train ossifier (n gliders, left to right) behind every ossifier in
   transit; their states are valid from t */
int gc_rope_push_ossifier(int32_t n, const int32_t *id, const int64_t *t0, const int64_t *x0,
                          const int32_t *cL, int64_t t) {
    if (n > OMAX) { failed = 35; return ERR; }
    GROW(oss, n_oss, cap_oss, 1);
    memmove(oss + 1, oss, n_oss * sizeof(Oss));
    Oss *o = &oss[0];
    o->n = n; o->prog = 0; o->t = t;
    for (int q = 0; q < n; q++) {
        int32_t i = new_item(PART, id[q], t0[q], x0[q], cL[q], 0);
        if (i < 0) return ERR;
        if (!is_fam(&items[i], 0)) { failed = 36; return ERR; }
        o->it[q] = i;
    }
    n_oss++;
    return OK;
}

/* -- API ---------------------------------------------------------------------- */

int gc_reset(void) {
    free(items); items = 0; n_items = cap_items = 0;
    free_head = head = tail = -1; next_tok = next_seq = 1;
    free(orbits); orbits = 0; n_orbits = cap_orbits = 0;
    free(o_off); free(o_w); free(o_phl); free(o_phr);
    o_off = o_w = 0; o_phl = o_phr = 0; n_oarr = cap_oarr = 0;
    free(entries); entries = 0; n_entries = cap_entries = 0;
    free(e_off); free(e_w); free(e_phl); free(e_phr); free(e_lmin); free(e_rmax);
    e_off = e_w = e_lmin = e_rmax = 0; e_phl = e_phr = 0; n_earr = cap_earr = 0;
    free(pieces); pieces = 0; n_pieces = cap_pieces = 0;
    free(heap); heap = 0; n_heap = cap_heap = 0;
    free(mtab); mtab = 0; mcap = mused = 0;
    free(ptab); ptab = 0; pcap = pused = 0;
    free(pool); pool = 0; n_pool = cap_pool = 0;
    now = 0; n_events = 0; failed = 0;
    free(units); units = 0; n_units = cap_units = 0;
    free(oss); oss = 0; n_oss = cap_oss = 0; rope_on = 0; wake = INT64_MAX;
    free(utab); utab = 0; ucap = uused = 0; free(upool); upool = 0; n_upool = cap_upool = 0;
    rope_cross = rope_miss = 0; n_dbg = 0;
    memset(fam_count, 0, sizeof(fam_count));
    sen_den[0] = sen_den[1] = 1;
    return mgrow();
}

int gc_failed(void) { return failed; }
int64_t gc_now(void) { return now; }
int64_t gc_events(void) { return n_events; }
int64_t gc_heap(void) { return n_heap; }
void gc_request(int32_t *a, int32_t *b, int32_t *k, int64_t *t) {
    *a = req_a; *b = req_b; *k = req_k; *t = req_t;
}

/* item i at time t: kind, id, phase/step, left edge, width, cL */
void gc_item(int32_t i, int64_t t, int32_t *out, int64_t *left) {
    Item *it = &items[i];
    int32_t ph = 0, w = 0; int64_t l = 0;
    if (it->kind == PART || it->kind == COMP) state(it, t, &ph, &l, &w);
    out[0] = it->kind; out[1] = it->id; out[2] = ph; out[3] = w; out[4] = it->cL;
    *left = l;
}

/* piece k of entry e is now simulated: kind/id/phase */
void gc_set_piece(int32_t e, int32_t k, int32_t kind, int32_t id, int32_t phase) {
    Piece *p = &pieces[entries[e].pbase + k];
    p->kind = kind; p->id = id; p->phase = phase;
}

int32_t gc_item_entry(int32_t i) { return items[i].id; }

int32_t gc_add_orbit(int32_t p, int32_t d, const int32_t *off, const int32_t *w,
                     const int8_t *phl, const int8_t *phr) {
    if (n_orbits == cap_orbits) {
        int64_t c = cap_orbits ? 2 * cap_orbits : 256;
        Orbit *q = realloc(orbits, c * sizeof(Orbit));
        if (!q) { failed = 1; return -1; }
        orbits = q; cap_orbits = c;
    }
    if (n_oarr + p > cap_oarr) {
        int64_t c = cap_oarr ? 2 * cap_oarr : 4096;
        while (c < n_oarr + p) c *= 2;
        o_off = realloc(o_off, c * sizeof(int32_t)); o_w = realloc(o_w, c * sizeof(int32_t));
        o_phl = realloc(o_phl, c); o_phr = realloc(o_phr, c);
        if (!o_off || !o_w || !o_phl || !o_phr) { failed = 1; return -1; }
        cap_oarr = c;
    }
    Orbit *o = &orbits[n_orbits];
    o->p = p; o->d = d; o->base = (int32_t)n_oarr;
    o->v = (double)d / p;
    double lo_min = 1e300, hi_max = -1e300;
    for (int s = 0; s < p; s++) {
        o_off[n_oarr + s] = off[s]; o_w[n_oarr + s] = w[s];
        o_phl[n_oarr + s] = phl[s]; o_phr[n_oarr + s] = phr[s];
        double lin = (double)d * s / p;
        if (off[s] - lin < lo_min) lo_min = off[s] - lin;
        if (off[s] + w[s] - lin > hi_max) hi_max = off[s] + w[s] - lin;
    }
    o->lo_min = lo_min; o->hi_max = hi_max;
    n_oarr += p;
    return (int32_t)n_orbits++;
}

int32_t gc_add_entry(int32_t T, const int32_t *off, const int32_t *w,
                     const int8_t *phl, const int8_t *phr, int32_t np,
                     const int32_t *pkind, const int32_t *pid, const int32_t *pphase,
                     const int64_t *poff, const int32_t *pphl) {
    if (n_entries == cap_entries) {
        int64_t c = cap_entries ? 2 * cap_entries : 256;
        Entry *q = realloc(entries, c * sizeof(Entry));
        if (!q) { failed = 1; return -1; }
        entries = q; cap_entries = c;
    }
    int64_t need = T + 1;
    if (n_earr + need > cap_earr) {
        int64_t c = cap_earr ? 2 * cap_earr : 65536;
        while (c < n_earr + need) c *= 2;
        e_off = realloc(e_off, c * sizeof(int32_t)); e_w = realloc(e_w, c * sizeof(int32_t));
        e_phl = realloc(e_phl, c); e_phr = realloc(e_phr, c);
        e_lmin = realloc(e_lmin, c * sizeof(int32_t)); e_rmax = realloc(e_rmax, c * sizeof(int32_t));
        if (!e_off || !e_w || !e_phl || !e_phr || !e_lmin || !e_rmax) { failed = 1; return -1; }
        cap_earr = c;
    }
    if (n_pieces + np > cap_pieces) {
        int64_t c = cap_pieces ? 2 * cap_pieces : 1024;
        while (c < n_pieces + np) c *= 2;
        Piece *q = realloc(pieces, c * sizeof(Piece));
        if (!q) { failed = 1; return -1; }
        pieces = q; cap_pieces = c;
    }
    Entry *e = &entries[n_entries];
    e->T = T; e->base = (int32_t)n_earr; e->pbase = (int32_t)n_pieces; e->np = np;
    memcpy(e_off + n_earr, off, need * sizeof(int32_t));
    memcpy(e_w + n_earr, w, need * sizeof(int32_t));
    memcpy(e_phl + n_earr, phl, need); memcpy(e_phr + n_earr, phr, need);
    for (int64_t k = need - 1; k >= 0; k--) {
        int32_t l = off[k], r = off[k] + w[k];
        if (k < need - 1) {
            if (e_lmin[n_earr + k + 1] < l) l = e_lmin[n_earr + k + 1];
            if (e_rmax[n_earr + k + 1] > r) r = e_rmax[n_earr + k + 1];
        }
        e_lmin[n_earr + k] = l; e_rmax[n_earr + k] = r;
    }
    n_earr += need;
    for (int k = 0; k < np; k++) {
        Piece *p = &pieces[n_pieces + k];
        p->kind = pkind[k]; p->id = pid[k]; p->phase = pphase[k]; p->off = poff[k];
        p->phL = pphl[k];
    }
    n_pieces += np;
    return (int32_t)n_entries++;
}

/* the merge of the pending request resolves to kind/id/phase */
int gc_set_merge(int32_t kind, int32_t id, int32_t phase, int32_t dx) {
    uint64_t k1, k2; int64_t la, lb; int32_t wa;
    signature(&items[req_a], &items[req_b], req_t, &k1, &k2, &la, &wa, &lb);
    if (4 * (mused + 1) > 3 * mcap && !mgrow()) return ERR;
    MEnt *m = mfind(k1, k2);
    if (!m->used) mused++;
    m->k1 = k1; m->k2 = k2; m->kind = kind; m->id = id; m->phase = phase; m->dx = dx; m->used = 1;
    return OK;
}

/* request a materialization of side s (0: L, 1: R) now; returns the
   sentinel's bound, or the far value if that side has no sentinel */
int64_t gc_side_request(int32_t s) {
    int32_t i = s == 0 ? head : tail;
    if (i < 0 || items[i].kind != (s == 0 ? SENL : SENR))
        return s == 0 ? INT64_MIN : INT64_MAX;
    if (s == 0) { req_a = i; req_b = items[i].next; }
    else { req_a = items[i].prev; req_b = i; }
    req_t = now;
    return sen_bound(s, now);
}

/* append an item at the right end (setup, before gc_start) */
int32_t gc_append(int32_t kind, int32_t id, int64_t t0, int64_t x0, int32_t cL, int64_t tc) {
    int32_t i = new_item(kind, id, t0, x0, cL, tc);
    if (i < 0) return -1;
    items[i].prev = tail;
    if (tail < 0) head = i; else items[tail].next = i;
    tail = i;
    return i;
}

void gc_set_side(int32_t side, int64_t b0, int64_t num, int64_t den) {
    sen_b0[side] = b0; sen_num[side] = num; sen_den[side] = den;
}

int gc_start(void) {
    for (int32_t i = head; i >= 0; i = items[i].next)
        if (schedule_item(i, now) != OK) return ERR;
    return OK;
}

/* the pending sentinel request: replace the sentinel (req_a or req_b) by
   n new items given as arrays (sentinel first for L, last for R) */
int gc_materialize(int32_t n, const int32_t *kind, const int32_t *id, const int64_t *t0,
                   const int64_t *x0, const int32_t *cL) {
    int32_t sen = items[req_a].kind == SENL ? req_a : req_b;
    int32_t *idx = malloc(n * sizeof(int32_t));
    if (!idx) { failed = 1; return ERR; }
    for (int k = 0; k < n; k++) {
        idx[k] = new_item(kind[k], id[k], t0[k], x0[k], cL[k], 0);   /* untouched rows */
        if (idx[k] < 0) { free(idx); return ERR; }
    }
    int r = replace(sen, sen, idx, n, req_t);
    free(idx);
    return r;
}

/* process events up to time T; returns OK (now = T), NEED_MERGE or
   NEED_SIDE (gc_request tells which; the event stays queued), or ERR */
int gc_advance(int64_t T) {
    while (n_heap && heap[0].t <= T) {
        Event e = heap[0];
        Item *a = &items[e.a];
        int valid = e.kind == EV_S ? (a->kind == COMP && a->uid == e.tok)
                                   : (a->kind != DEAD && a->ptok == e.tok && a->next == e.b);
        /* a rope emission relinks the sentinel's neighbour before a request
           may interrupt the event: only its token counts */
        if (e.kind == EV_M && rope_on && a->kind == SENL && a->ptok == e.tok) valid = 1;
        if (!valid) { pop(); continue; }
        now = e.t;
        int r;
        if (e.kind == EV_M && rope_on && a->kind == SENL) {
            req_a = e.a; req_b = e.b; req_t = e.t;
            int r = rope_event(e.a, e.t);
            if (r == NEED_UNIT || r == NEED_SIDE) return r;
            if (r != OK) return ERR;
            pop();
            n_events++;
            continue;
        }
        if (e.kind == EV_M) {
            req_a = e.a; req_b = e.b; req_t = e.t;
            pop();
            /* the replacement reschedules; if Python does not call
               gc_materialize the pair is lost, so it must */
            return NEED_SIDE;
        }
        if (e.kind == EV_C) r = do_merge(e.a, e.b, e.t);
        else r = do_split(e.a, e.t);
        if (r == NEED_MERGE || r == NEED_PIECE) return r;   /* event stays queued */
        if (r != OK) return ERR;
        /* new events are never earlier, and at equal time come later
           (larger seq): the processed event is still at the top */
        pop();
        n_events++;
    }
    now = T;
    return OK;
}

/* items overlapping [lo, hi) at time now, walking from the right end:
   out arrays get kind, id, phase/step, left edge, width, cL; returns the
   count (at most max), or -1 if more */
int64_t gc_list(int64_t lo, int64_t hi, int64_t max, int32_t *kind, int32_t *id,
                int32_t *phase, int64_t *left, int32_t *width, int32_t *cL, int64_t *tc) {
    int32_t i = tail;
    /* walk left to the first item whose right edge < lo */
    while (i >= 0) {
        Item *it = &items[i];
        if (it->kind == SENL) break;
        if (it->kind != SENR) {
            int32_t ph, w; int64_t l;
            state(it, now, &ph, &l, &w);
            if (l + w <= lo) break;
        }
        i = it->prev;
    }
    int32_t j = i < 0 ? head : i;
    int64_t n = 0;
    for (; j >= 0; j = items[j].next) {
        Item *it = &items[j];
        int32_t ph = 0, w = 0; int64_t l;
        if (it->kind == SENL) l = sen_bound(0, now);
        else if (it->kind == SENR) l = sen_bound(1, now);
        else state(it, now, &ph, &l, &w);
        if (n == max) return -1;
        kind[n] = it->kind; id[n] = it->id; phase[n] = ph; left[n] = l; width[n] = w;
        cL[n] = it->cL; tc[n] = it->tc;
        n++;
        if (it->kind != SENL && l >= hi) break;
        if (it->kind == SENR) break;
    }
    return n;
}

/* all items in order: kind, id, cL (int32 x3 per item), t0, x0, tc (int64 x3) */
int64_t gc_dump(int64_t max, int32_t *small, int64_t *big) {
    int64_t n = 0;
    for (int32_t i = head; i >= 0; i = items[i].next) {
        if (n == max) return -1;
        small[3 * n] = items[i].kind; small[3 * n + 1] = items[i].id;
        small[3 * n + 2] = items[i].cL;
        big[3 * n] = items[i].t0; big[3 * n + 1] = items[i].x0; big[3 * n + 2] = items[i].tc;
        n++;
    }
    return n;
}

void gc_set_now(int64_t t) { now = t; }

int64_t gc_count(void) {
    int64_t n = 0;
    for (int32_t i = head; i >= 0; i = items[i].next) n++;
    return n;
}
