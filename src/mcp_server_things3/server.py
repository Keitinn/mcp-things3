import asyncio
import logging
import os
import subprocess
import sys
from urllib.parse import quote

import mcp.types as types
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio

# Handle both relative and absolute imports
try:
    from .applescript_handler import AppleScriptHandler
except ImportError:
    from applescript_handler import AppleScriptHandler

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to load .env file for development
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not required in production

# Check for auth token at startup
auth_token = os.environ.get("THINGS3_AUTH_TOKEN")
if auth_token:
    logger.info("Things3 auth token configured")
else:
    logger.warning("THINGS3_AUTH_TOKEN not set - update operations will fail")

# Initialize the server
server = Server("mcp-server-things3")

class XCallbackURLHandler:
    """Handles x-callback-url execution for Things3."""

    @staticmethod
    def build_url(base_url: str, params: dict) -> str:
        """
        Builds a properly encoded x-callback-url.
        """
        if not params:
            return base_url
        
        encoded_params = []
        for key, value in params.items():
            if value is not None:
                # Handle list values (like tags)
                if isinstance(value, list):
                    value = ",".join(str(v) for v in value)
                # Use quote() instead of quote_plus() - Things3 prefers %20 over +
                encoded_params.append(f"{key}={quote(str(value), safe='')}")
        
        return f"{base_url}?{'&'.join(encoded_params)}"

    @staticmethod
    def call_url(url: str) -> str:
        """
        Executes an x-callback-url using the 'open' command.
        """
        try:
            result = subprocess.run(
                ['open', url],
                check=True,
                capture_output=True,
                text=True
            )
            return result.stdout
        except FileNotFoundError:
            logger.error("'open' command not found")
            raise RuntimeError("Failed to execute x-callback-url: 'open' command not found")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to execute x-callback-url: {e}")
            raise RuntimeError(f"Failed to execute x-callback-url: {e}")
    
    @staticmethod
    def validate_things3_available() -> bool:
        """
        Check if Things3 is available on the system.
        """
        try:
            result = subprocess.run(
                ['osascript', '-e', 'tell application "System Events" to exists application process "Things3"'],
                check=True,
                capture_output=True,
                text=True
            )
            return result.stdout.strip() == "true"
        except subprocess.CalledProcessError:
            return False

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    List available Things3 tools.
    """
    return [
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
        ),
        types.Tool(
            name="view-inbox",
            description="View all todos in the Things3 inbox",
            inputSchema={
                "type": "object",
                "properties": {},
                "additionalProperties": False
            },
        ),
        types.Tool(
            name="view-projects",
            description="View all projects in Things3",
            inputSchema={
                "type": "object",
                "properties": {},
                "additionalProperties": False
            },
        ),
        types.Tool(
            name="view-todos",
            description="View all todos in Things3",
            inputSchema={
                "type": "object",
                "properties": {},
                "additionalProperties": False
            },
        ),
        types.Tool(
            name="create-things3-project",
            description="Create a new project in Things3",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "notes": {"type": "string"},
                    "area": {"type": "string"},
                    "when": {"type": "string"},
                    "deadline": {"type": "string"},
                    "tags": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["title"]
            },
        ),
        types.Tool(
            name="create-things3-todo",
            description="Create a new to-do in Things3",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "notes": {"type": "string"},
                    "when": {"type": "string"},
                    "deadline": {"type": "string"},
                    "checklist": {"type": "array", "items": {"type": "string"}},
                    "tags": {"type": "array", "items": {"type": "string"}},
                    "list": {"type": "string"},
                    "heading": {"type": "string"},
                },
                "required": ["title"]
            },
        ),
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
        ),
        types.Tool(
            name="search-things3-todos",
            description="Search for todos in Things3 by title or content",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search term to look for in todo titles and notes"},
                },
                "required": ["query"]
            },
        ),
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
        ),
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
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    Handle tool execution requests.
    """
    try:
        if name == "update-things3-todo":
            if not arguments:
                raise ValueError("Missing arguments")
            
            # Get auth token
            auth_token = os.environ.get("THINGS3_AUTH_TOKEN")
            if not auth_token:
                return [types.TextContent(type="text", text="""❌ Authentication Required

The THINGS3_AUTH_TOKEN environment variable is not set.

To get your token:
1. Open Things3
2. Go to Settings → General → Enable Things URLs → Manage
3. Copy your token
4. Set environment variable: export THINGS3_AUTH_TOKEN="your-token-here"

Note: Each device has its own token.""")]
            
            # Validate Things3 is available
            if not XCallbackURLHandler.validate_things3_available():
                return [
                    types.TextContent(
                        type="text",
                        text="Things3 is not running or not installed. Please start Things3 and try again.",
                    )
                ]
            
            # Build URL with special handling for empty strings
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
            
            url = XCallbackURLHandler.build_url(base_url, params)
            logger.info(f"Updating todo with URL: {url}")
            
            try:
                XCallbackURLHandler.call_url(url)
                
                # Build smart response
                response_parts = [f"✅ Updated todo"]
                
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
            except Exception as e:
                logger.error(f"Error updating todo: {e}")
                return [
                    types.TextContent(
                        type="text",
                        text=f"Failed to update todo: {str(e)}",
                    )
                ]
        
        if name == "view-inbox":
            # Validate Things3 is accessible
            if not AppleScriptHandler.validate_things3_access():
                return [types.TextContent(type="text", text="Things3 is not available. Please ensure Things3 is installed and running.")]
            
            try:
                todos = AppleScriptHandler.get_inbox_tasks() or []
                if not todos:
                    return [types.TextContent(type="text", text="No todos found in Things3 inbox.")]

                response = ["Todos in Things3 inbox:"]
                for todo in todos:
                    todo_id = todo.get("id", "")
                    title = (todo.get("title", "Untitled Todo")).strip()
                    tags = todo.get("tags", "")
                    
                    # Build response line
                    line = f"\n• {title}"
                    if tags:
                        line += f" #{tags.replace(',', ' #')}"
                    line += f" (id: {todo_id})"
                    
                    response.append(line)

                return [types.TextContent(type="text", text="\n".join(response))]
            except Exception as e:
                logger.error(f"Error retrieving inbox tasks: {e}")
                return [types.TextContent(type="text", text=f"Failed to retrieve inbox tasks: {str(e)}")]

        if name == "view-projects":
            # Validate Things3 is accessible
            if not AppleScriptHandler.validate_things3_access():
                return [types.TextContent(type="text", text="Things3 is not available. Please ensure Things3 is installed and running.")]
            
            try:
                projects = AppleScriptHandler.get_projects() or []
                if not projects:
                    return [types.TextContent(type="text", text="No projects found in Things3.")]

                response = ["Projects in Things3:"]
                for project in projects:
                    project_id = project.get("id", "")
                    title = (project.get("title", "Untitled Project")).strip()
                    response.append(f"\n• {title} (id: {project_id})")

                return [types.TextContent(type="text", text="\n".join(response))]
            except Exception as e:
                logger.error(f"Error retrieving projects: {e}")
                return [types.TextContent(type="text", text=f"Failed to retrieve projects: {str(e)}")]

        if name == "view-todos":
            # Validate Things3 is accessible
            if not AppleScriptHandler.validate_things3_access():
                return [types.TextContent(type="text", text="Things3 is not available. Please ensure Things3 is installed and running.")]
            
            try:
                todos = AppleScriptHandler.get_todays_tasks() or []
                if not todos:
                    return [types.TextContent(type="text", text="No todos found in Things3.")]

                # Check for overload
                todo_count = len(todos)
                if todo_count > 4:
                    response = [f"⚠️ Today's Focus ({todo_count} items - consider reviewing):"]
                else:
                    response = [f"Today's Focus ({todo_count} items):"]
                
                for todo in todos:
                    todo_id = todo.get("id", "")
                    title = (todo.get("title", "Untitled Todo")).strip()
                    tags = todo.get("tags", "")
                    
                    # Build response line
                    line = f"\n• {title}"
                    if tags:
                        line += f" #{tags.replace(',', ' #')}"
                    line += f" (id: {todo_id})"
                    
                    response.append(line)
                
                if todo_count > 4:
                    response.append("\n💡 Today has more than 4 items. Consider:")
                    response.append("• Which are truly TODAY vs. nice-to-have?")
                    response.append("• Move flexible items to Anytime (update with when='')")
                    response.append("• Use Evening section for time-specific tasks")

                return [types.TextContent(type="text", text="\n".join(response))]
            except Exception as e:
                logger.error(f"Error retrieving todos: {e}")
                return [types.TextContent(type="text", text=f"Failed to retrieve todos: {str(e)}")]

        if name == "create-things3-project":
            if not arguments:
                raise ValueError("Missing arguments")

            # Validate Things3 is available
            if not XCallbackURLHandler.validate_things3_available():
                return [
                    types.TextContent(
                        type="text",
                        text="Things3 is not running or not installed. Please start Things3 and try again.",
                    )
                ]

            # Build the Things3 URL with proper encoding
            base_url = "things:///add-project"
            params = {
                "title": arguments["title"]
            }
            
            # Optional parameters
            if "notes" in arguments:
                params["notes"] = arguments["notes"]
            if "area" in arguments:
                params["area"] = arguments["area"]
            if "when" in arguments:
                params["when"] = arguments["when"]
            if "deadline" in arguments:
                params["deadline"] = arguments["deadline"]
            if "tags" in arguments:
                params["tags"] = arguments["tags"]
            
            url = XCallbackURLHandler.build_url(base_url, params)
            logger.info(f"Creating project with URL: {url}")
            
            try:
                XCallbackURLHandler.call_url(url)
                return [
                    types.TextContent(
                        type="text",
                        text=f"Created project '{arguments['title']}' in Things3",
                    )
                ]
            except Exception as e:
                logger.error(f"Error creating project: {e}")
                return [
                    types.TextContent(
                        type="text",
                        text=f"Failed to create project in Things3: {str(e)}",
                    )
                ]

        if name == "create-things3-todo":
            if not arguments:
                raise ValueError("Missing arguments")

            # Validate Things3 is available
            if not XCallbackURLHandler.validate_things3_available():
                return [
                    types.TextContent(
                        type="text",
                        text="Things3 is not running or not installed. Please start Things3 and try again.",
                    )
                ]

            # Build the Things3 URL with proper encoding
            base_url = "things:///add"
            params = {
                "title": arguments["title"]
            }
            
            # Optional parameters
            if "notes" in arguments:
                params["notes"] = arguments["notes"]
            if "when" in arguments:
                params["when"] = arguments["when"]
            if "deadline" in arguments:
                params["deadline"] = arguments["deadline"]
            if "checklist" in arguments:
                params["checklist"] = "\n".join(arguments["checklist"])
            if "tags" in arguments:
                params["tags"] = arguments["tags"]
            if "list" in arguments:
                params["list"] = arguments["list"]
            if "heading" in arguments:
                params["heading"] = arguments["heading"]
            
            url = XCallbackURLHandler.build_url(base_url, params)
            logger.info(f"Creating todo with URL: {url}")
            
            try:
                XCallbackURLHandler.call_url(url)
                return [
                    types.TextContent(
                        type="text",
                        text=f"Created to-do '{arguments['title']}' in Things3",
                    )
                ]
            except Exception as e:
                logger.error(f"Error creating todo: {e}")
                return [
                    types.TextContent(
                        type="text",
                        text=f"Failed to create to-do in Things3: {str(e)}",
                    )
                ]

        if name == "complete-things3-todo":
            if not arguments:
                raise ValueError("Missing arguments")

            # Validate Things3 is available
            if not AppleScriptHandler.validate_things3_access():
                return [
                    types.TextContent(
                        type="text",
                        text="Things3 is not available. Please ensure Things3 is installed and running.",
                    )
                ]

            try:
                todo_id = arguments["id"]
                success = AppleScriptHandler.complete_todo_by_id(todo_id)
                if success:
                    return [
                        types.TextContent(
                            type="text",
                            text=f"✅ Successfully completed todo",
                        )
                    ]
                else:
                    return [
                        types.TextContent(
                            type="text",
                            text=f"""❌ Todo not found with ID: {todo_id}

This might happen if:
• The todo was deleted
• The ID was copied incorrectly
• The todo is in Trash/Logbook

Try searching for the task first:
- Use 'search-things3-todos' with keywords from the title""",
                        )
                    ]
            except Exception as e:
                logger.error(f"Error completing todo: {e}")
                return [
                    types.TextContent(
                        type="text",
                        text=f"Failed to complete todo: {str(e)}",
                    )
                ]

        if name == "search-things3-todos":
            if not arguments:
                raise ValueError("Missing arguments")

            # Validate Things3 is available
            if not AppleScriptHandler.validate_things3_access():
                return [
                    types.TextContent(
                        type="text",
                        text="Things3 is not available. Please ensure Things3 is installed and running.",
                    )
                ]

            try:
                todos = AppleScriptHandler.search_todos(arguments["query"])
                if not todos:
                    return [
                        types.TextContent(
                            type="text",
                            text=f"No todos found matching '{arguments['query']}'",
                        )
                    ]

                response = [f"Found {len(todos)} todo(s) matching '{arguments['query']}':"]
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

                return [types.TextContent(type="text", text="\n".join(response))]
            except Exception as e:
                logger.error(f"Error searching todos: {e}")
                return [
                    types.TextContent(
                        type="text",
                        text=f"Failed to search todos: {str(e)}",
                    )
                ]

        if name == "view-upcoming":
            # Validate Things3 is accessible
            if not AppleScriptHandler.validate_things3_access():
                return [types.TextContent(type="text", text="Things3 is not available. Please ensure Things3 is installed and running.")]
            
            try:
                tasks = AppleScriptHandler.get_upcoming_tasks() or []
                if not tasks:
                    return [types.TextContent(type="text", text="No upcoming scheduled tasks in Things3.")]

                response = ["Upcoming scheduled tasks in Things3:"]
                response.append("\n💡 These tasks are hibernating until their scheduled date arrives.")
                
                # Group tasks by date
                from datetime import datetime, timedelta
                today = datetime.now().date()
                tomorrow = today + timedelta(days=1)
                next_week = today + timedelta(days=7)
                
                tomorrow_tasks = []
                this_week_tasks = []
                later_tasks = []
                
                for task in tasks:
                    when_str = task.get("when", "")
                    # Simple date parsing - in production might need better handling
                    if "Tomorrow" in when_str:
                        tomorrow_tasks.append(task)
                    else:
                        # For now, just put everything in this week
                        this_week_tasks.append(task)
                
                if tomorrow_tasks:
                    response.append("\n📅 Tomorrow:")
                    for task in tomorrow_tasks:
                        todo_id = task.get("id", "")
                        title = task.get("title", "Untitled")
                        tags = task.get("tags", "")
                        list_name = task.get("list", "")
                        
                        line = f"  • {title}"
                        if list_name:
                            line += f" [{list_name}]"
                        if tags:
                            line += f" #{tags.replace(',', ' #')}"
                        line += f" (id: {todo_id})"
                        response.append(line)
                
                if this_week_tasks:
                    response.append("\n📅 This Week:")
                    for task in this_week_tasks:
                        todo_id = task.get("id", "")
                        title = task.get("title", "Untitled")
                        tags = task.get("tags", "")
                        list_name = task.get("list", "")
                        when_date = task.get("when", "")
                        
                        line = f"  • {title}"
                        if list_name:
                            line += f" [{list_name}]"
                        if tags:
                            line += f" #{tags.replace(',', ' #')}"
                        line += f" (id: {todo_id})"
                        response.append(line)

                return [types.TextContent(type="text", text="\n".join(response))]
            except Exception as e:
                logger.error(f"Error retrieving upcoming tasks: {e}")
                return [types.TextContent(type="text", text=f"Failed to retrieve upcoming tasks: {str(e)}")]

        if name == "view-anytime":
            # Validate Things3 is accessible
            if not AppleScriptHandler.validate_things3_access():
                return [types.TextContent(type="text", text="Things3 is not available. Please ensure Things3 is installed and running.")]
            
            try:
                tasks = AppleScriptHandler.get_anytime_tasks() or []
                if not tasks:
                    return [types.TextContent(type="text", text="No anytime tasks in Things3.")]

                response = ["Anytime tasks in Things3:"]
                response.append("\n💡 These active tasks are ready whenever you are. Pull to Today as capacity allows.")
                
                # Group by project/area
                loose_tasks = []
                by_project = {}
                
                for task in tasks:
                    list_name = task.get("list", "")
                    if list_name:
                        if list_name not in by_project:
                            by_project[list_name] = []
                        by_project[list_name].append(task)
                    else:
                        loose_tasks.append(task)
                
                # Show loose tasks first
                if loose_tasks:
                    response.append("\n📌 No Project/Area:")
                    for task in loose_tasks:
                        todo_id = task.get("id", "")
                        title = task.get("title", "Untitled")
                        tags = task.get("tags", "")
                        due_date = task.get("due_date", "")
                        
                        line = f"  • {title}"
                        if due_date and due_date != "missing value":
                            line += f" ⚠️ Due: {due_date.split(',')[0]}"  # Simple date format
                        if tags:
                            line += f" #{tags.replace(',', ' #')}"
                        line += f" (id: {todo_id})"
                        response.append(line)
                
                # Show tasks by project
                for project_name, project_tasks in sorted(by_project.items()):
                    response.append(f"\n📁 {project_name}:")
                    for task in project_tasks:
                        todo_id = task.get("id", "")
                        title = task.get("title", "Untitled")
                        tags = task.get("tags", "")
                        due_date = task.get("due_date", "")
                        
                        line = f"  • {title}"
                        if due_date and due_date != "missing value":
                            line += f" ⚠️ Due: {due_date.split(',')[0]}"
                        if tags:
                            line += f" #{tags.replace(',', ' #')}"
                        line += f" (id: {todo_id})"
                        response.append(line)

                return [types.TextContent(type="text", text="\n".join(response))]
            except Exception as e:
                logger.error(f"Error retrieving anytime tasks: {e}")
                return [types.TextContent(type="text", text=f"Failed to retrieve anytime tasks: {str(e)}")]

        raise ValueError(f"Unknown tool: {name}")

    except Exception as e:
        logger.error(f"Error handling tool {name}: {e}")
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]

async def main():
    """Run the server."""
    logger.info("Starting Things3 MCP server...")
    
    # Handle graceful shutdown
    def handle_signal(signum, frame):
        logger.info("Shutting down gracefully...")
        raise SystemExit(0)

    import signal
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    # Run the server using stdin/stdout streams
    try:
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="mcp-server-things3",
                    server_version="0.1.0",
                    capabilities=server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )
    except SystemExit:
        pass
    except Exception as e:
        logger.error(f"Server error: {e}")
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())