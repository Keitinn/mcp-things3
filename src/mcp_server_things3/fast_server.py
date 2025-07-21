"""FastMCP implementation of Things3 MCP server."""

import os
import logging
from fastmcp import FastMCP

# Try to import relative, fall back to absolute for testing
try:
    from .applescript_handler import AppleScriptHandler
    from .config import Settings
except ImportError:
    from applescript_handler import AppleScriptHandler
    from config import Settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load .env file for development
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Create settings instance from environment
settings = Settings()

# Validate auth token on startup if provided
if settings.auth_token:
    logger.info("✅ Things3 auth token configured - update operations available")
else:
    logger.warning("⚠️ No auth token configured - update operations will fail")
    logger.info("To configure: Set THINGS3_AUTH_TOKEN environment variable")

# Create FastMCP app
mcp = FastMCP(
    name="mcp-server-things3-fast",
    instructions="""This server provides access to Things3 task management on macOS.
    
Authentication: Some operations require a Things3 auth token. Set THINGS3_AUTH_TOKEN 
environment variable or pass it in the Claude Desktop config."""
)

@mcp.tool
def check_auth_status() -> str:
    """
    Check if Things3 authentication is configured.
    
    This tool helps verify that the auth token is properly configured
    via environment variable.
    """
    if settings.is_authenticated:
        return "✅ Things3 authentication is configured. Update operations will work."
    else:
        return """❌ Authentication not configured.

To configure authentication:
1. Via environment variable: export THINGS3_AUTH_TOKEN="your-token"
2. Via Claude Desktop config: Add to env section

To get your token:
1. Open Things3
2. Go to Settings → General → Enable Things URLs → Manage
3. Copy your token (device-specific)"""


@mcp.tool(name="view-projects")
def view_projects() -> str:
    """View all projects in Things3"""
    try:
        # Validate Things3 is accessible
        if not AppleScriptHandler.validate_things3_access():
            return "Things3 is not available. Please ensure Things3 is installed and running."
        
        projects = AppleScriptHandler.get_projects() or []
        if not projects:
            return "No projects found in Things3."

        response = ["Projects in Things3:"]
        for project in projects:
            project_id = project.get("id", "")
            title = project.get("title", "Untitled Project").strip()
            response.append(f"\n• {title} (id: {project_id})")

        return "\n".join(response)
    except Exception as e:
        logger.error(f"Error retrieving projects: {e}")
        return f"Failed to retrieve projects: {str(e)}"

