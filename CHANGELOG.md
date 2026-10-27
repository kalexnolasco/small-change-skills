# Changelog

All notable changes are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and the project uses [Semantic Versioning](https://semver.org/).

## [1.0.0] - 2026-10-27

First English edition, derived from [heyanpeng/fast-code-skills](https://github.com/heyanpeng/fast-code-skills)
(MIT) at commit `052b78e`.

### Added

- Claude Code plugin and marketplace manifests (`.claude-plugin/`), so the skills install with `/plugin`.
- `scripts/validate.py` and a GitHub Actions workflow that checks frontmatter, names, description length and links.
- A shared, explicit "Task context" hand-off block used by all four skills.
- A stack-neutral verification matrix (JS/TS, Python, Go, Rust, JVM, shell, docs) in `fast-small-task`.

### Changed

- All skills and documents translated to English and written to be language-neutral.
- `fast-commit`: protected-branch check covers the default branch, release branches and project-protected branches
  (the original only stopped on `master`); documents `git commit -- <paths>`, non-interactive hunk staging and project
  trailer policies (sign-off, AI attribution).
- `fast-small-review`: the default-branch base is resolved with `git merge-base` against `origin/HEAD`.

### Removed

- `upgrade-deepdoc`: specific to one private project, not reusable.
