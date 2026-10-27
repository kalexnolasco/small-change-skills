# Usage

## Layout

```text
small-change-skills/
├── skills/                    # the only source of truth
│   ├── fast-small-task/SKILL.md
│   ├── fast-small-review/SKILL.md
│   ├── fast-review-fix/SKILL.md
│   └── fast-commit/SKILL.md
├── .claude-plugin/            # Claude Code plugin + marketplace manifests
├── scripts/validate.py        # structure and link checks
├── AGENTS.md, CLAUDE.md       # rules for maintaining this repository
└── README.md, CHANGELOG.md, LICENSE
```

An installed copy does not follow edits to this repository; update it explicitly.

## Install

### Claude Code plugin

```text
/plugin marketplace add kalexnolasco/small-change-skills
/plugin install small-change-skills@small-change-skills
```

Update with `/plugin marketplace update small-change-skills`; remove with `/plugin uninstall small-change-skills`.
Plugin skills may appear namespaced, for example `/small-change-skills:fast-commit`.

### Skills CLI

```bash
npx skills add kalexnolasco/small-change-skills        # this project
npx skills add kalexnolasco/small-change-skills -g     # global
npx skills check
npx skills update
```

`update` may update other skills the CLI manages; read its prompt first.

### Manual copy

| Tool | Project | Global |
| --- | --- | --- |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| Codex | `.agents/skills/` | `~/.codex/skills/` (or `$CODEX_HOME/skills/`) |

```bash
mkdir -p ~/.claude/skills
cp -R /path/to/small-change-skills/skills/* ~/.claude/skills/
```

Copy only `skills/`, never this repository's `AGENTS.md` or `CLAUDE.md`, so the target project's own rules stay in
charge. Check first that no skill with the same name exists; back up and compare any you customised. On Windows copy the
four folders with Explorer or PowerShell.

Open a new session and check that the four names are listed. If both a project and a global copy exist, confirm which
one the tool actually loads.

To remove a manual install, delete only these four folders.

## Calling the skills

```text
Use fast-small-task: change the button tooltip to "Save draft", keep the current behaviour.
Use fast-small-review: check the change I just made, report only evidenced issues.
Use fast-review-fix: confirm and fix the findings above one by one.
Use fast-commit: commit only the files from this task.
```

Claude Code also accepts `/fast-small-task`; Codex accepts `$fast-small-task`. If the tool does not find a skill,
check the install path and the `SKILL.md` frontmatter, then reopen the session, or simply ask the agent to read the file
and follow it.

In one conversation `fast-small-task` runs `fast-small-review` when it finishes, unless you ask it not to. Later skills
reuse the Task context and rerun checks only when the diff, coverage or risk changed. `fast-small-review` also takes an
explicit scope: `staged`, `unstaged`, files, a commit or a base branch. `fast-commit` follows your commit format, leaves
unrelated changes out, stops on unclear ownership, protected branches or failing checks, and never pushes.

## Checking a change to this repository

```bash
python3 scripts/validate.py
git diff --check
```

The validator checks each skill's frontmatter (`name` equals the directory, lowercase-hyphenated, at most 64
characters; a non-empty `description` of at most 1024), the plugin manifests' JSON and every relative Markdown link. It
proves structure, not behaviour: try a changed skill on a real repository before releasing it.
