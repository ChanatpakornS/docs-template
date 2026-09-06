# Go Standards

Load this file when creating or modifying `.go` files.

## Formatting

- Code must be `gofmt`-clean; run `goimports` to order imports (stdlib, then third-party, then local, separated by blank lines).
- Indent with tabs. Do not hand-align; let the formatter decide.
- One package per directory. Package name matches the directory, lower-case, no underscores.

## Naming

- Exported identifiers get doc comments starting with the identifier name.
- Acronyms keep a consistent case: `userID`, `HTTPClient`, `parseURL`.
- Keep names short in small scopes (`i`, `r`, `buf`); grow them with scope.
- No stutter: `http.Server`, not `http.HTTPServer`.

## Pass-by-reference guidelines

- Slices, maps, channels, and function values are already reference-like — pass them directly, do not take their address.
- Pass a pointer when the callee must mutate the caller's value, when the struct is large enough that copying matters, or when the type contains a `sync` primitive (`sync.Mutex`, `sync.WaitGroup`) that must not be copied.
- Pass small, immutable structs by value — it is clearer and avoids nil checks.
- Be consistent within a type: if one method has a pointer receiver, all of them should.
- Return values, not out-params. Reserve pointer params for genuine mutation.

## Error handling

- Return errors, do not panic. Panics are for programmer bugs and truly unrecoverable states, never for expected failure.
- Wrap with context as errors propagate: `fmt.Errorf("load config %s: %w", path, err)`. Use `%w` so callers can `errors.Is` / `errors.As`.
- Define sentinel errors (`var ErrNotFound = errors.New("not found")`) for conditions callers branch on.
- Handle an error once: either handle it or return it, not both (do not log-and-return).
- Check every error. If deliberately ignoring one, assign to `_` with a comment saying why.

## Context

- `context.Context` is the first parameter, named `ctx`. Never store it in a struct.
- Pass `ctx` down every call that does I/O or blocking work; honour cancellation.

## Concurrency

- The goroutine that creates a channel owns closing it.
- Guard shared state with a mutex or confine it to one goroutine; run tests with `-race`.

## Testing

- Table-driven tests with subtests (`t.Run`). Name cases by behaviour.
- Use `t.Helper()` in assertion helpers.
- Prefer the stdlib `testing` package; add a matcher library only if the project already uses one.
- Test exported behaviour through the package's public API where practical.
