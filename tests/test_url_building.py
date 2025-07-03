"""Unit tests for Things3 URL building functionality."""

import pytest
from urllib.parse import unquote

from mcp_server_things3.fast_server import build_things_url


class TestURLBuilding:
    """Test URL building with various edge cases."""
    
    def test_basic_url_building(self):
        """Test basic URL construction."""
        url = build_things_url("things:///add", {"title": "Test Task"})
        assert url == "things:///add?title=Test%20Task"
    
    def test_empty_params(self):
        """Test URL building with no parameters."""
        url = build_things_url("things:///add", {})
        assert url == "things:///add"
    
    def test_none_params(self):
        """Test URL building with None parameters."""
        url = build_things_url("things:///add", None)
        assert url == "things:///add"
    
    def test_special_characters(self):
        """Test URL encoding of special characters."""
        params = {
            "title": "Task with #hashtags & ampersands",
            "notes": "Line 1\nLine 2\rCarriage return"
        }
        url = build_things_url("things:///add", params)
        
        # Decode to verify proper encoding
        decoded = unquote(url)
        assert "#hashtags" in decoded
        assert "&" in decoded
        assert "\n" in decoded
    
    def test_list_values(self):
        """Test handling of list values (like tags)."""
        params = {
            "title": "Test",
            "tags": ["work", "urgent", "project-x"]
        }
        url = build_things_url("things:///add", params)
        
        # Should join with commas
        assert "tags=work%2Curgent%2Cproject-x" in url
    
    def test_none_values_filtered(self):
        """Test that None values are filtered out."""
        params = {
            "title": "Test",
            "notes": None,
            "when": "today"
        }
        url = build_things_url("things:///add", params)
        
        assert "notes=" not in url
        assert "title=Test" in url
        assert "when=today" in url
    
    def test_empty_string_values(self):
        """Test that empty strings are preserved (for clearing fields)."""
        params = {
            "title": "Test",
            "when": "",  # Empty string to clear date
            "notes": "Some notes"
        }
        url = build_things_url("things:///add", params)
        
        assert "when=" in url  # Empty value should be included
        assert "title=Test" in url
    
    def test_auth_token_handling(self):
        """Test that auth tokens are properly encoded."""
        params = {
            "title": "Test",
            "auth-token": "abc123-def456"
        }
        url = build_things_url("things:///update", params)
        
        assert "auth-token=abc123-def456" in url
    
    def test_unicode_characters(self):
        """Test handling of unicode characters."""
        params = {
            "title": "Café ☕️ and 日本語",
            "notes": "Emoji test: 🎯 💡 ⚠️"
        }
        url = build_things_url("things:///add", params)
        
        # Should be properly encoded
        assert "things:///add?" in url
        assert len(url) > 50  # Should be longer due to encoding
    
    def test_checklist_items(self):
        """Test handling of checklist items (newline-separated)."""
        params = {
            "title": "Project Setup",
            "checklist-items": "Step 1\nStep 2\nStep 3"
        }
        url = build_things_url("things:///add", params)
        
        # Newlines should be encoded
        assert "%0A" in url or "\\n" in unquote(url)