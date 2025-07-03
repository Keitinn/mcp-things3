# Instructions for AI Assistants

This document provides guidance for AI assistants (like Claude) working with the Things3 MCP Server codebase.

## 🎯 Project Overview

This is an MCP (Model Context Protocol) server that integrates with Things3, a popular macOS task management app. The server allows programmatic access to Things3 functionality while respecting the app's philosophy of thoughtful task management.

## 🏗️ Architecture

### Core Components

1. **`fast_server.py`**: Main FastMCP server with tool definitions
   - Handles all MCP protocol communication
   - Defines tools and their schemas
   - Manages auth token validation
   - Provides philosophical guidance in responses

2. **`applescript_handler.py`**: AppleScript execution layer
   - `run_script()`: For inline AppleScript execution
   - `run_script_file()`: For executing .applescript files
   - JSON parsing for all bulk operations
   - Legacy parsing methods (kept for single-item operations)

3. **`applescript/` directory**: JSON-based AppleScript files
   - Each file uses Foundation framework for JSON serialization
   - Consistent structure: convert Things3 objects → NSDictionary → JSON
   - `search_todos.applescript` accepts command-line arguments

## 🔑 Key Design Decisions

### JSON Serialization
- **Why**: AppleScript's native record format flattens when converted to strings
- **Solution**: Use macOS Foundation framework's NSJSONSerialization
- **Pattern**: All bulk read operations use dedicated .applescript files
- **Benefit**: Reliable parsing, handles special characters, future-proof

### ID-Based Operations
- **All tasks/projects have unique IDs** (e.g., "2DCAbD81QBc6oQbzaNjFhM")
- **Users must search/view first** to get IDs before updating/completing
- **Never use title matching** for modifications (ambiguous and error-prone)

### Auth Token Requirement
- **Required for**: `update` operations only
- **Source**: Things3 Settings → General → Enable Things URLs → Manage
- **Storage**: Environment variable `THINGS3_AUTH_TOKEN`
- **Scope**: Device-specific (each Mac has its own token)

### Philosophy Integration
- **Tool descriptions include guidance** on Things3's intended usage
- **Responses reinforce best practices** (e.g., Today list warnings)
- **Examples**: "Today is for commitments, not wishlist", "Deadlines ≠ scheduling"

## 📝 Code Patterns

### Adding a New Tool

1. **Define in `handle_list_tools()`**:
```python
types.Tool(
    name="tool-name",
    description="""Brief description.

PHILOSOPHY:
• Key principle about this tool
• Another principle

TIPS:
• Practical usage tip""",
    inputSchema={...}
)
```

2. **Implement in `handle_call_tool()`**:
```python
if name == "tool-name":
    # Validate auth token if needed
    # Call appropriate AppleScript method
    # Return with philosophical guidance
```

3. **Add AppleScript support** (if needed):
   - Create new .applescript file using existing pattern
   - Use Foundation framework for JSON output
   - Add method in applescript_handler.py

### Error Handling Pattern
```python
try:
    # Operation
except json.JSONDecodeError as e:
    print(f"Error parsing JSON: {e}")
    return []  # Always return safe default
except Exception as e:
    print(f"Error in operation: {e}")
    return []  # Never crash the server
```

## ⚠️ Important Constraints

### Things3 Limitations
- **AppleScript can't access**: Headings, individual checklist items, repeating task details
- **URL scheme requires auth for**: update, update-project, json commands
- **Built-in lists**: Use exact names like "Today", "Upcoming", "Anytime"

### MCP Limitations
- **Stateless protocol**: Can't remember previous commands
- **No file access**: Can't read/write Things3 database directly
- **Async execution**: All operations must complete within timeout

## 🧪 Testing Approach

1. **Manual testing via Claude Desktop** is primary method
2. **Test edge cases**:
   - Empty lists
   - Missing auth token
   - Invalid IDs
   - Special characters in titles/notes

3. **Verify JSON structure**:
```python
# Quick test script
from mcp_server_things3.applescript_handler import AppleScriptHandler
tasks = AppleScriptHandler.get_todays_tasks()
print(json.dumps(tasks, indent=2))
```

## 🚀 Common Tasks

### Update AppleScript Methods
1. Modify the .applescript file in `applescript/`
2. Test with `osascript` command directly
3. Ensure JSON output is valid
4. Update any field mappings in Python

### Add Philosophy Guidance
1. Update tool description in `handle_list_tools()`
2. Add contextual responses in `handle_call_tool()`
3. Reference Things3's principles (see THINGS3_GUIDE.md)

### Debug Issues
1. Check logs for AppleScript errors
2. Verify auth token is set correctly
3. Test AppleScript directly in Script Editor
4. Ensure Things3 is running and accessible

## 📚 Reference Documents

- **`requirements/context.md`**: Things3 philosophy and AppleScript details
- **`requirements/tech_spec.md`**: Tool signatures and implementation specs
- **`QUICK_REFERENCE.md`**: User-facing command reference
- **`THINGS3_GUIDE.md`**: User guide with philosophy and workflows

## 🎨 Style Guidelines

- **Be explicit about IDs**: Always remind users they need IDs from search/view
- **Include philosophy**: Responses should guide toward Things3 best practices
- **Fail gracefully**: Return empty lists/safe defaults, never crash
- **Log errors**: Use print() for debugging, but don't expose internals to users
- **Keep it simple**: This is a focused tool, not a full Things3 replacement

## 🔍 Code Health

- **No parsing cruft**: JSON serialization eliminated complex regex parsing
- **Minimal dependencies**: Just MCP and standard library (plus dotenv for dev)
- **Clear separation**: MCP protocol handling vs Things3 interaction
- **Documented patterns**: Each AppleScript file follows same structure

Remember: This server is a bridge between AI assistants and Things3's thoughtful task management philosophy. Every feature should reinforce good productivity practices, not just enable bulk operations.