@mcp.tool(name="view-todos")
def view_todos(list_name: str = "Today") -> str:
    """View todos from a specific Things3 list.
    
    Args:
        list_name: The list to view todos from. Valid options:
                  - Today (default): Tasks scheduled for today
                  - Inbox: Unprocessed tasks
                  - Anytime: Tasks without specific scheduling
                  - Upcoming: Tasks scheduled for future dates
                  - Someday: Tasks deferred indefinitely
                  - Logbook: Completed and canceled tasks
                  - Trash: Deleted tasks
    
    PHILOSOPHY BY LIST:
    
    Today:
    • For focused commitments, not wishlists (max ~4 items)
    • Tasks appear here on their scheduled date
    • If overloaded, move flexible items to Anytime
    
    Inbox:
    • For capture, not storage - process regularly
    • Decide: do it, delegate it, defer it, or delete it
    • Goal is inbox zero, not inbox storage
    
    Anytime:
    • Most tasks should live here - ready when you are
    • Having many tasks in Anytime is normal and good
    • Pull from here to Today as capacity allows
    • Tasks with deadlines (but no when date) stay here
    • Deadlines ≠ scheduling
    
    Upcoming:
    • Tasks scheduled for specific future dates (hibernating)
    • For "I can't/won't start this until X date"
    • Not everything needs a date - resist scheduling for scheduling's sake
    • Does NOT include tasks with deadlines but no start date
    
    Examples:
    - view_todos() - Shows Today list
    - view_todos("Inbox") - Shows unprocessed tasks
    - view_todos("Anytime") - Shows active unscheduled tasks
    - view_todos("Upcoming") - Shows future scheduled tasks
    """
    try:
        # Validate Things3 is accessible
        if not AppleScriptHandler.validate_things3_access():
            return "Things3 is not available. Please ensure Things3 is installed and running."
        
        todos = AppleScriptHandler.get_tasks_from_list(list_name) or []
        if not todos:
            return f"No todos found in {list_name} list."

        # Check for overload and set appropriate header
        todo_count = len(todos)
        if list_name == "Today":
            if todo_count > 4:
                response = [f"⚠️ Today's Focus ({todo_count} items - consider reviewing):"]
            else:
                response = [f"Today's Focus ({todo_count} items):"]
        elif list_name == "Inbox":
            response = [f"Inbox ({todo_count} items):"]
        elif list_name == "Anytime":
            response = [f"Anytime tasks ({todo_count} items):"]
            response.append("💡 These active tasks are ready whenever you are. Pull to Today as capacity allows.")
        elif list_name == "Upcoming":
            response = [f"Upcoming scheduled tasks ({todo_count} items):"]
            response.append("💡 These tasks are hibernating until their scheduled date arrives.")
        else:
            response = [f"{list_name} ({todo_count} items):"]
        
        # Special formatting for Anytime list (group by project/area)
        if list_name == "Anytime":
            # Group by project/area
            loose_tasks = []
            by_project = {}
            
            for task in todos:
                project_name = task.get("list", "")
                if project_name:
                    if project_name not in by_project:
                        by_project[project_name] = []
                    by_project[project_name].append(task)
                else:
                    loose_tasks.append(task)
            
            # Show loose tasks first
            if loose_tasks:
                response.append("\n📌 No Project/Area:")
                for task in loose_tasks:
                    todo_id = task.get("id", "")
                    title = task.get("title", "Untitled Todo").strip()
                    tags = task.get("tags", "")
                    due_date = task.get("due_date", "")
                    
                    line = f"  • {title}"
                    if due_date and due_date != "missing value" and due_date != "":
                        line += f" ⚠️ Due: {due_date.split(',')[0]}"
                    if tags:
                        line += f" #{tags.replace(',', ' #')}"
                    line += f" (id: {todo_id})"
                    response.append(line)
            
            # Show tasks by project
            for project_name, project_tasks in sorted(by_project.items()):
                response.append(f"\n📁 {project_name}:")
                for task in project_tasks:
                    todo_id = task.get("id", "")
                    title = task.get("title", "Untitled Todo").strip()
                    tags = task.get("tags", "")
                    due_date = task.get("due_date", "")
                    
                    line = f"  • {title}"
                    if due_date and due_date != "missing value" and due_date != "":
                        line += f" ⚠️ Due: {due_date.split(',')[0]}"
                    if tags:
                        line += f" #{tags.replace(',', ' #')}"
                    line += f" (id: {todo_id})"
                    response.append(line)
        else:
            # Standard formatting for other lists
            for todo in todos:
                todo_id = todo.get("id", "")
                title = todo.get("title", "Untitled Todo").strip()
                tags = todo.get("tags", "")
                due_date = todo.get("due_date", "")
                project_name = todo.get("list", "")
                
                # Build response line
                line = f"\n• {title}"
                
                # Add project/area for Upcoming list
                if list_name == "Upcoming" and project_name:
                    line += f" [{project_name}]"
                
                # Add due date if present (except for Anytime which handles it above)
                if due_date and due_date != "missing value" and due_date != "" and list_name != "Anytime":
                    line += f" ⚠️ Due: {due_date.split(',')[0]}"
                    
                if tags:
                    line += f" #{tags.replace(',', ' #')}"
                line += f" (id: {todo_id})"
                
                response.append(line)
        
        # Add philosophy reminders for specific lists
        if list_name == "Today" and todo_count > 4:
            response.append("\n💡 Today has more than 4 items. Consider:")
            response.append("• Which are truly TODAY vs. nice-to-have?")
            response.append("• Move flexible items to Anytime (update with when='')")
            response.append("• Use Evening section for time-specific tasks")
        elif list_name == "Inbox" and todo_count > 10:
            response.append("\n💡 Tip: Process your inbox - decide, don't just collect")
        
        return "\n".join(response)
    except ValueError as e:
        return str(e)
    except Exception as e:
        logger.error(f"Error retrieving todos from {list_name}: {e}")
        return f"Failed to retrieve todos from {list_name}: {str(e)}"

