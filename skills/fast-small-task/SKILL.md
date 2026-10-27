---
name: fast-small-task
description: Deliver a small, low-risk change in an existing codebase with the minimum edit and targeted verification, then hand off to fast-small-review. Use for a single page, component, module, copy, style, config value or simple bug fix ("hide this button", "change this message", "fix this off-by-one, run only the related test"). Not for large features, refactors, migrations or cross-service changes.
---

# Fast Small Task

## Goal

Deliver a small change completely and quickly without giving up basic correctness. Keep investigation and verification
narrow; do not turn a small change into a full development workflow.

## Is it small?

Treat the request as small when all of these hold:

- it touches one clear page, component, module or script;
- it needs no database migration, new domain model, cross-service protocol or large refactor;
- it can be verified by a focused test, a static check or a precise manual check.

If it touches several independent modules, a public API or protocol, build configuration, shared data structures, or is
a complex new feature, say so plainly and switch to the host's normal development workflow. Never force this flow on a
change it does not fit.

## Workflow

1. **Read the rules that apply.** Only the `AGENTS.md`, `CLAUDE.md`, contributing guide and test conventions that cover
   the paths you will touch. Keep the user's uncommitted changes intact.
2. **Locate fast.** Use `rg` / `rg --files` (or the host's search tool) and small reads to find the entry point, its
   callers and the directly related tests. No aimless browsing of the whole repository.
3. **State scope and assumptions once.** Act on what the code makes clear. Ask only about ambiguity that would change
   the approach, the blast radius or safety. Before editing, say in one sentence what you will change and what you
   assume.
4. **Make the minimum edit.** Change only what the request needs, reuse the patterns already in the file, and use the
   host's local edit tool (`apply_patch`, `Edit` or equivalent). No drive-by refactors, renames or formatting.
5. **Verify precisely** (see the matrix below). Always run `git diff --check`. If no test exists, it is too expensive to
   start or it is flaky, use the smallest meaningful check and say what you did not run.
6. **Escalate only on evidence.** Widen the tests or run a build only when the change touched a shared component,
   utility, route, protocol, cross-page state, build config, dependency or data structure, or when a focused test fails
   and the change may be the cause.
7. **Review by default.** When the change is done and verified, run `fast-small-review` on it and pass the task context
   below, unless the user asked to skip review, the task is unfinished, or it was escalated to a full workflow.
8. **Report.** What changed, what behaviour was deliberately kept, which checks ran and which did not, the review result
   and any known risk. If review finds issues, report them; do not fix them inside this flow.

## Verification matrix

Pick the smallest check that actually covers the change. Never default to the full suite.

| Change | Minimum check |
| --- | --- |
| Copy, CSS, JSON, YAML, Markdown | `git diff --check`; the project's formatter or schema check if it has one |
| JS / TS | affected test file filtered by name (`vitest -t`, `jest -t`), lint and typecheck of the changed files |
| Python | `pytest path/to/test_file.py -k name`, the project's linter on the changed files |
| Go | `go test ./pkg/... -run Name`, `go vet` on the package |
| Rust | `cargo test name`, `cargo clippy -p crate` when cheap |
| JVM | the single test class (`-Dtest=Class#method` or `--tests`) |
| Shell | `shellcheck` on the changed script, a dry run if the script has one |
| Tests only | only the tests you changed |
| Shared component, route or config | focused tests plus typecheck; widen further only on evidence |

Use the commands the project already defines (`package.json` scripts, `Makefile`, `tox`, `justfile`) before inventing
your own. Run independent checks in parallel.

## UI changes

Verify low-risk UI changes (a button, spacing, a label) with code reading and focused tests. Start the app or take
screenshots only when the layout risk is real, the user gave a visual reference, or the user asked for it.

## Speed limits

Unless the user asks or the risk truly needs it, do not: run the full test suite, run a full build or package, create a
worktree, launch the app for visual checks, write a long implementation plan, spawn sub-agents, or invoke other heavy
workflow skills.

## Git

Do not stage, commit, push or open a pull request unless the user asks. When asked, follow the project's commit format
and branch rules, or hand off to `fast-commit`.

## Task context (hand-off)

End with this block so `fast-small-review`, `fast-review-fix` and `fast-commit` in the same conversation can reuse it
instead of rescanning:

```text
Task context
- Goal: <request and acceptance criteria>
- Changed files: <paths>
- Related, unchanged: <paths read to understand scope>
- Checks run: <command, filter, result>
- Review: <fast-small-review run? scope, result, findings>
- Known failures: <related / unrelated, with evidence>
- Open questions: <assumptions or findings still to confirm>
```

If a previous fast skill already produced this block, reuse its scope, files and results. Re-read rules, rescan or rerun
passed checks only when the diff changed, a result no longer covers it, or the risk went up.

## Communication

- Follow the user's language and the project's conventions; keep code, commands, paths and identifiers verbatim.
- One short scope statement at the start; speak up at once on a blocker, a permission need or a key ambiguity.
- Never say "all tests pass" unless that exact scope ran and passed. Report unrelated pre-existing failures separately
  and do not fix them.

## Example requests

- "Hide the share button in the desktop editor header, keep the one in the overflow menu, run only the related tests."
- "Change the copy on this page; don't run the whole suite."
- "This button doesn't update its state after a click; fix it and verify just that."
