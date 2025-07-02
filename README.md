# MCP Server for Things3

A robust MCP (Model Context Protocol) server providing comprehensive integration with Things3, allowing you to create, manage, and search tasks and projects through the MCP protocol. Features ID-based task management, JSON-based AppleScript integration, and Things3 philosophy guidance.

## Features

- ✅ **Create Projects & Todos**: Full metadata support with checklists, tags, and dates
- ✅ **Update Tasks**: Modify any task property using task IDs with auth token support
- ✅ **View Tasks**: List tasks from Inbox, Today, Upcoming, Anytime, or Projects
- ✅ **Complete Tasks**: Mark todos as completed using their ID
- ✅ **Search Functionality**: Search through all todos by title or content
- ✅ **Things3 Philosophy**: Built-in guidance for effective task management
- ✅ **JSON Integration**: Reliable data extraction using Foundation framework
- ✅ **Today Overload Warning**: Alerts when Today list exceeds 4 items

## Installation

### Prerequisites
- macOS with Things3 installed
- Python 3.10+ 
- Things3 running (for real-time operations)
- Things3 auth token (for update operations)

### Install the Server

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd mcp-things3
   ```

2. Install using pip:
   ```bash
   pip install -e .
   ```

3. The server will be available as `mcp-server-things3`

### Auth Token Setup

For update operations, you need to set your Things3 auth token:

1. Open Things3
2. Go to Settings → General → Enable Things URLs → Manage
3. Copy your auth token
4. Set the environment variable:
   ```bash
   export THINGS3_AUTH_TOKEN="your-token-here"
   ```

## Tools Available

### View Operations

#### `view-inbox`
View all todos in the Things3 inbox.
- **Parameters**: None
- **Returns**: List of inbox todos with IDs, titles, tags, and metadata

#### `view-todos`
View all todos in today's list with overload warning.
- **Parameters**: None
- **Returns**: List of today's todos with IDs and warning if >4 items

#### `view-upcoming`
View scheduled future tasks in Things3's Upcoming list.
- **Parameters**: None
- **Returns**: Tasks organized by date, showing what's hibernating until scheduled

#### `view-anytime`
View all unscheduled active tasks in Things3's Anytime list.
- **Parameters**: None
- **Returns**: Tasks organized by project/area, ready whenever you are

#### `view-projects`
View all projects in Things3.
- **Parameters**: None  
- **Returns**: List of all projects with IDs and titles

### Creation Operations

#### `create-things3-project`
Creates a new project in Things3.
- **Required**: `title` (string)
- **Optional**: 
  - `notes` (string)
  - `area` (string) 
  - `when` (string) - Date/time to start
  - `deadline` (string) - Due date
  - `tags` (array of strings)

**Example**:
```json
{
  "title": "Website Redesign",
  "notes": "Complete overhaul of company website",
  "area": "Work",
  "deadline": "2024-03-15",
  "tags": ["urgent", "web-dev"]
}
```

#### `create-things3-todo`
Creates a new to-do in Things3.
- **Required**: `title` (string)
- **Optional**:
  - `notes` (string)
  - `when` (string) - Date/time to start  
  - `deadline` (string) - Due date
  - `checklist` (array of strings)
  - `tags` (array of strings)
  - `list` (string) - Project or area to assign to
  - `heading` (string) - Group under this heading

**Example**:
```json
{
  "title": "Review design mockups",
  "notes": "Check the new homepage designs",
  "list": "Website Redesign", 
  "deadline": "2024-02-20",
  "tags": ["review"],
  "checklist": ["Check mobile responsiveness", "Verify brand guidelines", "Test accessibility"]
}
```

### Management Operations

#### `update-things3-todo`
Update an existing to-do in Things3. Requires auth token.
- **Required**: `id` (string) - Todo ID from view/search results
- **Optional**: All todo fields (title, notes, when, deadline, tags, etc.)
- **Special**: `completed`, `canceled` (boolean) for status changes
- **Returns**: Success message with philosophical guidance

**Example**:
```json
{
  "id": "2DCAbD81QBc6oQbzaNjFhM",
  "when": "tomorrow",
  "tags": ["urgent", "review"]
}
```

#### `complete-things3-todo`
Mark a todo as completed using its ID.
- **Required**: `id` (string) - Todo ID from view/search results
- **Returns**: Success/failure message

**Example**:
```json
{
  "id": "2DCAbD81QBc6oQbzaNjFhM"
}
```

#### `search-things3-todos`
Search for todos by title or content.
- **Required**: `query` (string) - Search term
- **Returns**: List of matching todos with status and metadata

**Example**:
```json
{
  "query": "website"
}
```

## Integration with Claude

This MCP server is designed to work seamlessly with Claude AI. Once configured, you can use natural language to manage your Things3 tasks:

- "Create a project called 'Q1 Planning' with a deadline of March 31st"
- "Add a todo to review the budget with a checklist of tasks"
- "Show me all my tasks for today"
- "Mark the 'Call client' task as completed"
- "Search for all todos related to the website project"

## Configuration

### MCP Client Configuration

Add to your MCP client configuration (e.g., Claude Desktop config):

```json
{
  "mcpServers": {
    "things3": {
      "command": "mcp-server-things3",
      "args": []
    }
  }
}
```

### Things3 Setup

1. Ensure Things3 is installed and running
2. Grant necessary permissions when prompted for AppleScript access
3. The server will validate Things3 availability before operations

## Architecture

### Components

- **`server.py`**: Main MCP server implementation with tool definitions and handlers
- **`applescript_handler.py`**: AppleScript integration with JSON serialization via Foundation framework
- **`applescript/`**: Dedicated AppleScript files for each bulk operation using JSON output
- **URL Encoding**: Proper x-callback-url parameter encoding for special characters
- **Error Handling**: Comprehensive validation and graceful error recovery

### Key Features

- **JSON Serialization**: Uses macOS Foundation framework for reliable data extraction
- **ID-Based Operations**: All tasks tracked by unique IDs, not titles
- **Auth Token Support**: Environment variable for Things3 URL scheme authentication
- **Philosophy Integration**: Built-in guidance for effective Things3 usage
- **Bulk Operations**: Efficient retrieval of multiple items with proper JSON structure

## Development

### Testing

The server includes comprehensive logging for debugging. Individual tools can be tested through the MCP protocol once configured with your client.

### Debugging

The server includes comprehensive logging. Set log level for debugging:

```bash
export PYTHONPATH="."
python -c "
import logging
logging.basicConfig(level=logging.DEBUG)
from src.mcp_server_things3.server import main
import asyncio
asyncio.run(main())
"
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## Troubleshooting

