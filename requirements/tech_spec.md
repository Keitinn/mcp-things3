## 🔧 Technical Specification for Things3 MCP Server

### 📋 Tool Signatures & Schemas

#### 1. `update-things3-todo`
```python
types.Tool(
    name="update-things3-todo",
    description="""Update an existing to-do in Things3. Requires the todo's ID (use search or view tools first).

SCHEDULING PHILOSOPHY:
• when="today" → Use sparingly. Today is for focused commitments, not a wishlist
• when="2024-12-25" → Task hibernates in Upcoming until this date
• when=null → Moves to Anytime (can tackle whenever). Good default for most tasks
• when="" → Clears date, returns to Anytime
• deadline → Task stays in Anytime even with deadline (can start anytime, must finish by date)

TIPS:
• Don't reschedule repeatedly - might mean task needs breaking down
• Clearing a date (when="") often better than pushing to tomorrow
• Use tags for priority rather than scheduling everything for today""",
    inputSchema={
        "type": "object",
        "properties": {
            "id": {"type": "string", "description": "Required. The ID of the todo to update"},
            "title": {"type": "string"},
            "notes": {"type": "string"},
            "when": {"type": ["string", "null"], "description": "today, tomorrow, evening, anytime, someday, YYYY-MM-DD, or empty string to clear"},
            "deadline": {"type": ["string", "null"], "description": "YYYY-MM-DD or empty string to clear"},
            "tags": {"type": "array", "items": {"type": "string"}, "description": "Replaces all tags"},
            "checklist": {"type": "array", "items": {"type": "string"}, "description": "Full replacement of checklist items"},
            "list": {"type": "string", "description": "Project or area name to move to"},
            "completed": {"type": "boolean"},
            "canceled": {"type": "boolean"}
        },
        "required": ["id"],
        "additionalProperties": False
    }
)
```

**Implementation**:
```python
# In handle_call_tool()
if name == "update-things3-todo":
    # 1. Get auth token
    auth_token = os.environ.get("THINGS3_AUTH_TOKEN")
    if not auth_token:
        return [types.TextContent(type="text", text="Error: THINGS3_AUTH_TOKEN environment variable not set. Get your token from Things3 Settings → General → Enable Things URLs → Manage")]
    
    # 2. Build URL with special handling for empty strings
    base_url = "things:///update"
    params = {
        "id": arguments["id"],
        "auth-token": auth_token
    }
    
    # Handle fields that can be cleared with empty string
    if "when" in arguments:
        params["when"] = arguments["when"] if arguments["when"] else ""
    if "deadline" in arguments:
        params["deadline"] = arguments["deadline"] if arguments["deadline"] else ""
    
    # Normal fields
    if "title" in arguments:
        params["title"] = arguments["title"]
    if "notes" in arguments:
        params["notes"] = arguments["notes"]
    if "tags" in arguments:
        params["tags"] = arguments["tags"]  # Will be joined with commas by build_url
    if "checklist" in arguments:
        params["checklist-items"] = "\n".join(arguments["checklist"])
    if "list" in arguments:
        params["list"] = arguments["list"]
    if "completed" in arguments:
        params["completed"] = str(arguments["completed"]).lower()
    if "canceled" in arguments:
        params["canceled"] = str(arguments["canceled"]).lower()
    
    # 3. Execute and provide smart response
    # Include philosophy tips based on what was updated
```

#### 2. `view-upcoming`
```python
types.Tool(
    name="view-upcoming",
    description="""View scheduled future tasks in Things3's Upcoming list.

WHAT YOU'LL SEE:
• Tasks scheduled for specific future dates (hibernating until then)
• Next 7 days shown separately at top
• Does NOT include tasks with deadlines but no start date

PHILOSOPHY:
• Upcoming is for "I can't/won't start this until X date"
• Not everything needs a date - resist scheduling for scheduling's sake
• If unsure when to start something, leave in Anytime instead""",
    inputSchema={
        "type": "object",
        "properties": {},
        "additionalProperties": False
    }
)
```

#### 3. `view-anytime`
```python
types.Tool(
    name="view-anytime", 
    description="""View all unscheduled active tasks in Things3's Anytime list.

WHAT YOU'LL SEE:
• All tasks without specific start dates
• Tasks with deadlines (but no when date)
• Today's tasks marked with a star
• Organized by project/area

PHILOSOPHY:
• Most tasks should live here - ready when you are
• Having many tasks in Anytime is normal and good
• Pull from here to Today as capacity allows
• Deadlines ≠ scheduling (deadline tasks stay here until you schedule them)""",
    inputSchema={
        "type": "object",
        "properties": {},
        "additionalProperties": False
    }
)
```

#### 4. Modified `complete-things3-todo`
```python
types.Tool(
    name="complete-things3-todo",
    description="""Mark a todo as completed. Requires the todo's ID (find it using search or view tools first).

NOTE: Completion is final - tasks move to Logbook. If you might need it again, consider:
• Rescheduling instead (update with when="tomorrow")
• Moving to Someday (update with when="someday")
• Adding a "waiting" tag instead""",
    inputSchema={
        "type": "object",
        "properties": {
            "id": {"type": "string", "description": "Required. The ID of the todo to complete"}
        },
        "required": ["id"],
        "additionalProperties": False
    }
)
```

### 📊 Response Format Specifications

#### All View/Search Tools MUST Return:
```python
{
    "id": "2DCAbD81QBc6oQbzaNjFhM",     # ALWAYS included
    "title": "Review Q4 presentation",   # Task title
    "list": "Work",                      # Parent project/area name (not ID)
    "list_type": "project",              # "project" or "area" 
    "when": "today",                     # today/tomorrow/evening/YYYY-MM-DD/null
    "deadline": "2024-12-31",            # YYYY-MM-DD/null
    "tags": ["urgent", "review"],        # Array of tag names
    "notes_preview": "First 100 chars...", # Truncated notes
    "has_checklist": true,               # Boolean
    "checklist_summary": "3/5",          # X/Y format if has checklist
    "status": "open"                     # open/completed/canceled
}
```

