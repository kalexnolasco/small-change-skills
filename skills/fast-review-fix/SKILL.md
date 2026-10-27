---
name: fast-review-fix
description: Close out code-review findings on a small change one by one - confirm each still holds, apply the minimum fix, add a regression test when the bug is reproducible, and verify each with a targeted check. Use for findings from fast-small-review, pasted PR comments or an already diagnosed test failure ("fix the P2 from that review", "address these PR comments, no refactoring"). Not for broad rewrites.
---

# Fast Review Fix

## Goal

Close review findings quickly: confirm each problem still exists, fix it with the smallest change, add a regression test
where it pays, and give evidence per finding. A review fix is never a licence for unrelated refactoring.

## Input

Accepted sources:

- findings from `fast-small-review`;
- review comments or inline comments pasted by the user;
- a test failure or regression that is already pinned down.

Without a concrete finding or a reproducible problem, say there is nothing to fix. Do not go hunting for problems.

## When to stop and escalate

This flow fits low-risk fixes inside one page, component or module. Tell the user it is out of scope and stop widening
the change when:

- the fix needs a refactor across independent modules;
- it changes a public API, shared component, protocol, data structure or build configuration;
- it involves security, permissions, persistence, concurrency, migrations or cross-service behaviour;
- several high-risk findings conflict on design;
- the user asks for a full rework.

## Workflow

1. **Sort the findings.** Prefer the task context from `fast-small-review`. Order `P0 → P1 → P2 → P3`, then by
   dependency and risk. Keep each finding's file, line, problem and acceptance condition.
2. **Confirm each one.** Read the current code and minimum context. If a finding no longer holds or another change
   already solved it, change nothing and record the evidence.
3. **Respect the goal.** The user's goal outranks a review suggestion. If a suggestion would change that goal or widen
   the scope, say so, and ask when it matters.
4. **Fix minimally.** Touch only what the finding needs, keep the user's other changes, and use the host's local edit
   tool. Never run commands that overwrite or reset the working tree.
5. **Add a regression test** for a reproducible behaviour bug when a small one is possible; extend an existing test when
   it already covers the area. No unrelated test matrices.
6. **Verify each fix** with at least one directly relevant test or check, plus `git diff --check`. Batch findings that
   the same command covers into one run.
7. **Light re-check.** Look only at the fix diff for side effects, goal drift or new regressions. Do not rerun a full
   review.
8. **Report** each finding as `fixed`, `no change needed (not valid / already done)` or `blocked (needs a decision)`,
   with evidence and the checks you did not run.
9. **Hand off** the task context (below) so `fast-commit` can use it directly.

## Rules for findings

- Do not accept review comments blindly; check them against the code, tests and project rules.
- No drive-by refactors, renames or style changes while fixing a finding.
- If you cannot reproduce it but the risk is plausible, keep the finding open, say the evidence is insufficient and
  propose the next check.
- One root cause may close several findings with one change; report which findings it covers.
- Never add code whose only purpose is to "answer the review" for a finding that does not hold.
- If the real risk turns out higher than the finding said, say so at once and leave this low-risk flow.

## Severity

- `P0`: blocks release, corrupts data or is a serious security issue.
- `P1`: likely functional bug or significant regression.
- `P2`: ordinary functional issue or a clear test gap.
- `P3`: low-risk, non-blocking improvement.

## Verification

Prefer, in order: the affected test filtered by name, the new or reused regression test, lint/typecheck of the changed
files, `git diff --check`. Separate failures caused by the fix (report as blocking or unfinished) from pre-existing,
environmental or unrelated ones (list them, do not attribute them to the fix). One failure is not a reason to run the
full suite or to edit unrelated code. Reuse earlier results only while the diff, coverage and risk are unchanged.

## Git and external state

Edit the working tree only. Do not stage, commit, push, open pull requests or resolve external review threads unless
the user asks.

## Output

```text
Conclusion: fixed N, need a decision M, no change needed K.

Per finding
- [P1] <finding>: fixed
  Change: what was done
  Check: what ran
- [P2] <finding>: no change needed (not valid / already done)
  Evidence: why
- [P1] <finding>: blocked (needs a decision)
  Reason: what is missing or conflicting

Verification
- Ran: focused tests, lint/typecheck, git diff --check
- Not run: what and why
```

Keep the file and line of inline comments in the report, but never resolve or edit them. Report new issues with the
host's inline-comment capability if it has one, or as plain text with file and line.

## Task context (hand-off)

```text
Task context
- Goal: <original request>
- Changed files: <paths>
- Related, unchanged: <paths>
- Checks run: <command, filter, result>
- Known failures: <related / unrelated>
- Open findings: <still unresolved, with reason>
```

## Speed limits

Unless the user asks or the risk truly needs it, do not: run the full suite, run a full build, create a worktree, launch
the app or take screenshots, spawn sub-agents, or run a full code-review workflow.

## Communication

- Follow the user's language and the project's conventions; keep code, commands, paths and identifiers verbatim.
- Say up front which findings you will handle; speak up at once on ambiguity, permissions or scope.
- Passing tests never mean "the code is definitely correct".
- No commit unless the user asks.

## Example requests

- "Fix the P2 test gap from the last review; run only the related tests."
- "Address these PR comments one by one, no refactoring on the side."
- "This test failure is already diagnosed; fix it and add a regression test."
