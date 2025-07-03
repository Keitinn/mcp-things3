"""Unit tests for AppleScript handler functionality."""

import pytest
from unittest.mock import patch, Mock

from mcp_server_things3.applescript_handler import AppleScriptHandler


class TestAppleScriptHandler:
    """Test AppleScript handler utilities."""
    
    def test_normalize_task_basic(self):
        """Test basic task normalization."""
        task = {
            "id": "123",
            "title": "Test Task",
            "due_date": "missing value",
            "notes": "Some notes"
        }
        
        normalized = AppleScriptHandler.normalize_task(task)
        
        assert normalized["id"] == "123"
        assert normalized["title"] == "Test Task"
        assert normalized["due_date"] is None  # Converted from "missing value"
        assert normalized["notes"] == "Some notes"
    
    def test_normalize_task_empty(self):
        """Test normalization with empty task."""
        assert AppleScriptHandler.normalize_task({}) == {}
        assert AppleScriptHandler.normalize_task(None) is None
    
    def test_normalize_task_all_fields(self):
        """Test normalization of all nullable fields."""
        task = {
            "id": "123",
            "title": "Test",
            "due_date": "missing value",
            "when_date": "missing value", 
            "when": "missing value",
            "notes": "missing value",
            "tags": "missing value",
            "list": "missing value"
        }
        
        normalized = AppleScriptHandler.normalize_task(task)
        
        # All "missing value" fields should be None
        assert normalized["due_date"] is None
        assert normalized["when_date"] is None
        assert normalized["when"] is None
        assert normalized["notes"] is None
        assert normalized["tags"] is None
        assert normalized["list"] is None
        
        # Non-nullable fields unchanged
        assert normalized["id"] == "123"
        assert normalized["title"] == "Test"
    
    def test_normalize_task_real_values(self):
        """Test that real values are preserved."""
        task = {
            "id": "123",
            "title": "Test Task",
            "due_date": "December 25, 2024",
            "notes": "Real notes",
            "tags": "work,urgent",
            "list": "Work Project"
        }
        
        normalized = AppleScriptHandler.normalize_task(task)
        
        # All values should be preserved
        assert normalized["due_date"] == "December 25, 2024"
        assert normalized["notes"] == "Real notes"
        assert normalized["tags"] == "work,urgent"
        assert normalized["list"] == "Work Project"
    
    def test_safe_string_for_applescript(self):
        """Test AppleScript string escaping."""
        # Test quotes
        result = AppleScriptHandler.safe_string_for_applescript('Say "hello"')
        assert result == 'Say \\"hello\\"'
        
        # Test newlines
        result = AppleScriptHandler.safe_string_for_applescript("Line 1\nLine 2")
        assert result == "Line 1\\nLine 2"
        
        # Test backslashes
        result = AppleScriptHandler.safe_string_for_applescript("Path\\to\\file")
        assert result == "Path\\\\to\\\\file"
        
        # Test empty string
        result = AppleScriptHandler.safe_string_for_applescript("")
        assert result == ""
        
        # Test None
        result = AppleScriptHandler.safe_string_for_applescript(None)
        assert result == ""


class TestAppleScriptExecution:
    """Test AppleScript execution with mocking."""
    
    @patch('mcp_server_things3.applescript_handler.subprocess.run')
    def test_run_script_success(self, mock_run):
        """Test successful script execution."""
        mock_result = Mock()
        mock_result.stdout = "script output"
        mock_run.return_value = mock_result
        
        result = AppleScriptHandler.run_script('tell app "Finder" to return name')
        
        assert result == "script output"
        mock_run.assert_called_once()
    
    @patch('mcp_server_things3.applescript_handler.subprocess.run')
    def test_run_script_failure(self, mock_run):
        """Test script execution failure with better error message."""
        from subprocess import CalledProcessError
        
        error = CalledProcessError(1, ['osascript'], stderr="AppleScript error")
        mock_run.side_effect = error
        
        with pytest.raises(RuntimeError) as exc_info:
            AppleScriptHandler.run_script('bad script')
        
        error_msg = str(exc_info.value)
        assert "AppleScript execution failed" in error_msg
        assert "AppleScript error" in error_msg
        assert "bad script" in error_msg
    
    @patch('mcp_server_things3.applescript_handler.subprocess.run')
    def test_run_script_file_not_found(self, mock_run):
        """Test script file not found error."""
        with pytest.raises(FileNotFoundError) as exc_info:
            AppleScriptHandler.run_script_file("nonexistent.applescript")
        
        assert "AppleScript file not found" in str(exc_info.value)