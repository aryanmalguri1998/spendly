# Claude Code — Learning Log & Revision Notes

> A running log of Claude Code commands, concepts, and workflows I've used.
> Built while following a "how to use Claude" playlist so I have something to come back to and revise.
>
> **How this file is maintained:** When I say "generate summary" (or similar), Claude appends
> what I've learned/used since the last entry — slash commands, subagents, MCP, hooks, etc.

---

## Slash Commands Used

| Command | What it does | Notes |
|---------|-------------|-------|
| `/rename <name>` | Renames the current session | Used to name this session "intro session" |
| `/resume` | Reopens a previous session to continue it | Cancelled it this time |
| `/exit` | Quits the Claude Code session | Prints "Bye!" |
| `/export <file>` | Exports the full conversation to a file | Exported to `file.md` |
| `/model` | Picks the model + sets default for new sessions | Set default to **Opus 4.8** |
| `/usage` | Opens usage/settings dialog | Shows plan usage |
| `/login` | Sign in to your Anthropic / Claude account | Used to authenticate or switch accounts |
| `/logout` | Sign out of the current account | Clears stored credentials |
| `/extra-usage` | Manage extra usage beyond your plan limits | Lets you opt in to / control pay-as-you-go usage when you hit plan caps |
| `/insights` | Generates a usage report analyzing your past sessions | Outputs an HTML report (what's working, friction, suggestions) |
| `/config` | Opens the configuration dialog | Edit settings like theme, model, and other preferences |
| `/permissions` | Manage tool/command permissions | Allow or deny commands & file access so Claude isn't blocked mid-task |
| `/theme` | Change the color theme | Set to **dark** |
| `/voice` | Voice input/output controls | Talk to Claude / hear responses instead of typing |

---

## Concepts & Workflows

### Running commands in the background
- `python app.py` was launched as a **background task** (gets an ID like `becnk6q0x`).
- Claude is notified when it finishes/stops; output is written to a temp file you can read anytime.
- Useful for long-running processes (dev servers) so you can keep working.

### Asking Claude about a codebase
- Asked Claude to explain **what the project does**, the **tech stack**, and the **project structure** — Claude reads the files and summarizes instead of you digging manually.

---

## Concepts to explore next (from the playlist)
- [ ] **Subagents** — spawning specialized agents for parallel/complex tasks (`Agent` / `Task` tools)
- [ ] **MCP servers** — connecting external tools/data sources
- [ ] **Hooks** — auto-running behavior on events (e.g. format on save, run on stop)
- [ ] **Skills / custom slash commands** — reusable prompts & workflows
- [ ] **Plan mode** — let Claude design before editing
- [ ] **Memory** — persistent facts across sessions

---

*Last updated: 2026-06-14*
