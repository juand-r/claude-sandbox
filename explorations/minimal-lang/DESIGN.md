# Minimal-Lang Design Document

## The Thesis

Most programming languages were designed for humans typing code. But increasingly,
code is *generated* (by LLMs) and *reviewed* (by humans). This changes the design
tradeoffs:

- **Verbosity for clarity** was worth it when humans typed and read. Now verbosity
  costs tokens (money, latency) on the generation side and cognitive load on the
  review side.
- **Boilerplate for safety** (type annotations, error handling) made sense when
  humans were unreliable. LLMs are *differently* unreliable -- they're great at
  boilerplate but bad at subtle logic. So the language should make logic clear
  and automate the rest.

## Boilerplate Catalog

Here's what eats lines in real codebases, ranked by how "accidental" vs "essential"
the ceremony is:

### 1. Data definitions (HIGH accidental ceremony)
```java
// Java: 30+ lines for a simple data holder
public class User {
    private final String name;
    private final int age;
    private final String email;

    public User(String name, int age, String email) {
        this.name = name;
        this.age = age;
        this.email = email;
    }

    public String getName() { return name; }
    public int getAge() { return age; }
    public String getEmail() { return email; }

    @Override
    public boolean equals(Object o) { ... }
    @Override
    public int hashCode() { ... }
    @Override
    public String toString() { ... }
}
```
Even Kotlin's `data class User(val name: String, val age: Int, val email: String)`
still requires explicit types when they could often be inferred from usage.

### 2. Error handling (MEDIUM accidental ceremony)
```go
// Go: error checking after every call
result, err := doThing()
if err != nil {
    return fmt.Errorf("doing thing: %w", err)
}
result2, err := doOtherThing(result)
if err != nil {
    return fmt.Errorf("doing other thing: %w", err)
}
```
Rust's `?` operator was a big improvement. But we can go further.

### 3. Import/module boilerplate (MEDIUM accidental ceremony)
```python
from collections import defaultdict
from typing import List, Dict, Optional
from pathlib import Path
import json
import os
```
Why do I need to declare that I'm using `json.loads()`? The name is unambiguous.

### 4. Iteration/transformation patterns (LOW-MEDIUM)
```python
# Filtering, mapping, collecting -- so common, so verbose
results = []
for item in items:
    if item.is_valid():
        results.append(item.transform())
```
vs. `items |> filter(.valid) |> map(.transform)` -- pipes + shorthand accessors.

### 5. Null/optional handling (MEDIUM)
```kotlin
val name = user?.profile?.displayName ?: user?.username ?: "Anonymous"
```
This is actually not bad in Kotlin. But the *need* to think about null at every
step is the real problem. What if nullability were handled structurally?

### 6. Async/concurrency ceremony (HIGH)
```javascript
const result = await fetch(url);
const data = await result.json();
const processed = await Promise.all(data.map(async (item) => {
    const detail = await fetch(item.url);
    return await detail.json();
}));
```
What if *everything* could be concurrent by default and the runtime figures it out?

### 7. Type declarations (MEDIUM -- controversial)
Full inference like Haskell? Too hard to read. Full declaration like Java? Too verbose.
The sweet spot: infer locally, declare at boundaries.

---

## Design Principles

1. **Defaults should be the common case.** Immutable by default. Public by default
   (most code isn't a library). Concurrent by default. Errors propagate by default.

2. **Names are enough.** If a name unambiguously refers to something, don't require
   an import or declaration. Auto-resolve.

3. **Structure over ceremony.** Data is just named tuples. No getters/setters/constructors.
   Pattern matching replaces most conditional logic.

4. **Pipelines over nesting.** `a |> b |> c` instead of `c(b(a))`. Data flows
   left to right like reading.

5. **Errors are values, but quiet ones.** Like Rust's `?` but even more implicit.
   Failed operations produce typed error values that propagate unless handled.

6. **Types exist to help, not hinder.** Inferred within functions. Required at
   function signatures (the "boundary" principle). Structural, not nominal.

---

## Syntax Sketch (very early)

```
-- A function. Types inferred internally, declared at boundaries.
fetch_user(id: Int) -> User | NotFound =
    row = db.query("SELECT * FROM users WHERE id = ?", id)?
    User(name: row.name, age: row.age, email: row.email)

-- Data type. That's it. Equality, hashing, printing: automatic.
User = { name: Str, age: Int, email: Str }

-- Pipeline processing
active_users =
    db.query("SELECT * FROM users")?
    |> filter(.active)
    |> sort_by(.name)
    |> map(.email)

-- Pattern matching replaces if/else chains
describe(user: User) -> Str =
    match user.age
        0..17  -> "minor"
        18..64 -> "adult"
        _      -> "senior"

-- Concurrency: just call things. Runtime parallelizes independent operations.
(profile, posts, friends) = (
    fetch_profile(id),
    fetch_posts(id),
    fetch_friends(id),
)

-- Error handling: ? propagates, or handle inline
name = fetch_user(id)?.name or "Anonymous"
```

## What This Is NOT

- Not a "natural language" programming language. Code should be precise.
- Not dynamically typed. Types exist, they're just inferred where possible.
- Not a DSL. It should be general-purpose.

---

## Open Design Questions

1. **How far to push auto-imports?** Module system still needed for namespacing,
   but maybe you never write `import` explicitly?

2. **Metaprogramming?** Macros add power but also confusion. Maybe a restricted
   form (like Zig's comptime)?

3. **FFI story?** If this transpiles to another language, interop is easier.
   Transpile target: Rust? Go? JS? All three?

4. **Memory model?** GC (simpler) vs ownership (safer)? For an LLM-era language,
   GC might be the right call -- ownership is exactly the kind of thing LLMs
   get wrong.

5. **Concurrency model?** Implicit parallelism is appealing but hard. Maybe
   structured concurrency (like Trio/Kotlin coroutines) with less syntax?