#### Today List Response Format:
```python
# When count > 4
"⚠️ Today's Focus (7 items - consider reviewing):

• Buy milk (id: ABC123...)
• Call dentist @ 2pm (id: DEF456...) 
• Review presentation [Work] #urgent (id: GHI789...)
...

💡 Today has more than 4 items. Consider:
• Which are truly TODAY vs. nice-to-have?
• Move flexible items to Anytime (update with when='')
• Use Evening section for time-specific tasks"

# When count <= 4
"Today's Focus (3 items):

• Buy milk (id: ABC123...)
• Call dentist @ 2pm (id: DEF456...)
• Review presentation [Work] #urgent (id: GHI789...)"
```

### 🔌 AppleScript Handler Method Signatures

#### Modified Methods
```python
@staticmethod
def get_inbox_tasks() -> List[Dict[str, Any]]:
    """Returns tasks with id, title, notes, due_date, when, tags, list, list_type"""
    
@staticmethod  
def get_todays_tasks() -> List[Dict[str, Any]]:
    """Returns tasks with id, title, notes, due_date, when, tags, list, list_type, is_evening"""
    
@staticmethod
def get_projects() -> List[Dict[str, Any]]:
    """Returns projects with id, title, notes, area, todo_count"""

@staticmethod
def search_todos(query: str) -> List[Dict[str, Any]]:
    """Returns tasks with id, title, notes, status, due_date, when, tags, list, list_type"""

@staticmethod
def complete_todo_by_id(todo_id: str) -> bool:
    """Completes todo by ID. Returns True if successful."""
```

#### New Methods
```python
@staticmethod
def get_upcoming_tasks() -> List[Dict[str, Any]]:
    """
    Returns tasks from Upcoming list, organized by date.
    
    Returns:
    [
        {
            "date": "2024-12-20",  # Or "Tomorrow"
            "tasks": [
                {"id": "...", "title": "...", ...}
            ]
        }
    ]
    """

@staticmethod
def get_anytime_tasks() -> List[Dict[str, Any]]:
    """
    Returns unscheduled active tasks, organized by project/area.
    
    Returns:
    {
        "loose_tasks": [{"id": "...", "title": "...", ...}],
        "projects": {
            "Project Name": [{"id": "...", "title": "...", ...}]
        }
    }
    """

@staticmethod
def get_today_count() -> int:
    """Returns count of tasks in Today list for overload warnings."""
```

### 🛡️ Error Handling Specifications

#### Auth Token Errors
```python
# Missing token
if not auth_token:
    return [types.TextContent(
        type="text", 
        text="""❌ Authentication Required

The THINGS3_AUTH_TOKEN environment variable is not set.

To get your token:
1. Open Things3
2. Go to Settings → General → Enable Things URLs → Manage
3. Copy your token
4. Set environment variable: export THINGS3_AUTH_TOKEN="your-token-here"

Note: Each device has its own token."""
    )]
```

#### ID Not Found
```python
# When update/complete fails
return [types.TextContent(
    type="text",
    text=f"""❌ Todo not found with ID: {todo_id}

This might happen if:
• The todo was deleted
• The ID was copied incorrectly
• The todo is in Trash/Logbook

Try searching for the task first:
- Use 'search-things3-todos' with keywords from the title"""
)]
```

### 🔍 Data Validation Rules

1. **Date Validation**:
   - Accept: `YYYY-MM-DD`, `today`, `tomorrow`, `evening`, `anytime`, `someday`
   - Evening times: `evening@HH:MM` or `evening@HPM`
   - Empty string `""` = clear date
   - `null` in JSON = keep unchanged

2. **Tag Validation**:
   - Strip whitespace from each tag
   - Empty tags array = clear all tags
   - Non-existent tags are ignored by Things3

3. **Checklist Validation**:
   - Max 100 items
   - Each item max 1000 chars
   - Empty array = clear checklist

4. **ID Format**:
   - Must match pattern: `[A-Za-z0-9-]{22,}`
   - No validation on checksum - Things3 will reject invalid

### 🎯 Smart Response Logic

#### For `update-things3-todo`:
```python
# After successful update
response_parts = [f"✅ Updated '{task_title}'"]

# Check for overload if scheduled for today
if arguments.get("when") == "today":
    today_count = AppleScriptHandler.get_today_count()
    if today_count > 4:
        response_parts.append(f"\n⚠️ Today now has {today_count} items. Stay focused on what's truly important today.")

# Explain deadline behavior
if arguments.get("deadline") and not arguments.get("when"):
    response_parts.append("\n💡 Task remains in Anytime (active but unscheduled) since only deadline was set. It will show a countdown but won't appear in Today until you explicitly schedule it.")

# Warn about someday
if arguments.get("when") == "someday":
    response_parts.append("\n📦 Moved to Someday - this task won't appear in active lists until you're ready to act on it.")

return [types.TextContent(type="text", text="\n".join(response_parts))]
```

### 🔄 State Management

Since MCP is stateless, each operation must:
1. Never assume previous context
2. Always return IDs for subsequent operations
3. Include enough info in responses for follow-up actions
4. Guide users to discover IDs before updates

### 📱 Environment Configuration

```python
# At server startup
auth_token = os.environ.get("THINGS3_AUTH_TOKEN")
if auth_token:
    logger.info("Things3 auth token configured")
else:
    logger.warning("THINGS3_AUTH_TOKEN not set - update operations will fail")

# For development with .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not required in production
```