@mcp.tool(name="search-things3-todos")
def search_things3_todos(query: str) -> str:
    """Search for todos in Things3 by title or content"""
    try:
        # Validate Things3 is accessible
        if not AppleScriptHandler.validate_things3_access():
            return "Things3 is not available. Please ensure Things3 is installed and running."

        todos = AppleScriptHandler.search_todos(query)
        if not todos:
            return f"No todos found matching '{query}'"

        response = [f"Found {len(todos)} todo(s) matching '{query}':"]
        for todo in todos:
            todo_id = todo.get("id", "")
            title = todo.get("title", "Untitled Todo")
            status = todo.get("status", "unknown")
            tags = todo.get("tags", "")
            status_icon = "✅" if status == "completed" else "⏳"
            
            # Build response line
            line = f"\n{status_icon} {title}"
            if tags:
                line += f" #{tags.replace(',', ' #')}"
            line += f" (id: {todo_id})"
            
            response.append(line)

        return "\n".join(response)
    except Exception as e:
        logger.error(f"Error searching todos: {e}")
        return f"Failed to search todos: {str(e)}"

@mcp.tool(
    name="complete-things3-todo",
    description="""Mark a todo as completed. Requires the todo's ID (find it using search or view tools first).

NOTE: Completion is final - tasks move to Logbook. If you might need it again, consider:
• Rescheduling instead (update with when="tomorrow")
• Moving to Someday (update with when="someday")
• Adding a "waiting" tag instead"""
)
def complete_things3_todo(id: str) -> str:
    """Complete a todo by ID."""
    try:
        # Validate Things3 is accessible
        if not AppleScriptHandler.validate_things3_access():
            return "Things3 is not available. Please ensure Things3 is installed and running."

        success = AppleScriptHandler.complete_todo_by_id(id)
        if success:
            return "✅ Successfully completed todo"
        else:
            return f"""❌ Todo not found with ID: {id}

This might happen if:
• The todo was deleted
• The ID was copied incorrectly
• The todo is in Trash/Logbook

Try searching for the task first:
- Use 'search-things3-todos' with keywords from the title"""
    except Exception as e:
        logger.error(f"Error completing todo: {e}")
        return f"Failed to complete todo: {str(e)}"

@mcp.tool(name="create-things3-project")
def create_things3_project(
    title: str,
    notes: str = None,
    area: str = None,
    when: str = None,
    deadline: str = None,
    tags: list[str] = None
) -> str:
    """Create a new project in Things3"""
    try:
        # Validate Things3 is available
        if not AppleScriptHandler.validate_things3_access():
            return "Things3 is not running or not installed. Please start Things3 and try again."

        # Build the Things3 URL with proper encoding
        base_url = "things:///add-project"
        params = {"title": title}
        
        # Optional parameters
        if notes:
            params["notes"] = notes
        if area:
            params["area"] = area
        if when:
            params["when"] = when
        if deadline:
            params["deadline"] = deadline
        if tags:
            params["tags"] = tags
        
        url = build_things_url(base_url, params)
        logger.info(f"Creating project with URL: {url}")
        
        call_things_url(url)
        return f"Created project '{title}' in Things3"
    except Exception as e:
        logger.error(f"Error creating project: {e}")
        return f"Failed to create project in Things3: {str(e)}"

@mcp.tool(name="create-things3-todo")
def create_things3_todo(
    title: str,
    notes: str = None,
    when: str = None,
    deadline: str = None,
    checklist: list[str] = None,
    tags: list[str] = None,
    list: str = None,
    heading: str = None
) -> str:
    """Create a new to-do in Things3"""
    try:
        # Validate Things3 is available
        if not AppleScriptHandler.validate_things3_access():
            return "Things3 is not running or not installed. Please start Things3 and try again."

        # Build the Things3 URL with proper encoding
        base_url = "things:///add"
        params = {"title": title}
        
        # Optional parameters
        if notes:
            params["notes"] = notes
        if when:
            params["when"] = when
        if deadline:
            params["deadline"] = deadline
        if checklist:
            params["checklist"] = "\n".join(checklist)
        if tags:
            params["tags"] = tags
        if list:
            params["list"] = list
        if heading:
            params["heading"] = heading
        
        url = build_things_url(base_url, params)
        logger.info(f"Creating todo with URL: {url}")
        
        call_things_url(url)
        return f"Created to-do '{title}' in Things3"
    except Exception as e:
        logger.error(f"Error creating todo: {e}")
        return f"Failed to create to-do in Things3: {str(e)}"

