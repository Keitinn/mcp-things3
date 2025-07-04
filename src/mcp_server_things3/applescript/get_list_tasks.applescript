use framework "Foundation"
use scripting additions

on run argv
    if (count of argv) < 1 then
        error "List name required as argument"
    end if
    
    set listName to item 1 of argv
    
    -- Validate list name
    if listName is not in {"Today", "Inbox", "Anytime", "Upcoming", "Someday", "Logbook", "Trash"} then
        error "Invalid list name. Valid lists: Today, Inbox, Anytime, Upcoming, Someday, Logbook, Trash"
    end if
    
    return my get_tasks_from_list(listName)
end run

on todo_to_dict(theTodo)
    set theDict to current application's NSMutableDictionary's dictionary()
    
    tell application "Things3"
        theDict's setValue:(id of theTodo) forKey:"id"
        theDict's setValue:(name of theTodo) forKey:"title"
        
        if notes of theTodo is not missing value then
            theDict's setValue:(notes of theTodo) forKey:"notes"
        else
            theDict's setValue:"" forKey:"notes"
        end if
        
        if due date of theTodo is not missing value then
            theDict's setValue:((due date of theTodo) as string) forKey:"due_date"
        else
            theDict's setValue:"" forKey:"due_date"
        end if
        
        -- Add status
        if status of theTodo is completed then
            theDict's setValue:"completed" forKey:"status"
        else if status of theTodo is canceled then
            theDict's setValue:"canceled" forKey:"status"
        else
            theDict's setValue:"open" forKey:"status"
        end if
        
        -- Add when date for scheduled tasks
        if activation date of theTodo is not missing value then
            theDict's setValue:((activation date of theTodo) as string) forKey:"when_date"
        else
            theDict's setValue:"" forKey:"when_date"
        end if
        
        set tagList to tag names of theTodo
        if tagList is not {} then
            set AppleScript's text item delimiters to ","
            set tagText to tagList as string
            set AppleScript's text item delimiters to ""
            theDict's setValue:tagText forKey:"tags"
        else
            theDict's setValue:"" forKey:"tags"
        end if
        
        -- Get project/area info
        set parentList to ""
        set parentType to ""
        if project of theTodo is not missing value then
            set parentList to name of project of theTodo
            set parentType to "project"
        else if area of theTodo is not missing value then
            set parentList to name of area of theTodo
            set parentType to "area"
        end if
        theDict's setValue:parentList forKey:"list"
        theDict's setValue:parentType forKey:"list_type"
    end tell
    
    return theDict
end todo_to_dict

on todos_to_json(theTodos)
    set todoArray to current application's NSMutableArray's array()
    
    repeat with aTodo in theTodos
        set todoDict to todo_to_dict(aTodo)
        todoArray's addObject:todoDict
    end repeat
    
    set {jsonData, theError} to current application's NSJSONSerialization's dataWithJSONObject:todoArray options:0 |error|:(reference)
    
    if jsonData is missing value then
        error (theError's localizedDescription() as text)
    end if
    
    set jsonString to current application's NSString's alloc()'s initWithData:jsonData encoding:(current application's NSUTF8StringEncoding)
    
    return jsonString as text
end todos_to_json

on get_tasks_from_list(listName)
    tell application "Things3"
        try
            set theTodos to to dos of list listName
            
            if (count of theTodos) is 0 then
                return "[]"
            else
                return my todos_to_json(theTodos)
            end if
        on error errMsg
            return "{\"error\": \"" & errMsg & "\"}"
        end try
    end tell
end get_tasks_from_list