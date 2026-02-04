# Memory Folder

This folder tracks errors, failures, and solutions during development to prevent recurring issues.

## Error Log Format

### [YYYY-MM-DD] Error Title
- **Status:** Resolved/Open
- **Error:** [Description]
- **Solution:** [How it was fixed]
- **Prevention:** [How to prevent recurrence]

---

## History

### [2026-02-04] Hook File Missing Error
- **Status:** Resolved
- **Error:** PreToolUse hook failed because `.claude/hooks/moai/pre_tool__security_guard.py` did not exist
- **Solution:** Created hook folder structure using `mkdir -p` and bash echo command
- **Prevention:** Initialize project structure before starting development