### Common Issues

**"Things3 is not available"**
- Ensure Things3 is installed and running
- Grant AppleScript permissions when prompted
- Check Things3 is not in a permission-restricted mode

**"Failed to execute AppleScript"**
- Verify macOS security settings allow AppleScript
- Ensure Things3 has necessary accessibility permissions
- Try restarting Things3

**URL encoding issues with special characters**
- The server now properly handles unicode and special characters
- If issues persist, check the logs for specific URL construction errors

**"Authentication Required" for update operations**
- Ensure THINGS3_AUTH_TOKEN environment variable is set
- Get token from Things3 Settings → General → Enable Things URLs → Manage
- Each device has its own unique token

### Performance Notes

- AppleScript operations may have slight delays
- Large todo lists (1000+ items) may take longer to search
- Consider using specific searches rather than broad queries for better performance

## License

MIT License - see LICENSE file for details.

## Changelog

### v0.2.0
- Added `update-things3-todo` tool with auth token support
- Added `view-upcoming` and `view-anytime` tools
- Implemented JSON serialization using Foundation framework
- Changed to ID-based operations (no more title searching)
- Added Today overload warnings (>4 items)
- Added Things3 philosophy guidance in tool descriptions
- Updated Python requirement to 3.10+
- All responses now include task/project IDs

### v0.1.0
- Initial release with basic CRUD operations
- Comprehensive error handling and validation
- Secure URL encoding and AppleScript integration
- Search and completion functionality
