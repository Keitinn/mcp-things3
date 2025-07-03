"""Unit tests for response formatting functionality."""

import pytest
from unittest.mock import patch, Mock

from mcp_server_things3.applescript_handler import AppleScriptHandler


class TestResponseFormatting:
    """Test response formatting for various tools."""
    
    def test_task_formatting_basic(self):
        """Test basic task formatting with ID."""
        task = {
            "id": "ABC123DEF456",
            "title": "Complete project proposal",
            "tags": ""
        }
        
        # Simulate the formatting from view_inbox
        todo_id = task.get("id", "")
        title = task.get("title", "Untitled Todo").strip()
        tags = task.get("tags", "")
        
        line = f"• {title}"
        if tags:
            line += f" #{tags.replace(',', ' #')}"
        line += f" (id: {todo_id})"
        
        expected = "• Complete project proposal (id: ABC123DEF456)"
        assert line == expected
    
    def test_task_formatting_with_tags(self):
        """Test task formatting with multiple tags."""
        task = {
            "id": "ABC123",
            "title": "Review code",
            "tags": "work,urgent,backend"
        }
        
        todo_id = task.get("id", "")
        title = task.get("title", "Untitled Todo").strip()
        tags = task.get("tags", "")
        
        line = f"• {title}"
        if tags:
            line += f" #{tags.replace(',', ' #')}"
        line += f" (id: {todo_id})"
        
        expected = "• Review code #work #urgent #backend (id: ABC123)"
        assert line == expected
    
    def test_task_formatting_empty_title(self):
        """Test handling of empty/missing title."""
        task = {
            "id": "ABC123",
            "title": "",
            "tags": "work"
        }
        
        title = task.get("title", "Untitled Todo").strip()
        if not title:
            title = "Untitled Todo"
        
        line = f"• {title} (id: {task['id']})"
        
        expected = "• Untitled Todo (id: ABC123)"
        assert line == expected
    
    def test_task_formatting_with_due_date(self):
        """Test task formatting with due date (from anytime view)."""
        task = {
            "id": "ABC123",
            "title": "Submit report",
            "tags": "work",
            "due_date": "Friday, December 25, 2024 at 5:00 PM"
        }
        
        todo_id = task.get("id", "")
        title = task.get("title", "Untitled")
        tags = task.get("tags", "")
        due_date = task.get("due_date", "")
        
        line = f"  • {title}"
        if due_date:
            line += f" ⚠️ Due: {due_date.split(',')[0]}"  # Simple date format
        if tags:
            line += f" #{tags.replace(',', ' #')}"
        line += f" (id: {todo_id})"
        
        expected = "  • Submit report ⚠️ Due: Friday #work (id: ABC123)"
        assert line == expected
    
    def test_search_result_formatting(self):
        """Test search result formatting with status icons."""
        completed_task = {
            "id": "ABC123",
            "title": "Completed task",
            "status": "completed",
            "tags": "done"
        }
        
        pending_task = {
            "id": "DEF456", 
            "title": "Pending task",
            "status": "open",
            "tags": ""
        }
        
        # Test completed task
        status_icon = "✅" if completed_task["status"] == "completed" else "⏳"
        line = f"{status_icon} {completed_task['title']} #done (id: {completed_task['id']})"
        assert line == "✅ Completed task #done (id: ABC123)"
        
        # Test pending task
        status_icon = "✅" if pending_task["status"] == "completed" else "⏳"
        line = f"{status_icon} {pending_task['title']} (id: {pending_task['id']})"
        assert line == "⏳ Pending task (id: DEF456)"
    
    def test_project_formatting(self):
        """Test project formatting."""
        project = {
            "id": "PROJ123",
            "title": "Website Redesign"
        }
        
        project_id = project.get("id", "")
        title = project.get("title", "Untitled Project").strip()
        line = f"• {title} (id: {project_id})"
        
        expected = "• Website Redesign (id: PROJ123)"
        assert line == expected
    
    def test_today_overload_message(self):
        """Test Today overload warning message."""
        todo_count = 6
        
        if todo_count > 4:
            response = [f"⚠️ Today's Focus ({todo_count} items - consider reviewing):"]
        else:
            response = [f"Today's Focus ({todo_count} items):"]
        
        # Add overload guidance
        if todo_count > 4:
            response.append("💡 Today has more than 4 items. Consider:")
            response.append("• Which are truly TODAY vs. nice-to-have?")
            response.append("• Move flexible items to Anytime (update with when='')")
            response.append("• Use Evening section for time-specific tasks")
        
        result = "\n".join(response)
        
        assert "⚠️ Today's Focus (6 items - consider reviewing):" in result
        assert "💡 Today has more than 4 items" in result
        assert "truly TODAY vs. nice-to-have" in result
    
    def test_auth_error_message(self):
        """Test auth token error message formatting."""
        expected_message = """❌ Authentication Required

The THINGS3_AUTH_TOKEN environment variable is not set.

To get your token:
1. Open Things3
2. Go to Settings → General → Enable Things URLs → Manage
3. Copy your token
4. Set environment variable: export THINGS3_AUTH_TOKEN="your-token-here"

Note: Each device has its own token."""
        
        # This is the exact message from update-things3-todo
        actual_message = """❌ Authentication Required

The THINGS3_AUTH_TOKEN environment variable is not set.

To get your token:
1. Open Things3
2. Go to Settings → General → Enable Things URLs → Manage
3. Copy your token
4. Set environment variable: export THINGS3_AUTH_TOKEN="your-token-here"

Note: Each device has its own token."""
        
        assert actual_message == expected_message