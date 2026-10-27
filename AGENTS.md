# Maintaining this repository

This repository ships four skills. The source of truth is `skills/<name>/SKILL.md`; edit those files, never an
installed copy.

When the user names a fast skill, or the task fits one, read its file first and follow it:

| Skill | File | Use for |
| --- | --- | --- |
| fast-small-task | `skills/fast-small-task/SKILL.md` | Small, low-risk changes |
| fast-small-review | `skills/fast-small-review/SKILL.md` | Reviewing a small change, report only |
| fast-review-fix | `skills/fast-review-fix/SKILL.md` | Confirming and fixing concrete findings |
| fast-commit | `skills/fast-commit/SKILL.md` | Committing the current task when asked |

Rules:

- Keep the standard `SKILL.md` frontmatter (`name`, `description`) and the directory name equal to `name`.
- Skills stay project-, language- and host-neutral: anything host-specific needs an equivalent or a plain-text fallback.
- Never add a required dependency on a skill this repository does not ship.
- After any change run `python3 scripts/validate.py` and `git diff --check`; update `README.md`, `docs/usage.md` and
  `CHANGELOG.md` when installation, invocation or behaviour changes, and bump the version in both
  `.claude-plugin/*.json` files on a release.

These are the library's own rules; installing the skills elsewhere copies only `skills/`.
