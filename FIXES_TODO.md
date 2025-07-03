# Things3 MCP Server - Simple Fixes

**⚠️ DELETE THIS FILE AFTER COMPLETING ALL FIXES ⚠️**

## Context
Personal Things3 MCP server. Works fine, just needs a few practical improvements.

## Actually Worth Fixing

### 1. Better Error Messages
**Problem**: Generic "Failed to X" messages don't help debug
```python
except Exception as e:
    return f"Failed to retrieve inbox tasks: {str(e)}"
```
**Fix**: 
- Catch subprocess.CalledProcessError specifically
- Include the actual error from AppleScript/subprocess
- Maybe log the full command that failed

### 2. Basic Unit Tests
**What to test**:
- URL building with special characters
- Response formatting (the "• Task (id: xxx)" format)
- Auth token error message formatting
- Maybe mock some AppleScript responses

### 3. Validate Auth Token on Startup
**Problem**: Only find out token is wrong when trying to update
**Fix**: 
- Quick check on server startup if token is set
- Maybe try a dummy update call to verify it works
- Clear message about where to get token

### 4. Handle "missing value" Consistently  
**Problem**: Checking for literal "missing value" string from AppleScript
```python
if due_date and due_date != "missing value":
```
**Fix**: 
- Clean this up in one place when parsing AppleScript response
- Convert to None or empty string consistently

## Nice to Have (If Bored)

- Log all x-callback URLs for debugging (but not the auth token!)
- Add `--no-philosophy` flag to skip the life advice
- Timeout on AppleScript calls (they can hang)

## What NOT to Fix
- Date parsing (English/US only is fine)
- Concurrency (probably won't have multiple requests)
- Complex type safety (it works)
- Config files (env var is fine)
- X-callback-url feedback (Things3 doesn't provide any)

## Test Strategy
Just mock the subprocess calls and test the pure Python parts:
- `build_things_url()` 
- Response formatting functions
- Error message generation

Don't need integration tests - too much hassle.

---
Remember: This is personal software. Keep it simple!