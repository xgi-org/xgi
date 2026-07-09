# Project Instructions for AI Agents

This file provides instructions and context for AI coding agents working on this project.

<!-- BEGIN BEADS INTEGRATION v:1 profile:minimal hash:ca08a54f -->
## Beads Issue Tracker

This project uses **bd (beads)** for issue tracking. Run `bd prime` to see full workflow context and commands.

### Quick Reference

```bash
bd ready              # Find available work
bd show <id>          # View issue details
bd update <id> --claim  # Claim work
bd close <id>         # Complete work
```

### Rules

- Use `bd` for ALL task tracking — do NOT use TodoWrite, TaskCreate, or markdown TODO lists
- Run `bd prime` for detailed command reference and session close protocol
- Use `bd remember` for persistent knowledge — do NOT use MEMORY.md files

## Session Completion

**When ending a work session**, you MUST complete ALL steps below. Work is NOT complete until `git push` succeeds.

**MANDATORY WORKFLOW:**

1. **File issues for remaining work** - Create issues for anything that needs follow-up
2. **Run quality gates** (if code changed) - Tests, linters, builds
3. **Update issue status** - Close finished work, update in-progress items
4. **PUSH TO REMOTE** - This is MANDATORY:
   ```bash
   git pull --rebase
   bd dolt push
   git push
   git status  # MUST show "up to date with origin"
   ```
5. **Clean up** - Clear stashes, prune remote branches
6. **Verify** - All changes committed AND pushed
7. **Hand off** - Provide context for next session

**CRITICAL RULES:**
- Work is NOT complete until `git push` succeeds
- NEVER stop before pushing - that leaves work stranded locally
- NEVER say "ready to push when you are" - YOU must push
- If push fails, resolve and retry until it succeeds
<!-- END BEADS INTEGRATION -->


## Build & Test

_Add your build and test commands here_

```bash
# Example:
# npm install
# npm test
```

## Architecture Overview

_Add a brief overview of your project architecture_

## Conventions & Patterns

### Git workflow: ALL PRs target `dev`, not `main`

`main` is for releases only. Every feature, fix, doc change, and test change must
target the `dev` branch. The GitHub default base is currently `main`, so this is
easy to get wrong — you MUST verify the base every time.

**When opening a PR:**

```bash
gh pr create --base dev --title "..." --body "..."
```

`--base dev` is not optional. If you omit it, the PR will silently default to
`main` and break the release workflow. (See #717 for the team's documented
process and the iambic-pentameter reply for the squash/merge policy.)

**When fixing an already-open PR that targets the wrong base:**

```bash
gh pr edit <PR#> --base dev
```

**When merging:**

- Feature branch → `dev`: squash or merge, fine for small fixes
- `dev` → `main`: regular merge (preserves history) at release time
- After a release: backmerge `main` → `dev` to keep them in sync

**Do not:** open a PR against `main`, merge a feature PR into `main`, force-push
`main`, or change branch settings without team agreement.
