---
name: openclaw-safe-update
description: Safely check and manually update OpenClaw on hosts with non-standard service management (no systemd --user), including npm fallback, symlink repair, and gateway restart verification. Use when user asks to update OpenClaw, repair broken openclaw command, or run a controlled self-update through terminal/bot.
---

# OpenClaw Safe Update

Run controlled update workflow with explicit user confirmation before modifying packages.

## Workflow

1. Run `scripts/update_openclaw.sh check` to collect:
   - current OpenClaw version
   - latest npm version
   - openclaw command path
2. If user confirms update, run `scripts/update_openclaw.sh update`.
3. Report concise result:
   - version before/after
   - whether update is still available
   - any manual follow-up needed

## Guardrails

- Do not run auto-update loops.
- Do not use `systemctl --user` in this environment.
- Always repair `/usr/bin/openclaw` symlink after npm update.
- If npm update fails with `ENOTEMPTY` and a stale temp folder exists under `/usr/lib/node_modules/@qingchencloud/.openclaw-zh-*`, clean only that stale folder, then retry once.
- Keep user-facing output short and action-oriented.
