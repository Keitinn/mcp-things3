## 📚 Things3 MCP Server Knowledge Transfer

### 🧠 Things3 Philosophy & Core Concepts

#### List Semantics (Critical to Understand)
- **Today**: Curated daily commitments, NOT everything due today. Best with 3-7 items.
- **Upcoming**: Tasks scheduled for future dates that are "hibernating" until then
- **Anytime**: Active tasks without specific dates - ready to tackle whenever
- **Someday**: Vague ideas without clear next actions
- **Inbox**: Temporary holding for unprocessed items

#### Key Principles
1. **Start Date ≠ Deadline**: Start = "when will I begin?", Deadline = "when must I finish?"
2. **Tasks with deadlines stay in Anytime** until explicitly scheduled
3. **Projects can hibernate** - they hide from sidebar when scheduled for future
4. **Evening** is a subsection of Today for time-specific tasks

### 🔧 AppleScript Testing & Gotchas

#### Testing AppleScript Queries
```bash
# Test if Things3 exposes IDs
osascript -e 'tell application "Things3" to return id of first to do'

# Get all properties of a task
osascript -e 'tell application "Things3" to return properties of first to do'

# Test a specific list
osascript -e 'tell application "Things3" to return name of every to do of list "Upcoming"'
```

#### AppleScript Data Structures
- Things3 returns records like: `{title:"Buy milk", id:"UUID", due date:missing value}`
- `missing value` = null/undefined in AppleScript
- Dates come back as AppleScript date objects - need string conversion
- Lists come back as `{{record1}, {record2}}` format
- Empty results might be `{}` or `""` - handle both

#### Common AppleScript Errors
- "Invalid index" = list is empty or item doesn't exist
- Things3 must be running or AppleScript fails
- Some properties like `start date` might not exist on all objects
- Tag names return as comma-separated list, not array

### 🔗 URL Scheme Details

#### Auth Token
- Found in: Settings → General → Enable Things URLs → Manage
- Required for: `update`, `update-project`, and `json` (when updating)
- Format: Long alphanumeric string
- Different per device - user must get from their Things3

#### URL Construction Rules
- Use `%20` for spaces (not `+`)
- Parameters with empty values clear fields: `deadline=`
- Checklist items use `%0a` (newline) as separator
- Tags are comma-separated in single parameter
- Max 250 items per 10 seconds (rate limit)

#### Special `when` Values
```
"today"          → Today list
"tomorrow"       → Tomorrow (in Upcoming)
"evening"        → This Evening section
"evening@6pm"    → Evening with reminder
"anytime"        → Anytime list (clears date)
"someday"        → Someday list
"2024-12-25"     → Specific date (Upcoming)
""               → Clear date (same as null)
```

### 📊 Data Structure Patterns

#### Task ID Format
- UUIDs like: `2DCAbD81QBc6oQbzaNjFhM`
- Projects also have IDs: `Bsid9MD25LRKZbsUn2tn6o`
- Built-in lists use names: "Today", "Inbox", "Upcoming"
- Some built-in lists have IDs: "inbox", "today", "upcoming" (lowercase)

#### Task Properties Available
```
id                → Always exists
name              → Title of task
notes             → Can be missing value
status            → open/completed/canceled
due date          → AppleScript date or missing value
activation date   → When field (start date)
creation date     → When task was created
modification date → Last changed
completion date   → When marked done
tag names         → Comma-separated string or empty
project          → Reference to parent project
area             → Reference to parent area
```

### 🧪 Testing Approaches

#### Manual Testing Flow
1. Create test task via MCP
2. Search for it to get ID
3. Update it with various fields
4. Check in Things3 UI that changes applied
5. Complete it
6. Verify it moved to Logbook

#### Edge Cases to Test
- Empty Today list
- Today with 10+ items (overload)
- Tasks with unicode in titles
- Tasks with very long notes (10k chars)
- Tasks with both deadline and when date
- Moving tasks between projects
- Clearing dates (empty string vs null)

#### AppleScript Response Parsing
- The current `parse_applescript_record()` is fragile
- Consider using `osascript -ss` for better output format
- Watch for nested braces in task notes
- Handle both `{}` and `{{}}` for empty results

### ⚠️ Known Limitations

1. **AppleScript can't access**:
   - Headings
   - Individual checklist items
   - Repeating task details

2. **URL Scheme can't**:
   - Truly unschedule without auth token
   - Access task metadata (creation date, etc.)
   - Get task IDs back without JSON command

3. **Things3 Behaviors**:
   - Canceled vs Completed are different states
   - Can't complete project unless all children done
   - Quick Entry dialog is Mac-only
   - Natural language dates only in English

### 💡 User Experience Tips

1. **ID Discovery**: Users don't know IDs - always search/list first
2. **Overload Warnings**: Today > 4 items should trigger gentle warning
3. **Semantic Responses**: Say "moved to Anytime (unscheduled active tasks)" not just "updated"
4. **Error Recovery**: If task not found by ID, suggest searching
5. **Philosophy Reminders**: Update responses should reinforce good practices

### 🔒 Security & Config

- Auth token via environment variable: `THINGS3_AUTH_TOKEN`
- Never log auth token
- Validate Things3 is installed before operations
- URL encode all user input properly
- Handle missing auth token gracefully (some ops don't need it)

### 📱 Cross-Platform Differences

- Mac: Full AppleScript support
- Auth tokens are device-specific

