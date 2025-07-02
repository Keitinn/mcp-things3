# Things3 MCP Quick Reference

## 🎯 Essential Commands

### Discovery (No ID needed)
```
view-inbox                 # Unprocessed items
view-todos                 # Today list (with overload warning)
view-upcoming              # Future scheduled tasks
view-anytime               # Unscheduled active tasks  
view-projects              # All projects
search-things3-todos       # Find by keyword
```

### Creation
```
create-things3-todo
  title*                   # Required
  notes, when, deadline    # Optional
  tags: ["tag1", "tag2"]   # Array
  checklist: ["item1"]     # Array
  list: "Project Name"     # String

create-things3-project
  title*, notes, area      # Similar to todos
  when, deadline, tags     # Projects can be scheduled too
```

### Modification (Needs ID)
```
update-things3-todo
  id*                      # Required - get from search/view
  title, notes, when       # Any field to update
  deadline, tags, list     # Sparse updates
  checklist                # Full replacement
  completed: true/false    # Status changes
  canceled: true/false

complete-things3-todo
  id*                      # Just marks as done
```

## 📅 When Field Values

```
"today"                    # Today list
"tomorrow"                 # Tomorrow
"evening"                  # This Evening section
"evening@6pm"              # Evening with reminder
"2024-12-25"              # Specific date → Upcoming
"anytime"                  # Anytime list (unscheduled)
"someday"                  # Someday list (not actionable)
""                         # Empty string = clear date
null                       # No change (for updates)
```

## 🏷️ Special List IDs for 'show'

```
inbox, today, anytime, upcoming, someday, logbook,
tomorrow, deadlines, repeating, all-projects, logged-projects
```

## ⚡ Common Workflows

### Daily Review
1. `view-todos` → See Today (get warned if >4)
2. `view-upcoming` → Check what's coming
3. `view-anytime` → Pick tasks to schedule

### Task Management
1. `search-things3-todos query="dentist"` → Find task
2. Note the ID from results
3. `update-things3-todo id="..." when="next monday"`

### Clear Overloaded Today
1. `view-todos` → See all Today tasks with IDs
2. For each non-priority:
   `update-things3-todo id="..." when=""` → Back to Anytime

### Project Creation
```
create-things3-project 
  title="Website Redesign"
  area="Work"
  deadline="2024-03-31"
  tags=["q1", "priority"]
```

## 💡 Philosophy Reminders

- **Today = Commitment**, not wishlist (max 4-7 items)
- **Anytime = Default** for most tasks
- **Deadlines ≠ Scheduling** (stay in Anytime)
- **When stuck**: Clear date > Reschedule
- **Include joy**: Not just obligations

## 🚨 Auth Token Setup

```bash
# Get from Things3 → Settings → General → Enable Things URLs → Manage
export THINGS3_AUTH_TOKEN="your-token-here"
```

Without this, update operations will fail!