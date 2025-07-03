import subprocess
from typing import List, Dict, Any, Optional
import json
import re
import os
from pathlib import Path

class AppleScriptHandler:
    """Handles AppleScript execution for Things3 data retrieval."""
    
    @staticmethod
    def get_script_path(script_name: str) -> Path:
        """Get the path to an AppleScript file in the applescript directory."""
        # Get the directory where this Python file is located
        current_dir = Path(__file__).parent
        return current_dir / "applescript" / script_name
    
    @staticmethod
    def run_script_file(script_name: str) -> str:
        """
        Executes an AppleScript file and returns its output.
        """
        script_path = AppleScriptHandler.get_script_path(script_name)
        
        if not script_path.exists():
            raise FileNotFoundError(f"AppleScript file not found: {script_path}")
        
        try:
            result = subprocess.run(
                ['osascript', str(script_path)],
                check=True,
                capture_output=True,
                text=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            error_msg = f"AppleScript failed: {script_name}\n"
            if e.stderr:
                error_msg += f"Error: {e.stderr}\n"
            if e.returncode:
                error_msg += f"Exit code: {e.returncode}"
            raise RuntimeError(error_msg)

    @staticmethod
    def run_script(script: str) -> str:
        """
        Executes an AppleScript and returns its output.
        """
        try:
            result = subprocess.run(
                ['osascript', '-e', script],
                check=True,
                capture_output=True,
                text=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            error_msg = "AppleScript execution failed\n"
            if e.stderr:
                error_msg += f"Error: {e.stderr}\n"
            error_msg += f"Script: {script[:100]}..."  # Show first 100 chars
            raise RuntimeError(error_msg)

    @staticmethod
    def safe_string_for_applescript(text: str) -> str:
        """
        Safely escape a string for use in AppleScript by handling quotes and special characters.
        """
        if not text:
            return ""
        
        # Replace backslashes first to avoid double escaping
        text = text.replace("\\", "\\\\")
        # Replace quotes with escaped quotes
        text = text.replace('"', '\\"')
        # Replace newlines with \\n
        text = text.replace("\n", "\\n")
        text = text.replace("\r", "\\r")
        
        return text
    
    @staticmethod
    def normalize_task(task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize task data from AppleScript by converting 'missing value' to None.
        """
        if not task:
            return task
            
        # Fields that can have "missing value"
        nullable_fields = ['due_date', 'when_date', 'when', 'notes', 'tags', 'list']
        
        for field in nullable_fields:
            if field in task and task[field] == "missing value":
                task[field] = None
                
        return task


    @staticmethod
    def get_inbox_tasks() -> List[Dict[str, Any]]:
        """
        Retrieves tasks from the Inbox using AppleScript with JSON serialization.
        """
        try:
            # Use the new JSON-based AppleScript
            result = AppleScriptHandler.run_script_file("get_inbox_tasks.applescript")
            
            # Parse JSON directly
            if not result:
                return []
            
            tasks = json.loads(result)
            
            # Normalize and ensure consistent field names
            normalized_tasks = []
            for task in tasks:
                if "when" in task and "when_date" not in task:
                    task["when_date"] = task["when"]
                normalized_tasks.append(AppleScriptHandler.normalize_task(task))
            
            return normalized_tasks
            
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON from inbox tasks: {e}")
            return []
        except Exception as e:
            print(f"Error retrieving inbox tasks: {e}")
            return []

    @staticmethod
    def get_todays_tasks() -> List[Dict[str, Any]]:
        """
        Retrieves today's tasks from Things3 using AppleScript with JSON serialization.
        """
        try:
            # Use the new JSON-based AppleScript
            result = AppleScriptHandler.run_script_file("get_todays_tasks.applescript")
            
            # Parse JSON directly
            if not result:
                return []
            
            tasks = json.loads(result)
            
            # Normalize and ensure consistent field names
            normalized_tasks = []
            for task in tasks:
                if "when" in task and "when_date" not in task:
                    task["when_date"] = task["when"]
                normalized_tasks.append(AppleScriptHandler.normalize_task(task))
            
            return normalized_tasks
            
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON from today's tasks: {e}")
            return []
        except Exception as e:
            print(f"Error retrieving today's tasks: {e}")
            return []

    @staticmethod
    def get_projects() -> List[Dict[str, str]]:
        """
        Retrieves all projects from Things3 using AppleScript with JSON serialization.
        """
        try:
            # Use the new JSON-based AppleScript
            result = AppleScriptHandler.run_script_file("get_projects.applescript")
            
            # Parse JSON directly
            if not result:
                return []
            
            return json.loads(result)
            
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON from projects: {e}")
            return []
        except Exception as e:
            print(f"Error retrieving projects: {e}")
            return []

    @staticmethod
    def validate_things3_access() -> bool:
        """
        Validate that Things3 is accessible and responsive.
        """
        try:
            script = '''
            tell application "Things3"
                return name of application "Things3"
            end tell
            '''
            result = AppleScriptHandler.run_script(script)
            return "Things3" in result
        except Exception:
            return False


    @staticmethod
    def complete_todo_by_id(todo_id: str) -> bool:
        """
        Mark a todo as completed by its ID.
        """
        script = f'''
        tell application "Things3"
            try
                set foundTodo to to do id "{AppleScriptHandler.safe_string_for_applescript(todo_id)}"
                set status of foundTodo to completed
                return "COMPLETED:" & name of foundTodo
            on error
                return "NOT_FOUND"
            end try
        end tell
        '''
        
        try:
            result = AppleScriptHandler.run_script(script)
            return result.startswith("COMPLETED:")
        except Exception:
            return False

    @staticmethod
    def search_todos(query: str) -> List[Dict[str, Any]]:
        """
        Search for todos by title or content using JSON serialization.
        """
        try:
            # Use the new JSON-based AppleScript with query as argument
            result = subprocess.run(
                ['osascript', str(AppleScriptHandler.get_script_path("search_todos.applescript")), query],
                check=True,
                capture_output=True,
                text=True
            )
            
            # Parse JSON directly
            if not result.stdout.strip():
                return []
            
            todos = json.loads(result.stdout.strip())
            
            # Normalize and ensure consistent field names
            normalized_todos = []
            for todo in todos:
                if "when" in todo and "when_date" not in todo:
                    todo["when_date"] = todo["when"]
                normalized_todos.append(AppleScriptHandler.normalize_task(todo))
            
            return normalized_todos
            
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON from search: {e}")
            return []
        except Exception as e:
            print(f"Error searching todos: {e}")
            return []

    @staticmethod
    def get_upcoming_tasks() -> List[Dict[str, Any]]:
        """
        Returns tasks from Upcoming list using JSON serialization.
        """
        try:
            # Use the new JSON-based AppleScript
            result = AppleScriptHandler.run_script_file("get_upcoming_tasks.applescript")
            
            # Parse JSON directly
            if not result:
                return []
            
            tasks = json.loads(result)
            
            # Normalize and ensure consistent field names
            normalized_tasks = []
            for task in tasks:
                if "when" in task and "when_date" not in task:
                    task["when_date"] = task["when"]
                normalized_tasks.append(AppleScriptHandler.normalize_task(task))
            
            return normalized_tasks
            
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON from upcoming tasks: {e}")
            return []
        except Exception as e:
            print(f"Error retrieving upcoming tasks: {e}")
            return []

    @staticmethod
    def get_anytime_tasks() -> List[Dict[str, Any]]:
        """
        Returns unscheduled active tasks using JSON serialization.
        """
        try:
            # Use the new JSON-based AppleScript
            result = AppleScriptHandler.run_script_file("get_anytime_tasks.applescript")
            
            # Parse JSON directly
            if not result:
                return []
            
            tasks = json.loads(result)
            
            # Normalize all tasks
            return [AppleScriptHandler.normalize_task(task) for task in tasks]
            
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON from anytime tasks: {e}")
            return []
        except Exception as e:
            print(f"Error retrieving anytime tasks: {e}")
            return []

    @staticmethod
    def get_today_count() -> int:
        """
        Returns count of tasks in Today list for overload warnings.
        """
        script = '''
        tell application "Things3"
            return count of to dos of list "Today"
        end tell
        '''
        
        try:
            result = AppleScriptHandler.run_script(script)
            return int(result)
        except Exception:
            return 0
