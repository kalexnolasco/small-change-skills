# Small Change Skills

A fast lane for small code changes in existing projects: **minimal edit, targeted checks, quick review,
finding-by-finding fixes and scoped commits.** Four [Agent Skills](https://agentskills.io) in the standard `SKILL.md`
format, for Claude Code, Codex and any other tool that loads skills.

Most coding agents treat every request like a feature: they explore the whole repo, run the full test suite, write a
plan and open a review workflow. That is the right call for big work and a waste of minutes and tokens for "change this
label". These skills give the agent a disciplined short path, and the rules for when to leave it.

## The skills

| Skill | What it does | Example |
| --- | --- | --- |
| [fast-small-task](skills/fast-small-task/SKILL.md) | Ships a small, low-risk change with the minimum edit and targeted checks, then reviews it | "Hide the share button on this page, run only the related tests" |
| [fast-small-review](skills/fast-small-review/SKILL.md) | Reviews a small change and reports only evidenced, actionable findings (P0–P3); never edits | "Quick review of my diff, don't change anything" |
| [fast-review-fix](skills/fast-review-fix/SKILL.md) | Confirms and fixes concrete findings one by one, with a check per fix | "Fix the P2 from that review, nothing else" |
| [fast-commit](skills/fast-commit/SKILL.md) | Commits only this task's files or hunks in the project's format; never pushes or amends | "Commit this task, leave the other files out" |

They work alone or as a chain in one conversation. Each one ends with a short **Task context** block (goal, changed
files, checks run, known failures, open findings) that the next one reuses instead of rescanning the repository.

```text
fast-small-task ──► fast-small-review ──► fast-review-fix ──► fast-commit
   edit + check       report findings       fix + check        scoped commit
```

### Guard rails built in

- **Knows when it is not small.** Migrations, public APIs, shared components, security, concurrency or cross-service
  work make the skill stop and hand over to the full workflow.
- **Never sweeps the working tree.** No `git add -A`, no reset, stash or clean; unrelated changes stay untouched.
- **Never pushes, amends or bypasses hooks**, and asks before committing to a default or protected branch.
- **Honest reporting.** Every result lists what ran and what did not; "no findings" never means "correct".
- **Follows the project.** `AGENTS.md`, `CLAUDE.md`, commit format and trailer policy win over any default.

## Install

### Claude Code (plugin)

```text
/plugin marketplace add kalexnolasco/small-change-skills
/plugin install small-change-skills@small-change-skills
```

### Skills CLI (Claude Code, Codex and others)

```bash
npx skills add kalexnolasco/small-change-skills
```

Add `-g` for a global install.

### By hand

```bash
git clone https://github.com/kalexnolasco/small-change-skills.git
cp -R small-change-skills/skills/* ~/.claude/skills/   # Claude Code, global
cp -R small-change-skills/skills/* ~/.codex/skills/    # Codex, global
```

For a single project copy into `.claude/skills/` or `.agents/skills/` instead. More options, updating and removal are in
[docs/usage.md](docs/usage.md).

## Use

Name the skill in plain language, or call it directly:

```text
Use fast-small-task: change the save button label to "Save draft", keep the current behaviour.
/fast-small-review
/fast-commit
```

The skills answer in your language and keep code, commands and paths verbatim.

## Compatibility

- Pure instructions, no scripts to run: verification uses the tools your project already has.
- Host-specific features (patch tool, inline review comments, a full `code-review` skill) are optional; each has a
  plain fallback.
- Tested by structure (`python3 scripts/validate.py`). End-to-end behaviour depends on the host and model.

## Credits and licence

This is an English, stack-neutral edition of [heyanpeng/fast-code-skills](https://github.com/heyanpeng/fast-code-skills)
by heyanpeng, published under the MIT licence. The original's project-specific `upgrade-deepdoc` skill is not included;
see [CHANGELOG.md](CHANGELOG.md) for every change.

[MIT](LICENSE): both copyright notices must be kept in copies.
