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
- **Error:** PreToolUse/PostToolUse hooks failed because `.claude/hooks/moai/*.py` files did not exist
- **Solution:** Created all required hook files using bash echo command
- **Prevention:** Initialize project structure with all required files before development

### [2026-02-04] Docker ARM64 Compatibility Consideration
- **Status:** Documented
- **Context:** Raspberry Pi uses ARM64 architecture, need platform-specific images
- **Solution:** Added `platform: linux/arm64` to docker-compose.yml services
- **Prevention:** Always check target architecture before container deployment

### [2026-02-04] NAS Mount Path Configuration
- **Status:** Documented
- **Context:** NAS mount paths vary by system (/mnt, /media, custom NFS mounts)
- **Solution:** Created .env.example with NAS_PATH variable and deploy.sh for interactive setup
- **Prevention:** Use environment variables for all system-specific paths

### [2026-02-04] Korean Filename Handling
- **Status:** To Be Tested
- **Context:** Korean filenames and special characters in paths may cause encoding issues
- **Solution:** Use UTF-8 encoding in Python scripts and ensure proper locale settings
- **Prevention:** Add filename sanitization in validation step

### [2026-02-04] Code Review - Iteration 1 Findings
- **Status:** Partially Resolved
- **Critical Issues Found:** 2
- **High Issues Found:** 4
- **Medium Issues Found:** 4

#### Critical #1: Command Injection Vulnerability
- **Location:** medical-doc-automation.json Merge Document node
- **Issue:** File paths directly interpolated into shell command without sanitization
- **Fix:** Use Execute Command with proper parameter binding, add filename sanitization

#### Critical #2: Hardcoded Default Password
- **Location:** docker-compose.yml
- **Issue:** Password `changeme` in version control
- **Fix:** Remove from docker-compose, use .env only

#### High #3: Windows Path Compatibility
- **Location:** Path parsing in n8n workflow
- **Issue:** Hardcoded forward slashes, breaks on Windows
- **Fix:** Use Node.js path module, normalize paths

#### High #6: Incomplete Error Handler
- **Location:** Error handler node
- **Issue:** errorPath calculated but file never moved
- **Fix:** Add actual file move operation

#### Medium #8: Missing Dependencies
- **Issue:** requirements.txt exists but not referenced in Dockerfile
- **Fix:** Update Dockerfile to install from requirements.txt

### [2026-02-04] Iteration 1 Fixes Applied
- **Status:** Completed
- **Critical #1 (Command Injection):** Added filename sanitization in Python script and n8n workflow
- **Critical #2 (Hardcoded Password):** Removed password from docker-compose.yml, now only in .env
- **High #3 (Windows Paths):** Added path normalization with `replace(/\\/g, '/')`
- **High #6 (Error Handler):** Added actual file move operation to _Error folder
- **High #4 (JSON Validation):** Added separate validation node with field checking
- **Low #13 (Resource Limits):** Added CPU and memory limits to docker-compose
- **Low #14 (Health Check):** Added healthcheck for n8n container

### [2026-02-04] Security Hardening
- **Status:** Completed
- Added path traversal detection in Python script
- Added filename sanitization regex: `[^a-zA-Z0-9._-]`
- Added .gitignore for .env files
