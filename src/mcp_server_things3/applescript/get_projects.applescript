use framework "Foundation"
use scripting additions

on project_to_dict(theProject)
    set theDict to current application's NSMutableDictionary's dictionary()
    
    tell application "Things3"
        theDict's setValue:(id of theProject) forKey:"id"
        theDict's setValue:(name of theProject) forKey:"title"
        
        if notes of theProject is not missing value then
            theDict's setValue:(notes of theProject) forKey:"notes"
        else
            theDict's setValue:"" forKey:"notes"
        end if
        
        -- Get area if exists
        if area of theProject is not missing value then
            theDict's setValue:(name of area of theProject) forKey:"area"
        else
            theDict's setValue:"" forKey:"area"
        end if
    end tell
    
    return theDict
end project_to_dict

on projects_to_json(theProjects)
    set projectArray to current application's NSMutableArray's array()
    
    repeat with aProject in theProjects
        set projectDict to project_to_dict(aProject)
        projectArray's addObject:projectDict
    end repeat
    
    set {jsonData, theError} to current application's NSJSONSerialization's dataWithJSONObject:projectArray options:0 |error|:(reference)
    
    if jsonData is missing value then
        error (theError's localizedDescription() as text)
    end if
    
    set jsonString to current application's NSString's alloc()'s initWithData:jsonData encoding:(current application's NSUTF8StringEncoding)
    
    return jsonString as text
end projects_to_json

tell application "Things3"
    set allProjects to projects
    
    if (count of allProjects) is 0 then
        return "[]"
    else
        return my projects_to_json(allProjects)
    end if
end tell