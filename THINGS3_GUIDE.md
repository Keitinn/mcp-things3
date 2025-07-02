# Things3 MCP Server Guide

## 🧠 Core Philosophy

### The Things3 Way
Things3 isn't just a task manager - it's a system for feeling in control. Key principles:

1. **Today is Sacred**: Max 4-7 items. It's your commitment, not a wishlist.
2. **Start ≠ Due**: Start dates control when you'll BEGIN. Deadlines control when you must FINISH.
3. **Embrace Constraints**: "Too much to do in one day" is normal. Design around this reality.
4. **Include Joy**: Add fun things too, or reviewing tasks becomes a chore.

### List Philosophy
- **Inbox**: Capture quickly, process later
- **Today**: Your focused commitments (not everything due)
- **Upcoming**: Tasks hibernating until their start date
- **Anytime**: Active tasks ready whenever you are (most tasks live here)
- **Someday**: Vague ideas without clear next actions

## 🔧 Using the MCP Server

### Quick Start
```bash
# Set your auth token (get from Things3 Settings → General → Enable Things URLs → Manage)
export THINGS3_AUTH_TOKEN="your-token-here"

# Configure Claude Desktop to use the server
# In ~/Library/Application Support/Claude/claude_desktop_config.json:
{
  "mcpServers": {
    "things3": {
      "command": "uv",
      "args": ["run", "mcp-server-things3"],
      "cwd": "/Users/darin/shit/mcp-things3"
    }
  }
}
```

### Essential Workflows

#### 1. Quick Capture
```
"Add a todo to buy milk"
"Create a project for planning Sarah's birthday party"
```

#### 2. Daily Review
```
"Show me today's tasks"
"What's in my upcoming list?"
"Show anytime tasks" (then pick what to schedule)
```

#### 3. Update Flow (Always Search First!)
```
"Search for presentation tasks"
→ Get IDs from results
"Update todo [ID] to start tomorrow"
"Complete todo [ID]"
```

#### 4. Smart Scheduling
```
"Update [ID] with when=''" ← Clears date, better than endless rescheduling
"Update [ID] with when='someday'" ← Not ready to act on this
"Update [ID] with deadline='2024-12-31'" ← Stays in Anytime with countdown
```

## 💡 Best Practices

### For Claude (AI) Using Things3

1. **Always Search Before Update**: You need IDs to modify anything
   ```
   User: "Postpone the dentist appointment"
   You: First search → "search-things3-todos query='dentist'"
   Then: "update-things3-todo id='[found-id]' when='tomorrow'"
   ```

2. **Respect Today's Sanctity**: Warn when Today > 4 tasks
3. **Suggest Anytime**: Most tasks should be unscheduled until truly needed
4. **Explain Deadline Behavior**: Tasks with deadlines stay in Anytime

### Common Patterns

#### The Overwhelmed Today
```
View today → 8+ tasks
Suggest: "Which 3-4 are true priorities?"
Action: Update others with when='' (move to Anytime)
```

#### The Stale Task
```
Task rescheduled 3+ times
Suggest: "Might this need breaking down or moving to Someday?"
```

#### The Deadline Task
```
User adds deadline but no start date
Explain: "This stays in Anytime with a countdown. Schedule it when ready to start."
```

## 🚦 Natural Language Date Examples

Things3 accepts (in English + 7 other languages):
- `today`, `tomorrow`, `evening`
- `next monday`, `this weekend`
- `in 3 days`, `2 weeks from today`
- `Dec 25`, `December 25th`
- `evening@6pm` (with reminder)

## ⚠️ Limitations & Workarounds

### Can't Do
- Access calendar events (Things3 shows them but API doesn't expose)
- Modify headings or repeating tasks
- Get checklist item IDs (only full replacement)
- True "unschedule" without auth token

### Workarounds
- No "Move to top of Today" → Advise manual drag in app
- No bulk operations → Loop with rate limit awareness
- No attachments → Suggest links in notes

## 🗺️ Architecture Notes

### Why AppleScript + URL Scheme?
- AppleScript: Read operations, ID access, selection context
- URL Scheme: Create/update operations, cross-platform
- Both needed for full functionality

### ID Format
- Tasks: 22-char alphanumeric (e.g., `2DCAbD81QBc6oQbzaNjFhM`)
- Lists: Either names ("Today") or IDs ("inbox")

## 🧘 The Things3 Mindset

Remember: Things3 is about **feeling in control**, not productivity porn. Features that seem missing (like complex priority systems) are intentionally simple. The goal is clarity about what to do next, not elaborate planning systems.

When helping users:
- Encourage regular reviews over perfect systems
- Suggest sustainable practices over optimization
- Respect that "good enough" task management that you actually use beats perfect systems you abandon

## 🔍 Debugging

### Common Issues
1. **"Things3 not available"** → Is Things3 running?
2. **"Auth token required"** → Check THINGS3_AUTH_TOKEN env var
3. **"Task not found"** → Task might be in Trash/Logbook
4. **Empty results** → Check list names match exactly

### Test Commands
```bash
# Test AppleScript access
osascript -e 'tell application "Things3" to return name of first to do'

# Test URL scheme
open "things:///version"

# Check auth token
echo $THINGS3_AUTH_TOKEN
```

---

*Last updated: January 2025*
*Based on Things3 URL Scheme v2 and extensive testing*