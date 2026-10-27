---
name: fast-commit
description: Commit only the changes that belong to the current task - pick the right staged, unstaged and untracked files (or hunks), leave everything else untouched, write a message in the project's format and run a targeted pre-commit check. Use only when the user asks to commit ("commit this task", "commit just my change, not the other files", "write the commit message but don't commit"). Never pushes, amends or rewrites history.
---

# Fast Commit

## Goal

When the user explicitly asks for a commit, identify what "this task" changed, leave unrelated work alone, write a
message that follows the project's rules, run the targeted check and create the commit.

## Identify the task's changes

Prefer the task context of a previous fast skill in this conversation (goal, changed files, checks). Without it, work in
two passes and read contents only for candidates.

Pass 1, names only:

- `git status --short`
- `git diff --name-only`
- `git diff --cached --name-only`
- `git ls-files --others --exclude-standard`

Pass 2, candidates only:

- `git diff -- <candidate>`
- `git diff --cached -- <candidate>`

Decide ownership from the conversation's goal, the files actually edited in this task, the diff itself, related tests
and the project's rules. Include only what you can confirm belongs to the task:

- something already staged but unrelated must come out of the commit;
- unstaged changes that clearly belong to the task may be added;
- untracked files created by this task may be added;
- if ownership is unclear, stop and list the candidates. Never guess.

Never use `git add -A`, `git add .`, `git commit -a` or anything else that sweeps the whole working tree. Stage whole
files by exact path. When the project or user prefers it, `git commit -m "<msg>" -- <paths>` commits exactly those paths
regardless of what else is staged.

## Mixed files

If one file holds both this task's changes and someone else's:

1. stage only this task's hunks (`git add -p` is interactive; prefer applying a filtered patch with
   `git apply --cached` when the host cannot drive interactive prompts);
2. continue only if the split is reliable;
3. otherwise stop, name the file and the conflicting ranges, and let the user sort it out.

Never overwrite, revert, stash, reset or clean the user's unrelated changes.

## Commit message

1. Read the project's `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING`, commit-msg hooks and the last ~10 commits.
2. Write an outcome-focused subject from the actual diff.
3. Precedence: the user's explicit format and language, then the project's rules and recent style. With no convention,
   use Conventional Commits (`<type>: <summary>`) in the language of the conversation, for example:

   ```text
   fix: keep the top menu open after resize
   feat: show row actions based on container width
   test: add regression test for the review fix
   ```

4. One subject line is usually enough. Add a 1–3 line body only for independent changes or verification limits worth
   recording.
5. Follow the project's policy on trailers (sign-off, issue references, co-author lines). Some projects require them and
   some forbid AI attribution: the project's rule wins over any tool default.
6. If the user asked only for a message, output it and do not commit.

## Before committing

1. Confirm the final staged diff contains only this task.
2. Run `git diff --cached --check`.
3. Run the targeted tests and lint/typecheck for the changed paths. Do not run the full suite or a full build by default.

Reuse earlier results while they still cover the staged diff; rerun only when the staged diff changed coverage, a result
went stale or the risk rose. If a check fails, stop and report; commit anyway only if the user explicitly says so, and
mark the failure in the report.

If `git add`, `git commit` or another git step fails because of the sandbox, permissions, `.git/index.lock` or the
environment:

1. stop; do not retry in a loop or work around the restriction;
2. leave the working tree as it is;
3. print copy-ready commands with exact paths (`git add <paths>`, `git diff --cached --check`, `git commit -m "..."`);
4. state clearly that no commit was created.

## Safety

- **Protected branches:** stop and ask before committing directly to the default branch (`git symbolic-ref
  refs/remotes/origin/HEAD`, usually `main` or `master`), a release branch, or any branch the project marks as
  protected, unless the user already approved committing there.
- Never `git commit --amend`, rebase or otherwise rewrite history.
- Never push, open a pull request or touch external review threads.
- Never bypass hooks (`--no-verify`).
- Stop on merge or rebase conflicts.
- If a hook modifies or creates files, stop, report the new changes and let the user confirm.
- Never `git reset`, `git clean`, a destructive `checkout`/`restore`, or `stash`.

## Report

```text
Commit: <hash> <subject>
Task files: <list>
Excluded (unrelated): <list or none>
Staged automatically: <list or none>
Checks: <what actually ran>
Left uncommitted: <list or none>
```

If nothing can be confirmed as part of the task, explain why and do not create an empty commit. On failure, keep the
working tree, explain the cause and do not bypass hooks or roll anything back.

## Speed limits

Unless the risk truly needs it or the user asks, do not: run the full suite, run a full build or package, create a
worktree, push or do any remote operation, auto-fix hook complaints, or run other heavy workflows. Run independent
checks in parallel.

## Communication

- Follow the user's language and the project's conventions; keep code, commands, paths and identifiers verbatim.
- Before committing, briefly show the files and the message.
- "Committed" never means "all tests pass" unless the full suite actually ran.
- Stop and say so immediately on unclear ownership, a protected branch or a blocking check.

## Example requests

- "Commit this small task, including its unstaged changes."
- "Figure out which changes are mine and commit only those."
- "Write the commit message but don't commit yet."
