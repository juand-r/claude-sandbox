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
#define MARGIN 256
#define TILE 14
#define SHIFT 4

enum { DEAD = 0, PART = 1, COMP = 2, SENL = 3, SENR = 4 };
enum { EV_C = 0, EV_M = 1, EV_S = 2 };
enum { OK = 0, NEED_MERGE = 1, NEED_SIDE = 2, NEED_PIECE = 3, ERR = -1 };

typedef struct {
    int64_t t0, x0;
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
static int64_t n_earr, cap_earr;
static Piece *pieces; static int64_t n_pieces, cap_pieces;
static Event *heap; static int64_t n_heap, cap_heap;
static int64_t now;
static int64_t n_events;
static int64_t sen_b0[2], sen_num[2], sen_den[2];
static int failed;

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

/* first time >= t with fewer than MIN_GAP cells between a and b, or -1 */
static int64_t collision(const Item *a, const Item *b, int64_t t) {
    int64_t ea = end_of(a), eb = end_of(b);
    if (a->kind == PART && b->kind == PART) {
        const Orbit *oa = &orbits[a->id], *ob = &orbits[b->id];
        int64_t L = oa->p / gcd64(oa->p, ob->p) * ob->p;
        int64_t delta = ob->d * (L / ob->p) - oa->d * (L / oa->p);
        int32_t pa, pb, wa, wb; int64_t la, lb;
        state(a, t, &pa, &la, &wa); state(b, t, &pb, &lb, &wb);
        int64_t best = -1;
        int64_t ka = 0, kb = 0;          /* periods completed since t */
        for (int64_t i = 0; i < L; i++) {
            int32_t sa = (int32_t)((pa + i) % oa->p), sb = (int32_t)((pb + i) % ob->p);
            int64_t xa = la - o_off[oa->base + pa] + ((pa + i) / oa->p) * oa->d + o_off[oa->base + sa];
            int64_t xb = lb - o_off[ob->base + pb] + ((pb + i) / ob->p) * ob->d + o_off[ob->base + sb];
            int64_t g = xb - xa - o_w[oa->base + sa];
            int64_t tt;
            if (g < MIN_GAP) tt = i;
            else if (delta >= 0) continue;
            else tt = i + ((g - MIN_GAP) / (-delta) + 1) * L;
            if (best < 0 || tt < best) best = tt;
        }
        (void)ka; (void)kb; (void)wb;
        return best < 0 ? -1 : t + best;
    }
    int64_t horizon = ea < eb ? ea : eb;
    int64_t n = horizon - t + 1;
    int32_t ph; int64_t la, lb; int32_t wa, wb;
    state(a, t, &ph, &la, &wa); state(b, t, &ph, &lb, &wb);
    if (lb - la - wa >= MIN_GAP + 2 * n) return -1;     /* light cone */
    for (int64_t i = 0; i < n; i++) {
        state(a, t + i, &ph, &la, &wa); state(b, t + i, &ph, &lb, &wb);
        if (lb - la - wa < MIN_GAP) return t + i;
    }
    return -1;
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
        double lin = (double)(l - o_off[o->base + ph]);
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
    if (gap <= 0) return t;
    if (closing <= 0) return -1;
    int64_t tc = t + (int64_t)(gap / closing);
    if (end >= 0 && tc > end) return -1;
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

static int schedule_pair(int32_t a, int64_t t) {
    Item *ia = &items[a];
    int32_t b = ia->next;
    if (b < 0 || ia->kind == SENR) return OK;
    ia->ptok = next_tok++;
    Item *ib = &items[b];
    int64_t tc; int kind;
    if (ia->kind == SENL || ib->kind == SENR) {
        if (ia->kind == SENL && ib->kind == SENR) { failed = 2; return ERR; }
        tc = sentinel_time(ia, ib, t); kind = EV_M;
    } else { tc = collision(ia, ib, t); kind = EV_C; }
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

static int32_t new_item(int kind, int32_t id, int64_t t0, int64_t x0, int cL) {
    int32_t i = alloc_item();
    if (i < 0) return -1;
    Item *it = &items[i];
    it->kind = (int8_t)kind; it->id = id; it->t0 = t0; it->x0 = x0;
    it->cL = (int8_t)cL; it->ptok = 0; it->uid = next_tok++;
    it->prev = it->next = -1;
    return i;
}

static inline int mod14(int64_t x) { int r = (int)(x % TILE); return r < 0 ? r + TILE : r; }

/* item for a piece of kind/id/phase at left edge lo, time t */
static int32_t piece_item(int kind, int32_t id, int32_t phase, int64_t lo, int64_t t, int cL) {
    if (kind == PART) {
        const Orbit *o = &orbits[id];
        return new_item(PART, id, t - phase, lo - o_off[o->base + phase], cL);
    }
    return new_item(COMP, id, t, lo, cL);
}

static void signature(const Item *a, const Item *b, int64_t t, uint64_t *k1, uint64_t *k2,
                      int64_t *la, int32_t *wa, int64_t *lb) {
    int32_t pa, pb, wb;
    state(a, t, &pa, la, wa); state(b, t, &pb, lb, &wb);
    int64_t g = *lb - *la - *wa;
    *k1 = ((uint64_t)a->kind << 62) | ((uint64_t)(uint32_t)a->id << 30) | (uint64_t)pa;
    *k2 = ((uint64_t)b->kind << 62) | ((uint64_t)(uint32_t)b->id << 30) | ((uint64_t)pb << 2)
          | (uint64_t)(g & 3);
}

static int do_merge(int32_t a, int32_t b, int64_t t) {
    uint64_t k1, k2; int64_t la, lb; int32_t wa;
    signature(&items[a], &items[b], t, &k1, &k2, &la, &wa, &lb);
    int64_t g = lb - la - wa;
    if (g < 0 || g >= MIN_GAP) { failed = 3; return ERR; }
    MEnt *m = mfind(k1, k2);
    if (!m->used) { req_a = a; req_b = b; req_t = t; return NEED_MERGE; }
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

/* -- API ---------------------------------------------------------------------- */

int gc_reset(void) {
    free(items); items = 0; n_items = cap_items = 0;
    free_head = head = tail = -1; next_tok = next_seq = 1;
    free(orbits); orbits = 0; n_orbits = cap_orbits = 0;
    free(o_off); free(o_w); free(o_phl); free(o_phr);
    o_off = o_w = 0; o_phl = o_phr = 0; n_oarr = cap_oarr = 0;
    free(entries); entries = 0; n_entries = cap_entries = 0;
    free(e_off); free(e_w); free(e_phl); free(e_phr);
    e_off = e_w = 0; e_phl = e_phr = 0; n_earr = cap_earr = 0;
    free(pieces); pieces = 0; n_pieces = cap_pieces = 0;
    free(heap); heap = 0; n_heap = cap_heap = 0;
    free(mtab); mtab = 0; mcap = mused = 0;
    now = 0; n_events = 0; failed = 0;
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
        if (!e_off || !e_w || !e_phl || !e_phr) { failed = 1; return -1; }
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

/* append an item at the right end (setup, before gc_start) */
int32_t gc_append(int32_t kind, int32_t id, int64_t t0, int64_t x0, int32_t cL) {
    int32_t i = new_item(kind, id, t0, x0, cL);
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
        idx[k] = new_item(kind[k], id[k], t0[k], x0[k], cL[k]);
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
        if (!valid) { pop(); continue; }
        now = e.t;
        int r;
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
                int32_t *phase, int64_t *left, int32_t *width, int32_t *cL) {
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
        cL[n] = it->cL;
        n++;
        if (it->kind != SENL && l >= hi) break;
        if (it->kind == SENR) break;
    }
    return n;
}

int64_t gc_count(void) {
    int64_t n = 0;
    for (int32_t i = head; i >= 0; i = items[i].next) n++;
    return n;
}
