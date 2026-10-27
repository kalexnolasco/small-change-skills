---
name: fast-small-review
description: Quickly review a small change and report only actionable, evidenced findings (P0–P3) with file and line, backed by targeted checks. Read-only, never edits. Use after fast-small-task or on request ("quick review of my diff", "any obvious regression here?", "review the staged changes, no full test run"). Escalates to a full review for large, risky or cross-module changes.
---

# Fast Small Review

## Goal

Decide quickly whether a small change has a real problem that should block delivery. Focus on whether the request is
met, obvious regressions and verification evidence. Do not turn one small change into a long full code review.

## When to escalate

This flow fits low-risk changes inside one page, component or module. Escalate to a full review, and say why, when:

- several independent modules change, or the change is an architectural refactor;
- a public API, shared component, protocol, data structure or build configuration changes;
- security, permissions, persistence, concurrency, migrations or cross-service behaviour are involved;
- the user asks for a thorough review;
- a focused check fails and you cannot show it is unrelated to the change.

Use the host's review capability (for example a `code-review` skill or command) if it has one; otherwise continue with
your own review sized to the real risk. Do not require another skill to be installed, and stop calling it a "fast"
review once escalated.

## Scope

1. If the user named a scope (`staged`, `unstaged`, a commit, a range, files or a base), use exactly that.
2. Otherwise reuse the task context of a previous fast skill in this conversation: its goal, changed files and checks.
3. Otherwise review the uncommitted diff; if there is none, the current branch against its merge base with the default
   branch (`git merge-base HEAD origin/HEAD`, falling back to `main` or `master`).
4. If there is still nothing, report "nothing to review". Never review the whole repository on your own initiative.
5. Read only the rules (`AGENTS.md`, `CLAUDE.md`, contributing guide), callers, types and tests that bear on the
   changed paths.
6. Never run a command that overwrites or resets the working tree.

## What to look for

Report only findings you can pin to a file and line and that have a real effect:

- the request is not fully met, or an explicit requirement is missing;
- a functional regression, wrong state or unhandled edge case;
- error handling, null/empty values, permissions or disabled states that are wrong;
- tests that are missing, broken or assert the wrong behaviour;
- changes beyond the request, or unintended side effects.

Do not report: personal style preferences, formatting or naming that does not change behaviour, speculation without
evidence, optional refactors, or pre-existing issues unrelated to the change.

## Severity

- `P0`: blocks release, corrupts data or is a serious security issue.
- `P1`: likely functional bug or significant regression; fix before delivery.
- `P2`: ordinary functional issue or a clear test gap; should fix.
- `P3`: low-risk, non-blocking improvement.

Never pad the list. When nothing is actionable, say "No actionable findings."

## Workflow

1. State the scope and base in one sentence.
2. Read the diff and the minimum surrounding context.
3. Run `git diff --check` (or `git diff --cached --check` for staged scope).
4. Run the focused tests, lint or typecheck for the changed paths, filtered by name where the runner allows it.
5. Widen verification only for a high-impact risk, a public interface change, or when focused checks are not enough.
6. Do not edit code, stage, commit, push or open pull requests. Suggest fixes only; if the user asks for fixes, hand off
   to `fast-review-fix`.
7. Run independent checks in parallel.
8. If the diff has not changed since the task context was produced and its checks still cover it, do not rerun passed
   checks; add a check only when a finding needs new evidence.

## Failed checks

- **Caused by this change:** report it as a finding or a blocker, with the evidence.
- **Pre-existing, environmental or unrelated:** not a finding; list it under verification.

A failing test is not a reason to run the full suite, and never blame the change for a failure you cannot tie to it.

## Output

Conclusion first, then findings:

```text
Conclusion: No actionable findings. | Found N issue(s).

Findings
- [P1] path/to/file.ts:42
  Problem: what is wrong
  Impact: why it affects behaviour or delivery
  Fix: an actionable direction

Verification
- Ran: focused tests, lint/typecheck, git diff --check
- Not run: what and why

Scope: files, diff or base reviewed.
```

When the host supports inline review comments (for example a findings tool or `::code-comment`), you may also emit them
for clear, line-specific findings; otherwise plain text with file and line is enough. Always keep the summary.

## Task context (hand-off)

Keep the goal, reviewed files or base, related unchanged files, checks run, known failures and findings in the output so
`fast-review-fix` or `fast-commit` can use them without rescanning the same scope.

## Speed limits

Unless the user asks or the risk truly needs it, do not: run the full suite, run a full build, create a worktree,
launch the app, take screenshots or run visual regression, spawn sub-agents, or start another heavy review workflow.

## Communication

- Follow the user's language and the project's conventions; keep code, commands, paths and identifiers verbatim.
- Report findings; never fix them in this flow.
- "No findings" never means "the code is correct".
- When escalating, name the specific trigger.

## Example requests

- "Quick review of the button change I just made; don't run the full test suite."
- "Is there any obvious regression in this small change? Report only, don't edit."
- "Does the current diff meet the request? Run the relevant tests only."
