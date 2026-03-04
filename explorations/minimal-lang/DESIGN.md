# Design: A Language of Intent

## The Layers of Intent

When a human thinks about a program, they think at multiple layers:

```
Layer 4 (highest):  "Users can buy books"
Layer 3:            "A user has a cart; adding to cart, checking out"
Layer 2:            "POST /checkout validates cart, charges payment, creates order"
Layer 1:            "Serialize cart to JSON, call Stripe API, insert row, send email"
Layer 0 (lowest):   "Allocate buffer, format bytes, open socket, write..."
```

Most languages force you to work at layers 0-2, even when you're *thinking*
at layers 3-4. The friction is the constant translation downward.

**Key principle: the language should let you express intent at the highest
layer that's sufficient, and only force you down when you need to override
something specific.**

Most of the time, layer 3 is enough. Sometimes you need layer 2 for custom
logic. Rarely do you need layer 1. Almost never layer 0.

## What Goes in Each Layer

### Layer 4: Domain Declaration

This is where you name what exists and how it relates.

```
domain Bookstore:
    Book = { title, author, price: Money, genre }
    User = { name, email, cart: [Book] }
    Order = { user: User, items: [Book], total: Money, placed: Time }

    -- relationships
    User browses, searches, buys Book
    User has many Order
```

This isn't executable yet. It's a *domain model*. But from this, the system
can already derive:
- Database tables and relationships
- Basic types and constructors
- Serialization for all of these
- A default API shape (CRUD for each entity)

You haven't written a single function. You've just said what things ARE.

### Layer 3: Behavior (Intent-Level)

This is where you say what happens, without specifying mechanism.

```
when User buys:
    validate cart is not empty
    charge user for cart.total
    create Order from cart
    clear cart
    notify user of Order
```

This reads like a checklist. Each line is an *intent* that maps to a
well-known operation:
- `validate X` = check a condition, fail if not met
- `charge user for amount` = invoke payment (pluggable backend)
- `create X from Y` = construct and persist
- `notify user of X` = send notification (pluggable backend)

The system knows HOW to do each of these because they're standard verbs
with pluggable implementations. You configure the backend once:

```
payments: Stripe { key: env.STRIPE_KEY }
notifications: Email { smtp: env.SMTP_URL }
storage: Postgres { url: env.DATABASE_URL }
```

And the verbs just work.

### Layer 2: Logic (Where Humans Add Value)

This is where you write actual logic -- but ONLY the logic that's unique
to your problem. No wiring, no plumbing.

```
-- Custom pricing logic (this is where human thinking matters)
discount(user, book) =
    | user.is_member and book.price > 20  -> 0.15
    | user.orders.count > 10              -> 0.10
    | else                                -> 0

final_price(user, book) =
    book.price * (1 - discount(user, book))
```

This is pure logic. No imports, no classes, no dependency injection.
Just the decision tree that represents business rules.

### Layer 1: Override (Rarely Needed)

When the defaults aren't right, you reach down and specify:

```
-- Custom serialization for a weird external API
serialize Order for legacy_api:
    { "ord_id": .id, "itm_count": .items.length, "amt_cents": .total.cents }

-- Custom query when the generated one is too slow
find_popular_books(genre, limit) =
    sql"SELECT * FROM books WHERE genre = {genre}
        ORDER BY sales_count DESC LIMIT {limit}"
```

You're not writing this for everything -- just for the exceptions where
the system's default isn't good enough.

## The Core Mechanism: Derive Unless Overridden

The principle that ties it together:

**Everything is derived from the highest-level declaration, unless explicitly
overridden at a lower level.**

```
Book = { title, author, price: Money, genre }
```

From this single line, the system derives:

| Derived thing       | How                                  | Override? |
|---------------------|--------------------------------------|-----------|
| Constructor         | `Book("Dune", "Herbert", 9.99, :sf)` | Rarely    |
| Equality            | All fields compared                  | Sometimes |
| Database table      | `books(title, author, price, genre)` | Sometimes |
| JSON serialization  | `{"title":..., "author":...}`        | Sometimes |
| API endpoints       | `GET/POST/PUT/DELETE /books`          | Often     |
| Validation          | Non-null, type-correct               | Often     |
| Display/formatting  | `"Book(title, author)"`              | Often     |

"Rarely/sometimes/often" indicates how frequently you'd actually need to
override the default. The system should get the common case right so you
only write code for the uncommon case.

## Verbs as Language Primitives

Instead of importing frameworks, the language has built-in *verbs* that
represent universal operations:

```
serve     -- expose over HTTP/RPC
store     -- persist to storage
fetch     -- retrieve from external source
notify    -- send notification
schedule  -- run on a schedule
validate  -- check constraints
transform -- convert between shapes
test      -- assert behavior
```

Each verb has a pluggable backend. `serve` might use HTTP today and gRPC
tomorrow. `store` might use Postgres or SQLite or S3. You don't care at
the intent level.

This is not the language being bloated. These verbs are as fundamental to
real programs as `if` and `for`. Every nontrivial program serves, stores,
fetches, or notifies. We just pretend these are "library concerns" and
force everyone to wire them up from scratch.

## What the Human Writes vs. What the System Derives

For a complete bookstore app:

**Human writes (~50 lines):**
- Domain model (entities, relationships)
- Behavior descriptions (what happens when)
- Business logic (pricing, discounts, recommendations)
- Configuration (which backends to use)

**System derives (~5000 lines equivalent):**
- Database schema + migrations
- API endpoints + routing
- Serialization/deserialization
- Input validation
- Error handling and propagation
- Authentication/authorization plumbing
- Logging and monitoring hooks
- Test scaffolding

That's a 100:1 ratio. The human writes ONLY the parts that require
human judgment. The rest is mechanical and derivable.

## Open Questions

1. **How do you learn what the system derived?** You need to be able to
   inspect the generated behavior. Maybe: `explain Book.store` shows you
   the derived SQL. `explain checkout` shows the full expanded behavior.

2. **Type system:** How much type machinery do you expose? The declaration
   `price: Money` implies types, but do you need generics? Unions?
   Probably yes, but the syntax should stay close to natural expression.

3. **Error model:** "validate cart is not empty" -- what happens when it
   fails? The system needs a sensible default (return error to caller)
   with override capability (custom error messages, recovery logic).

4. **Testing:** If the system derives most code, what do humans test?
   Probably: business logic (layer 2) and integration behavior (layer 3).
   The derived code (layer 1) should be tested by the system itself.

5. **Escape hatch to what?** When you need layer 0 control, what do you
   drop into? Raw Rust? WASM? Some lower-level subset of the language?
   This matters a lot for adoption.