@mcp.tool(
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
• Use tags for priority rather than scheduling everything for today"""
)
def update_things3_todo(
    id: str,
    title: str = None,
    notes: str = None,
    when: str = None,
    deadline: str = None,
    tags: list[str] = None,
    checklist: list[str] = None,
    list: str = None,
    completed: bool = None,
    canceled: bool = None
) -> str:
    """Update an existing todo."""
    # Check auth token
    if not settings.is_authenticated:
        return """❌ Authentication Required

The THINGS3_AUTH_TOKEN environment variable is not set.

To get your token:
1. Open Things3
2. Go to Settings → General → Enable Things URLs → Manage
3. Copy your token
4. Set environment variable: export THINGS3_AUTH_TOKEN="your-token-here"

Note: Each device has its own token."""
    
    try:
        # Validate Things3 is available
        if not AppleScriptHandler.validate_things3_access():
            return "Things3 is not running or not installed. Please start Things3 and try again."
        
        # Build URL with special handling for empty strings
        base_url = "things:///update"
        params = {
            "id": id,
            "auth-token": settings.auth_token
        }
        
        # Handle fields that can be cleared with empty string
        if when is not None:
            params["when"] = when if when else ""
        if deadline is not None:
            params["deadline"] = deadline if deadline else ""
        
        # Normal fields
        if title is not None:
            params["title"] = title
        if notes is not None:
            params["notes"] = notes
        if tags is not None:
            params["tags"] = tags  # Will be joined with commas by build_url
        if checklist is not None:
            params["checklist-items"] = "\n".join(checklist)
        if list is not None:
            params["list"] = list
        if completed is not None:
            params["completed"] = str(completed).lower()
        if canceled is not None:
            params["canceled"] = str(canceled).lower()
        
        url = build_things_url(base_url, params)
        logger.info(f"Updating todo with URL: {url}")
        
        call_things_url(url)
        
        # Build smart response
        response_parts = ["✅ Updated todo"]
        
        # Check for overload if scheduled for today
        if when == "today":
            today_count = AppleScriptHandler.get_today_count()
            if today_count > 4:
                response_parts.append(f"\n⚠️ Today now has {today_count} items. Stay focused on what's truly important today.")
        
        # Explain deadline behavior
        if deadline and not when:
            response_parts.append("\n💡 Task remains in Anytime (active but unscheduled) since only deadline was set. It will show a countdown but won't appear in Today until you explicitly schedule it.")
        
        # Warn about someday
        if when == "someday":
            response_parts.append("\n📦 Moved to Someday - this task won't appear in active lists until you're ready to act on it.")
        
        return "\n".join(response_parts)
    except Exception as e:
        logger.error(f"Error updating todo: {e}")
        return f"Failed to update todo: {str(e)}"



# Main entry point for script
def main():
    """Main entry point for the FastMCP server."""
    mcp.run()

# Centralized X-Callback-URL handling
def build_things_url(base_url: str, params: dict) -> str:
    """Build a properly encoded Things3 URL."""
    if not params:
        return base_url
    
    from urllib.parse import quote
    encoded_params = []
    for key, value in params.items():
        if value is not None:
            # Handle list values (like tags)
            if isinstance(value, list):
                value = ",".join(str(v) for v in value)
            # Use quote() instead of quote_plus() - Things3 prefers %20 over +
            encoded_params.append(f"{key}={quote(str(value), safe='')}")
    
    return f"{base_url}?{'&'.join(encoded_params)}"

def call_things_url(url: str) -> None:
    """Execute a Things3 URL using the 'open' command."""
    import subprocess
    try:
        subprocess.run(['open', url], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to execute x-callback-url: {e}")

# Run the server
if __name__ == "__main__":
    main()