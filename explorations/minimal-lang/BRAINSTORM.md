# Brainstorm: Language at the Level of Thinking

## The Core Insight

Humans are slow at programming not because they think slowly, but because
languages operate at the wrong level of abstraction. There's a gap between
*what you mean* and *what you have to write*. That gap is boilerplate.

An LLM bridges that gap -- it translates intent into ceremony. But what if
the language itself operated at the level of intent?

**The language should work at the level of abstraction as thinking.**

## Where Does the Friction Come From?

Every time you think "I want X" and then spend 10 minutes writing the
mechanical translation of X, that's friction. Let's catalog it:

### Friction Type 1: "I know WHAT, but the language wants HOW"

You think: "sort users by age"
You write: import, loop or stream setup, comparator, collection, return

You think: "save this to the database"
You write: ORM config, model definition, migration, repository class, session management

You think: "make this available over HTTP"
You write: framework choice, routing, controller, serialization, middleware, error mapping

The human already *knows* the what. The language demands the how. Every time.

### Friction Type 2: "I already said this"

You defined a User with name, age, email. Now you need to:
- Write a constructor (you already said what the fields are)
- Write serialization (you already said the structure)
- Write validation (the types already imply constraints)
- Write a form (the fields already define the shape)
- Write a database schema (you already said it)

You said it ONCE. The language makes you say it FIVE TIMES in five formats.
This is the DRY violation at the language level.

### Friction Type 3: "This is obvious, but the compiler insists"

- Importing `json` before using `json.parse()` -- where else would it come from?
- Declaring a variable's type when it's assigned `"hello"` on the same line
- Wrapping every call in try/catch when you'd just propagate anyway
- Writing `async/await` when the runtime could figure out the dependency graph
- Annotating `@Override` -- what else would it be?

### Friction Type 4: "Every project starts the same way"

Before writing ANY logic, you need:
- Project structure (src/, tests/, config/)
- Build tool configuration
- Dependency management setup
- Entry point boilerplate (main function, app initialization)
- Testing framework setup

You haven't expressed a single thought yet and you've already made 50 decisions.

### Friction Type 5: "I'm repeating a pattern the language doesn't see"

The 15th REST endpoint. The 10th form handler. The 8th database query wrapper.
You can see the pattern. The language can't. So you either:
- Copy-paste and modify (error-prone)
- Write a meta-abstraction (over-engineering)
- Use code generation (leaves the language)

None of these are good.

---

## What Would "Thinking-Level" Code Look Like?

Let me try to write what a human *thinks* vs what they currently *write*:

### Example 1: A web app for a bookstore

**What you think:**
- A Book has a title, author, price, and genre
- Users can browse books, search, add to cart, and buy
- There's an admin who can add/edit books

**What you currently write:** 500+ lines across 15+ files.

**What you SHOULD write:**
```
Book = { title, author, price: Money, genre }
User = { name, email, cart: [Book] }

-- browsing
books |> where(.genre == genre) |> sort(.title)
books |> where(.title ~ query or .author ~ query)

-- cart
user.cart.add(book)
user.cart.total = sum(.price)

-- admin
admin can add, edit, remove books
```

Is that real code? Not yet. But the question is: *why can't it be?*
What's actually stopping us from making that executable?

### Example 2: CLI tool that processes CSV files

**What you think:**
- Read a CSV
- Filter rows where column X > some value
- Group by column Y
- Output summary

**What you should write:**
```
data = read("input.csv")
data |> where(.revenue > 1000) |> group(.region) |> summarize(
    count,
    total: sum(.revenue),
    avg: mean(.revenue),
)
```

This isn't far from what pandas/dplyr do. But those are LIBRARIES bolted
onto languages. Why isn't this the language itself?

### Example 3: A background job that runs every hour

**What you think:**
- Every hour, fetch new data from an API
- Compare to what we have
- Update the differences
- Notify if anything important changed

**What you should write:**
```
every 1.hour:
    new_data = fetch("https://api.example.com/data")
    changes = diff(new_data, stored_data)
    store(new_data)
    if changes.any(.important):
        notify(admin, "Important changes: {changes}")
```

No cron config. No job queue library. No daemon setup. You said "every hour"
and it happens.

---

## Key Design Ideas Emerging

### 1. Declaration = Implementation

When you declare a data type, you've ALSO declared its constructor, serialization,
equality, database schema, and API shape. One declaration, all derived forms.
You only write custom behavior for the exceptions.

### 2. The Compiler Fills In the Obvious

If the compiler can figure it out, you shouldn't write it. Types, imports,
error propagation, memory management, concurrency -- all inferred unless
you override.

### 3. Patterns Are First-Class

If you find yourself writing the same shape of code, you should be able to
name that shape and reuse it without dropping into macro-land or code gen.

```
-- maybe something like this?
pattern crud(T) =
    serve "/[T]s" -> all(T)
    serve "/[T]s/:id" -> find(T, id)
    serve "/[T]s" method:post -> create(T, body)
    serve "/[T]s/:id" method:put -> update(T, id, body)
    serve "/[T]s/:id" method:delete -> remove(T, id)

-- then just:
crud(Book)
crud(User)
```

### 4. The Language IS the Framework

No separate web framework, ORM, test runner, task scheduler. These are
language features. Not because the language is bloated, but because these
are *universal patterns* that every real program needs.

Or more precisely: the language provides the *verbs* (serve, store, test,
schedule, notify) and pluggable backends provide the implementation.

### 5. Progressive Disclosure of Complexity

- Simple things should be 1-3 lines
- Medium things should be 10-20 lines
- Complex things should be possible, with full control
- You should never hit a wall where the abstraction breaks and you have
  to rewrite everything at a lower level

---

## The Hard Questions

1. **Is this even a "programming language" anymore?** Or is it a specification
   language with an execution engine? Maybe the line is blurry and that's fine.

2. **Where does "intent" end and "logic" begin?** `sort users by age` is intent.
   A custom sorting algorithm is logic. The language needs to handle both.
   The boundary matters.

3. **How do you debug magic?** When the compiler fills in the obvious, and
   something goes wrong in the filled-in part, how does the human diagnose it?
   This is the perennial problem with "smart" languages.

4. **Can you be general-purpose AND this concise?** Domain-specific languages
   achieve this conciseness within their domain. Doing it across all domains
   might be impossible. Or it might require a different architecture -- maybe
   the core is tiny and "domain packs" extend it with the right verbs?

5. **Will experienced programmers trust it?** "The compiler figures it out"
   makes experts nervous. They want control. The escape hatches need to be
   good enough that experts feel safe.

---

## Possible Name Ideas (just riffing)

- **Say** (you say what you mean)
- **Mean** (say what you mean, mean what you say)
- **Min** (minimal)
- **Just** (just do it)
- **Intent**
- **So** (and so it is)
- **Hence**
