<file_map>
/Users/darin/docs/culturedcode.com/things/support
└── articles
    ├── 1059358.md
    ├── 1100684.md
    ├── 1298518.md
    ├── 1384628.md
    ├── 1477596.md
    ├── 1481195.md
    ├── 1665164.md
    ├── 1893713.md
    ├── 2094967.md
    ├── 2147161.md
    ├── 2157909.md
    ├── 2249437.md
    ├── 2409117.md
    ├── 2409121.md
    ├── 2409123.md
    ├── 2538669.md
    ├── 2693493.md
    ├── 2785159.md
    ├── 2803551.md
    ├── 2803552.md
    ├── 2803555.md
    ├── 2803556.md
    ├── 2803561.md
    ├── 2803564.md
    ├── 2803566.md
    ├── 2803567.md
    ├── 2803569.md
    ├── 2803570.md
    ├── 2803573.md
    ├── 2803574.md
    ├── 2803577.md
    ├── 2803579.md
    ├── 2803580.md
    ├── 2803581.md
    ├── 2803582.md
    ├── 2803583.md
    ├── 2803584.md
    ├── 2803585.md
    ├── 2803586.md
    ├── 2803588.md
    ├── 2803589.md
    ├── 2803590.md
    ├── 2803591.md
    ├── 2803592.md
    ├── 2803593.md
    ├── 2877019.md
    ├── 2955145.md
    ├── 2978194.md
    ├── 3289315.md
    ├── 3614435.md
    ├── 4001304.md
    ├── 4438545.md
    ├── 4522602.md
    ├── 4651820.md
    ├── 6378414.md
    └── 9780167.md

</file_map>

<file_contents>
File: /Users/darin/docs/culturedcode.com/things/support/articles/2803573.md
```md
---
title: Things URL Scheme - Things Support
url: https://culturedcode.com/things/support/articles/2803573
scraped_at: 2025-07-02 14:48:44
---

# Things URL Scheme - Things Support

The URL scheme lets pro users and developers of other apps send commands to Things. This page explains how it works.
Here are some examples of commands that Things understands:
  * Create a new to-do named “Buy milk”.
  * Show all to-dos tagged with “Errand”.
  * Search all to-dos for “shipping address”.


There’s also a powerful JSON-based command that lets you create entire projects, together with all their notes, headings, and to-dos.
You can find the full documentation for each supported command further below. If you want to jump right in, here’s a little link builder tool to get you started. Simply fill out some of the fields and the corresponding link will be created for you on the fly. Enjoy!
Commands are sent to Things by constructing special URL links of the form:
```
things:///commandName?
  parameter1=value1&
  parameter2=value2&
  ...

```

Opening these links will launch the app and execute the command. Here’s how you would tell Things to create a to-do:
```
things:///add?
  title=Buy%20milk&
  notes=High%20fat

```

All commands support the convention by calling the provided , or callbacks as appropriate. Many commands return parameters to the callback.
Some commands require you to provide IDs of to-dos or lists. Here’s how you can retrieve them in Things.
To get the ID of a to-do:
  * On the Mac, control-click on the to-do and choose → .
  * On iOS, tap the to-do to open it and in the toolbar at the bottom, tap → → .


To get the ID of a list:
  * On the Mac, control-click on the list in the sidebar and choose → .
  * On iOS, navigate into the list and at the top right of the screen, tap → → .


For security reasons, commands that modify existing Things data require an authorization token to run. This prevents malicious links from modifying your data. This token should be passed as the parameter along with the other parameters in the command. You can find your unique token in Things’ settings:
  * On the Mac, go to → → → → .
  * On iOS, go to → → .


The commands use the following data types for their parameters:     Percent encoded. Maximum un-encoded string length: 4,000 characters unless otherwise specified.     String. Either , or a date string of the form . E.g. . Things will also attempt to interpret natural language dates such as or . These must be provided in English, regardless of the user’s device language.     A string describing a time in the local time zone. E.g. 9:30PM or 21:30.     A followed by the symbol and then followed by a . E.g. 2018-02-25@14:00.     A date-time string conforming to . E.g. or .     A string in JSON format. See for more details.
The first time you execute a command via the URL scheme, Things will ask you if you want to enable this feature. Simply answer with .
You can later change this in Things’ settings:
  * On the Mac, go to → → .
  * On iOS, go to → → .


The current version of the URL scheme is 2.
Add a to-do. For example, create a to-do in the inbox:
Create a to-do with a tag and notes set to start this evening:
```
things:///add?
  title=Buy%20milk&
  notes=Low%20fat.&
  when=evening&
  tags=Errand

```

Create several to-dos and add them to the Shopping project:
```
things:///add?
  titles=Milk%0aBeer%0aCheese&
  list=Shopping

```

Create and schedule a to-do for next Monday in the Health area (with ID of ):
```
things:///add?
  title=Call%20doctor&
  when=next%20monday&
  list-id=3052219D-8039-43D0-8654-AE1E20BE4F56

```

Create a to-do in the “This Evening” list with a reminder at 6PM:
```
things:///add?
  title=Collect%20dry%20cleaning&
  when=evening@6pm

```

Note that a limit of 250 items can be added within a 10 second period.
All parameters are optional. If neither the nor are specified, the to-do will be added to the inbox.     String. The title of the to-do to add. Ignored if is also specified.     String separated by new lines (encoded to ). Use instead of to create multiple to-dos. Takes priority over and . The other parameters are applied to all the created to-dos.     String. The text to use for the notes field of the to-do. Maximum unencoded length: 10,000 characters.     String. Possible values: , , , , , a , or a . Using a date time string adds a reminder for that time. The time component is ignored if or is specified.     . The deadline to apply to the to-do.     Comma separated strings corresponding to the titles of tags. Does not apply a tag if the specified tag doesn’t exist.     String separated by new lines (encoded to ). Checklist items to add to the to-do (maximum of 100).     String. Possible values can be (newlines overflow into notes, replacing them), , or (newlines create multiple checklist rows). Takes priority over , , or .     String. The ID of a project or area to add to. Takes precedence over .     String. The title of a project or area to add to. Ignored if is present.     String. Takes precedence over . The ID of a heading within a project to add to. Ignored if a project is not specified, or if the heading doesn’t exist.     String. The title of a heading within a project to add to. Ignored if is present, if a project is not specified, or if the heading doesn’t exist.     Boolean. Whether or not the to-do should be set to complete. Default: . Ignored if is also set to .     Boolean. Whether or not the to-do should be set to canceled. Default: . Takes priority over .     Boolean. Whether or not to show the quick entry dialog (populated with the provided data) instead of adding a new to-do. Ignored if is specified. Default: .     Boolean. Whether or not to navigate to and show the newly created to-do. If multiple to-dos have been created, the first one will be shown. Ignored if is also set to . Default: .     . The date to set as the creation date for the to-do in the database. Ignored if the date is in the future.     . The date to set as the completion date for the to-do in the database. Ignored if the to-do is not completed or canceled, or if the date is in the future.     Comma separated string. The IDs of the to-dos created.
Add a project. For example, create a project to build a treehouse set to start today:
```
things:///add-project?
  title=Build%20treehouse&
  when=today

```

Create a project inside the Family area:
```
things:///add-project?
  title=Plan%20Birthday%20Party&
  area=Family

```

Create a project inside the Finance area (with ID of ) with a deadline of December 31:
```
things:///add-project?
  title=Submit%20Tax&
  deadline=December%2031&
  area-id=F00A4075-0CA6-4A7F-88C6-CC8B4F1712FC

```
    String. The title of the project.     String. The text to use for the notes field of the project. Maximum unencoded length: 10,000 characters.     String. Possible values: , , , , , a , or a . Using a date time string adds a reminder for that time. The time component is ignored if or is specified.     . The deadline to apply to the project.     Comma separated strings corresponding to the titles of tags. Does not apply a tag if the specified tag doesn’t exist.     String. The ID of an area to add to. Takes precedence over .     String. The title of an area to add to. Ignored if is present.     String separated by new lines (encoded to ). Titles of to-dos to create inside the project.     Boolean. Whether or not the project should be set to complete. Default: . Ignored if is also set to . Will set all child to-dos to be completed.     Boolean. Whether or not the project should be set to canceled. Default: . Takes priority over . Will set all child to-dos to be canceled.     Boolean. Whether or not to navigate into the newly created project. Default: .     . The date to set as the creation date for the project in the database. If the parameter is also specified, this date is applied to them, too. Ignored if the date is in the future.     . The date to set as the completion date for the project in the database. If the parameter is also specified, this date is applied to them, too. Ignored if the to-do is not completed or canceled, or if the date is in the future.     string. The ID of the project created.
Update an existing to-do. For example, set a to-do to start today:
```
things:///update?
  id=4BE64FEA-8FEF-4F4F-B8B2-4E74605D5FA5&
  when=today

```

Change the title of a to-do:
```
things:///update?
  id=4BE64FEA-8FEF-4F4F-B8B2-4E74605D5FA5&
  title=Buy%20bread

```

Append notes to a to-do:
```
things:///update?
  id=4BE64FEA-8FEF-4F4F-B8B2-4E74605D5FA5&
  append-notes=Wholemeal%20bread

```

Add some checklist items to a to-do:
```
things:///update?
  id=4BE64FEA-8FEF-4F4F-B8B2-4E74605D5FA5&
  append-checklist-items=Cheese%0aBread%0aEggplant

```

Remove the deadline from a to-do:
```
things:///update?
  id=4BE64FEA-8FEF-4F4F-B8B2-4E74605D5FA5&
  deadline=

```

and must be specified. All other parameters are optional. Including a parameter with an equals sign () but without a value will clear that value (see deadline example).     String. The Things URL scheme .     String. The ID of the to-do to update. Required.     String. The title of the to-do. This will replace the existing title.     String. The notes of the to-do. This will replace the existing notes. Maximum unencoded length: 10,000 characters.     String. Text to add before the existing notes of a to-do. Maximum unencoded length: 10,000 characters.     String. Text to add after the existing notes of a to-do. Maximum unencoded length: 10,000 characters.     String. Set the when field of a to-do. Possible values: , , , , a , or a . Including a time adds a reminder for that time. The time component is ignored if is specified. This field cannot be updated on repeating to-dos.     . The deadline to apply to the to-do. This field cannot be updated on repeating to-dos.     Comma separated strings corresponding to the titles of tags. Replaces all current tags. Does not apply a tag if the specified tag doesn’t exist.     Comma separated strings corresponding to the titles of tags. Adds the specified tags to a to-do. Does not apply a tag if the specified tag doesn’t exist.      (encoded to ) separated strings. Set the checklist items of the to-do (maximum of 100). Will replace all existing checklist items.      (encoded to ) separated strings. Add checklist items to the front of the list of checklist items in the to-do (maximum of 100).      (encoded to ) separated strings. Add checklist items to the end of the list of checklist items in the to-do (maximum of 100).     String. The ID of a project or area to move the to-do into. Takes precedence over .     String. The title of a project or area to move the to-do into. Ignored if is present.     String. Takes precedence over . The ID of a heading within a project to move the to-do to. Ignored if the to-do is not in a project with the specified heading. Can be used together with or .     String. The title of a heading within a project to move the to-do to. Ignored if is present, or if the to-do is not in a project with the specified heading. Can be used together with or .     Boolean. Complete a to-do or set a to-do to incomplete. Ignored if is also set to . Setting on a canceled to-do will also mark it as incomplete. This field cannot be updated on repeating to-dos.     Boolean. Cancel a to-do or set a to-do to incomplete. Takes priority over . Setting on a completed to-do will also mark it as incomplete. This field cannot be updated on repeating to-dos.     Boolean. Whether or not to navigate to and show the updated to-do. Default: .     Boolean. Set to to duplicate the to-do before updating it, leaving the original to-do untouched. Repeating to-dos cannot be duplicated. Default: .     . Set the creation date for the to-do in the database. Ignored if the date is in the future.     . Set the completion date for the to-do in the database. Ignored if the to-do is not completed or canceled, or if the date is in the future. This field cannot be updated on repeating to-dos.     String. The ID of the to-do updated.
Update an existing project. For example, set a project to start tomorrow:
```
things:///update-project?
  id=852763FD-5954-4DF9-A88A-2ADD808BD279&
  when=tomorrow

```

Add a tag to a project:
```
things:///update-project?
  id=852763FD-5954-4DF9-A88A-2ADD808BD279&
  add-tags=Important

```

Prepend notes to a project:
```
things:///update-project?
  id=852763FD-5954-4DF9-A88A-2ADD808BD279&
  prepend-notes=SFO%20to%20JFK.

```

Clear the deadline of a project:
```
things:///update-project?
  id=852763FD-5954-4DF9-A88A-2ADD808BD279&
  deadline=

```

and must be specified. All other parameters are optional. Including a parameter with an equals sign () but without a value will clear that value (see deadline example).     String. The Things URL scheme .     String. The ID of the project to update. Required.     String. The title of the project. This will replace the existing title.     String. The notes of the project. This will replace the existing notes. Maximum unencoded length: 10,000 characters.     String. Text to add before the existing notes of a project. Maximum unencoded length: 10,000 characters.     String. Text to add after the existing notes of a project. Maximum unencoded length: 10,000 characters.     String. Set the when field of a project. Possible values: , , , , a , or a . Including a time adds a reminder for that time. The time component is ignored if is specified. This field cannot be updated on repeating projects.     . The deadline to apply to the project. This field cannot be updated on repeating projects.     Comma separated strings corresponding to the titles of tags. Replaces all current tags. Does not apply a tag if the specified tag doesn’t exist.     Comma separated strings corresponding to the titles of tags. Adds the specified tags to a project. Does not apply a tag if the specified tag doesn’t exist.     String. The ID of an area to move the project into. Takes precedence over .     String. The title of an area to move the project into. Ignored if is present.     Boolean. Complete a project or set a project to incomplete. Ignored if is also set to . Setting to will be ignored unless all child to-dos are completed or canceled and all child headings archived. Setting to on a canceled project will mark it as incomplete. This field cannot be updated on repeating projects.     Boolean. Cancel a project or set a project to incomplete. Takes priority over . Setting to will be ignored unless all child to-dos are completed or canceled and all child headings archived. Setting to on a completed project will mark it as incomplete. This field cannot be updated on repeating projects.     Boolean. Whether or not to navigate to and show the updated project. Default: .     Boolean. Set to to duplicate the project before updating it, leaving the original project untouched. Repeating projects cannot be duplicated. Default: .     . Set the creation date for the project in the database. Ignored if the date is in the future.     . Set the completion date for the project in the database. Ignored if the project is not completed or canceled, or if the date is in the future. This field cannot be updated on repeating projects.     String. The ID of the project updated.
Navigate to and show an area, project, tag or to-do, or one of the built-in lists, optionally filtering by one or more tags.
Navigate to the Today list:
Navigate into project with ID :
Show project with title “Vacation”:
Show project with title “Vacation”, filtering by the “Errand” tag:
```
things:///show?
  query=vacation&
  filter=errand

```
    String. The ID of an area, project, tag or to-do to show; or one of the following built-in list IDs: , , , , , , , , , , . Takes precedence over .     String. The name of an area, project, tag or a built-in list to show. This is equivalent to entering the query text in to the quick find within Things and selecting the first result. Ignored if is also set. Note: task cannot be shown using the parameter; use the parameter or the command instead.     String. Comma separated strings corresponding to the titles of tags that the list should be filtered by.
Invoke and show the search screen. For example, search for the text “vacation”:
Show the search screen without searching for anything:
The version of the Things app and URL scheme.     String. The version of the Things URL scheme.     String. The build number of the app.
Things also has an advanced, JSON-based add command that allows more control over the projects and to-dos imported into Things. This command is intended to be used by app developers or other people familiar with scripting or programming.
We’ve created a set of Swift helper classes that you can use to more easily generate the JSON needed for this command. Get the code from the [Things JSON Coder GitHub repository](https://github.com/culturedcode/ThingsJSONCoder).
```
things:///json?data=
 [
  {
   "type": "project",
   "attributes": {
    "title": "Go Shopping",
    "items": [
     {
      "type": "to-do",
      "attributes": {
       "title": "Bread"
      }
     },
     {
      "type": "to-do",
      "attributes": {
       "title": "Milk"
      }
     }
    ]
   }
  }
 ]

```
    String. The Things URL scheme . This is required whenever the provided JSON data contains an operation.     JSON string. The JSON should be an array containing and objects (see below).     Boolean. Whether or not to navigate to and show the newly created to-do or project. If multiple items have been created, the first one will be shown. Default: .     JSON string. An array of IDs of the to-dos and projects created that were specified in the top level JSON array. The IDs of the to-dos created inside projects are not returned.
## Describing Things objects in JSON
Each operation consists of the following fields:
  * The type of the object. These are described in more detail below. This field is required.
  * The operation to perform on the object. Either (create a new object) or (update the fields of an existing object). If this field is not present, the operation is assumed to be . Currently only and objects can be updated.
  * Required for update operations, this is the ID of the object to update.
  * A dictionary of attributes, which correspond to the properties of the object itself. The field must be included but all attributes themselves are optional.

```
{
  "type": "to-do",
  "operation": "update",
  "id": "1BD13549-0BE7-49AC-B645-74B7BA8DE7C4",
  "attributes": {
    "deadline": "today"
  }
}

```
```
{
 "type": "to-do",
 "attributes": {
  "title": "Milk"
 }
}

```

  * : 
    * - string. The title of the to-do.
    * - string. The text to use for the notes field of the to-do. Maximum length: 10,000 characters.
    * - string. Possible values: , , , , , a , or a . Using a date time string adds a reminder for that time. The time component is ignored if or is specified.
    * - . The deadline to apply to the to-do.
    * - array of strings corresponding to the titles of tags. Does not apply a tag if a tag with the specified title doesn’t exist.
    * - array of objects (maximum of 100).
    * - string. The ID of a project or area to add to. Takes precedence over . Ignored if the to-do is specified inside the array of a object.
    * - string. The title of a project or area to add to. Ignored if is presen[<35;64;18Mt, or if the to-do is specified inside the array of a object.
    * - string. Takes precedence over . The ID of a heading within a project to add to. Ignored if a project is not specified, if the heading doesn’t exist, or if the to-do is specified inside the items array of a project object.
    * - string. The title of a heading within a project to add to. Ignored if is present, if a project is not specified, if the heading doesn’t exist, or if the to-do is specified inside the items array of a project object.
    * - boolean. Whether or not the to-do should be set to complete. Default: . Ignored if is also set to .
    * - boolean. Whether or not the to-do should be set to canceled. Default: . Takes priority over .
    * - . The date to set as the creation date for the to-do in the database. Ignored if the date is in the future.
    * - . The date to set as the completion date for the to-do in the database. Ignored if the to-do is not completed or canceled, or if the date is in the future.
  * specific . These attributes can only be used with operations: 
    * - string. Text to add before the existing notes of a to-do. Maximum unencoded length: 10,000 characters.
    * - string. Text to add after the existing notes of a to-do. Maximum unencoded length: 10,000 characters.
    * - comma separated strings corresponding to the titles of tags. Adds the specified tags to a to-do. Does not apply a tag if the specified tag doesn’t exist.
    * - (encoded to ) separated strings. Add checklist items to the front of the list of checklist items in the to-do (maximum of 100).
    * - (encoded to ) separated strings. Add checklist items to the end of the list of checklist items in the to-do (maximum of 100).

```
{
 "type": "project",
 "attributes": {
  "title": "Go Shopping",
  "items": [
   {
    "type": "to-do",
    "attributes": {
     "title": "Bread"
    }
   }
  ]
 }
}

```

  * : 
    * - string. The title of the project.
    * - string. The text to use for the notes field (maximum length: 10,000 characters).
    * - string. Possible values: , , , , , a , or a . Using a date time string adds a reminder for that time. The time component is ignored if or is specified.
    * - . The deadline to apply.
    * - array of strings corresponding to the titles of tags. Does not apply a tag if a tag with the specified title doesn’t exist.
    * - string. The ID of an area to add to. Takes precedence over .
    * - string. The title of an area to add to. Ignored if is present.
    * - boolean. Whether or not the project should be set to complete. Default: . Ignored unless all child to-dos are completed or canceled.
    * - boolean. Whether or not the project should be set to canceled. Default: . Takes priority over . Ignored unless all child to-dos are completed or canceled.
    * - . The date to set as the creation date for the project in the database. Ignored if the date is in the future.
    * - . The date to set as the completion date for the project in the database. Ignored if the project is not completed or canceled, or if the date is in the future.
  * specific . These attributes can only be used with operations: 
    * - array of or objects. To add to-dos to an existing project, create individual objects instead.
  * specific . These attributes can only be used with operations: 
    * String. Text to add before the existing notes of a project. Maximum unencoded length: 10,000 characters.
    * String. Text to add after the existing notes of a project. Maximum unencoded length: 10,000 characters.
    * Comma separated strings corresponding to the titles of tags. Adds the specified tags to a project. Does not apply a tag if the specified tag doesn’t exist.

```
{
 "type": "heading",
 "attributes": {
  "title": "Sights"
 }
}

```

  * : 
    * - string. The title of the heading.
    * - boolean. Whether or not the heading is archived. Default: . Ignored unless all to-dos under the heading are completed or canceled.

```
{
 "type": "checklist-item",
 "attributes": {
  "title": "Hotels",
  "completed": true
 }
}

```

  * : 
    * - string. The title of the checklist item.
    * - boolean. Whether or not the checklist item should be set to complete. Default: . Ignored if is also set to .
    * - boolean. Whether or not the checklist item should be set to canceled. Default: . Takes priority over .


This example is not URL encoded for clarity.
```
things:///json?data=
 [
  {
   "type": "project",
   "attributes": {
    "title": "Go Shopping",
    "items": [
     {
      "type": "to-do",
      "attributes": {
       "title": "Bread"
      }
     },
     {
      "type": "to-do",
      "attributes": {
       "title": "Milk"
      }
     }
    ]
   }
  },
  {
   "type": "project",
   "attributes": {
    "title": "Vacation in Rome",
    "notes": "Some time in August.",
    "area": "Family",
    "items": [
     {
      "type": "to-do",
      "attributes": {
       "title": "Ask Sarah for travel guide"
      }
     },
     {
      "type": "to-do",
      "attributes": {
       "title": "Add dates to calendar"
      }
     },
     {
      "type": "heading",
      "attributes": {
       "title": "Sights"
      }
     },
     {
      "type": "to-do",
      "attributes": {
       "title": "Vatican City"
      }
     },
     {
      "type": "to-do",
      "attributes": {
       "title": "The Colosseum",
       "notes": "12€"
      }
     },
     {
      "type": "heading",
      "attributes": {
       "title": "Planning"
      }
     },
     {
      "type": "to-do",
      "attributes": {
       "title": "Call Paolo",
       "completed": true
      }
     },
     {
      "type": "to-do",
      "attributes": {
       "title": "Book flights",
       "when": "today"
      }
     },
     {
      "type": "to-do",
      "attributes": {
       "title": "Research",
       "checklist-items": [
        {
         "type": "checklist-item",
         "attributes": {
          "title": "Hotels",
          "completed": true
         }
        },
        {
         "type": "checklist-item",
         "attributes": {
          "title": "Transport from airport"
         }
        }
       ]
      }
     }
    ]
   }
  },
  {
   "type": "to-do",
   "attributes": {
    "title": "Pick up dry cleaning",
    "when": "evening",
    "tags": [
     "Errand"
    ]
   }
  },
  {
   "type": "to-do",
   "attributes": {
    "title": "Submit report",
    "deadline": "2018-02-01",
    "list": "Work"
   }
  }
 ]

```

All of the above JSON examples must have the white space removed and then be URL encoded before they can be used. For example:
```
things:///json?data=
 [
  {
   "type": "to-do",
   "attributes": {
    "title": "Buy milk"
   }
  }
 ]

```

Deprecated. The command can be used for adding items via JSON.
Didn’t find what you were looking for? 


String. The title of the to-do to add. Ignored if titles is also specified.
String separated by new lines (encoded to %0a). Use instead of title to create multiple to-dos. Takes priority over title and show-quick-entry. The other parameters are applied to all the created to-dos.
Boolean. Whether or not the to-do should be set to complete. Default: false. Ignored if canceled is also set to true.
Boolean. Whether or not the to-do should be set to canceled. Default: false. Takes priority over completed.
Boolean. Whether or not to show the quick entry dialog (populated with the provided data) instead of adding a new to-do. Ignored if titles is specified. Default: false.
Boolean. Whether or not to navigate to and show the newly created to-do. If multiple to-dos have been created, the first one will be shown. Ignored if show-quick-entry is also set to true. Default: false.
String. The text to use for the notes field of the to-do. Maximum unencoded length: 10,000 characters.
String separated by new lines (encoded to %0a). Checklist items to add to the to-do (maximum of 100).
String. Possible values: today, tomorrow, evening, anytime, someday, a date string, or a date time string. Using a date time string adds a reminder for that time. The time component is ignored if anytime or someday is specified.
Date string. The deadline to apply to the to-do.
Comma separated strings corresponding to the titles of tags. Does not apply a tag if the specified tag doesn’t exist.
String. The title of a project or area to add to. Ignored if list-id is present.
String. The ID of a project or area to add to. Takes precedence over list.
String. The title of a heading within a project to add to. Ignored if heading-id is present, if a project is not specified, or if the heading doesn’t exist.
ISO8601 date time string. The date to set as the creation date for the to-do in the database. Ignored if the date is in the future.
ISO8601 date time string. The date to set as the completion date for the to-do in the database. Ignored if the to-do is not completed or canceled, or if the date is in the future.
String. The title of the project.
Boolean. Whether or not the project should be set to complete. Default: false. Ignored if canceled is also set to true. Will set all child to-dos to be completed.
Boolean. Whether or not the project should be set to canceled. Default: false. Takes priority over completed. Will set all child to-dos to be canceled.
Boolean. Whether or not to navigate into the newly created project. Default: false.
String. The text to use for the notes field of the project. Maximum unencoded length: 10,000 characters.
String. Possible values: today, tomorrow, evening, anytime, someday, a date string, or a date time string. Using a date time string adds a reminder for that time. The time component is ignored if anytime or someday is specified.
Date string. The deadline to apply to the project.
Comma separated strings corresponding to the titles of tags. Does not apply a tag if the specified tag doesn’t exist.
String. The title of an area to add to. Ignored if area-id is present.
String. The ID of an area to add to. Takes precedence over area.
String separated by new lines (encoded to %0a). Titles of to-dos to create inside the project.
ISO8601 date time string. The date to set as the creation date for the project in the database. If the to-dos parameter is also specified, this date is applied to them, too. Ignored if the date is in the future.
ISO8601 date time string. The date to set as the completion date for the project in the database. If the to-dos parameter is also specified, this date is applied to them, too. Ignored if the to-do is not completed or canceled, or if the date is in the future.
String. The Things URL scheme authorization token.
String. The ID of the to-do to update. Required.
String. The title of the to-do. This will replace the existing title.
Boolean. Complete a to-do or set a to-do to incomplete. Ignored if canceled is also set to true. Setting completed=false on a canceled to-do will also mark it as incomplete. This field cannot be updated on repeating to-dos.
Boolean. Cancel a to-do or set a to-do to incomplete. Takes priority over completed. Setting canceled=false on a completed to-do will also mark it as incomplete. This field cannot be updated on repeating to-dos.
Boolean. Whether or not to navigate to and show the updated to-do. Default: false.
Boolean. Set to true to duplicate the to-do before updating it, leaving the original to-do untouched. Repeating to-dos cannot be duplicated. Default: false.
String. The notes of the to-do. This will replace the existing notes. Maximum unencoded length: 10,000 characters.
String. Text to add before the existing notes of a to-do. Maximum unencoded length: 10,000 characters.
String. Text to add after the existing notes of a to-do. Maximum unencoded length: 10,000 characters.
String. Set the when field of a to-do. Possible values: today, tomorrow, evening, someday, a date string, or a date time string. Including a time adds a reminder for that time. The time component is ignored if someday is specified. This field cannot be updated on repeating to-dos.
Date string. The deadline to apply to the to-do. This field cannot be updated on repeating to-dos.
Comma separated strings corresponding to the titles of tags. Replaces all current tags. Does not apply a tag if the specified tag doesn’t exist.
Comma separated strings corresponding to the titles of tags. Adds the specified tags to a to-do. Does not apply a tag if the specified tag doesn’t exist.
\n (encoded to %0a) separated strings. Set the checklist items of the to-do (maximum of 100). Will replace all existing checklist items.
\n (encoded to %0a) separated strings. Add checklist items to the front of the list of checklist items in the to-do (maximum of 100).
\n (encoded to %0a) separated strings. Add checklist items to the end of the list of checklist items in the to-do (maximum of 100).
String. The title of a project or area to move the to-do into. Ignored if list-id is present.
String. The ID of a project or area to move the to-do into. Takes precedence over list.
String. The title of a heading within a project to move the to-do to. Ignored if heading-id is present, or if the to-do is not in a project with the specified heading. Can be used together with list or list-id.
ISO8601 date time string. Set the creation date for the to-do in the database. Ignored if the date is in the future.
ISO8601 date time string. Set the completion date for the to-do in the database. Ignored if the to-do is not completed or canceled, or if the date is in the future. This field cannot be updated on repeating to-dos.
String. The Things URL scheme authorization token.
String. The ID of the project to update. Required.
String. The title of the project. This will replace the existing title.
Boolean. Complete a project or set a project to incomplete. Ignored if canceled is also set to true. Setting to true will be ignored unless all child to-dos are completed or canceled and all child headings archived. Setting to false on a canceled project will mark it as incomplete. This field cannot be updated on repeating projects.
Boolean. Cancel a project or set a project to incomplete. Takes priority over completed. Setting to true will be ignored unless all child to-dos are completed or canceled and all child headings archived. Setting to false on a completed project will mark it as incomplete. This field cannot be updated on repeating projects.
Boolean. Whether or not to navigate to and show the updated project. Default: false.
Boolean. Set to true to duplicate the project before updating it, leaving the original project untouched. Repeating projects cannot be duplicated. Default: false.
String. The notes of the project. This will replace the existing notes. Maximum unencoded length: 10,000 characters.
String. Text to add before the existing notes of a project. Maximum unencoded length: 10,000 characters.
String. Text to add after the existing notes of a project. Maximum unencoded length: 10,000 characters.
String. Set the when field of a project. Possible values: today, tomorrow, evening, someday, a date string, or a date time string. Including a time adds a reminder for that time. The time component is ignored if someday is specified. This field cannot be updated on repeating projects.
Date string. The deadline to apply to the project. This field cannot be updated on repeating projects.
Comma separated strings corresponding to the titles of tags. Replaces all current tags. Does not apply a tag if the specified tag doesn’t exist.
Comma separated strings corresponding to the titles of tags. Adds the specified tags to a project. Does not apply a tag if the specified tag doesn’t exist.
String. The title of an area to move the project into. Ignored if area-id is present.
String. The ID of an area to move the project into. Takes precedence over area.
ISO8601 date time string. Set the creation date for the project in the database. Ignored if the date is in the future.
ISO8601 date time string. Set the completion date for the project in the database. Ignored if the project is not completed or canceled, or if the date is in the future. This field cannot be updated on repeating projects.
String. The ID of an area, project, tag or to-do to show; or one of the following built-in list IDs: inbox, today, anytime, upcoming, someday, logbook, tomorrow, deadlines, repeating, all-projects, logged-projects. Takes precedence over query.
String. The name of an area, project, tag or a built-in list to show. This is equivalent to entering the query text in to the quick find within Things and selecting the first result. Ignored if id is also set. Note: task cannot be shown using the query parameter; use the id parameter or the search command instead.
String. Comma separated strings corresponding to the titles of tags that the list should be filtered by.
JSON string. The JSON should be an array containing to-do and project objects (see bel[<35;65;18Mow).
String. The Things URL scheme authorization token. This is required whenever the provided JSON data contains an update operation.
Boolean. Whether or not to navigate to and show the newly created to-do or project. If multiple items have been created, the first one will be shown. Default: false.


```

File: /Users/darin/docs/culturedcode.com/things/support/articles/2803579.md
```md
---
title: Scheduling To-Dos in Things - Things Support
url: https://culturedcode.com/things/support/articles/2803579
scraped_at: 2025-07-02 14:48:44
---

# Scheduling To-Dos in Things - Things Support

In Things, you control when to-dos come to your attention. Curate what you see in , plan ahead to keep moving towards your goals, and store vague ideas until you have time to review them.


Things comes with default lists that organize to-dos by they can be done. belongs to one of these lists:
  * (including the optional section) lists everything that needs to get done today.
  * contains all the to-dos you can’t work on now but have planned for the future.
  * holds all to-dos that can be tackled “at any time” – they aren’t blocked by a lack of resources or a start date.
  * is for everything that’s not clear yet but might become actionable at a later time.

###### [What’s the purpose of each list? Learn more about Today, Upcoming, Anytime, and Someday. ](https://culturedcode.com/things/support/articles/4001304/)
The default lists cannot be renamed, removed, or re-ordered. However, if you prefer, you can work directly out of areas or projects.
To add, modify, or remove dates and reminders, go through the date picker. It allows you to assign to-dos to any of the default date-based lists. Here’s how to access it:
  * Hit the calendar icon inside a task if it doesn’t have a date yet.
  * Hit the date assignment inside the task if it’s already scheduled.
  * Or select a to-do and use on or .


The date picker offers shortcuts for , , and . By selecting a start date from the calendar grid, the to-do is assigned to . The button removes any existing schedules and assigns the task to .
(1) Schedule an undated to-do. (2) Reschedule a to-do via natural language. (3) Remove a date-assignment.
(1) Schedule an undated to-do. (2) Reschedule a to-do via natural language. (3) Remove a date-assignment.
The date picker answers the question of “When will I start working on this to-do?” Unlike a calendar, where you schedule your appointments for durations, a start date in Things merely indicates the day on which you want to begin work on a to-do. For example, a task with a future start date hibernates in until that date arrives and then hops over into to remind you to tackle it.
In addition to selecting options from the date picker, you can also use natural language to quickly set a future date, or keyboard shortcuts to circumvent the date picker entirely. Follow the links below to learn more.
[Keyboard Shortcuts for iPad & Vision](https://culturedcode.com/things/support/articles/2939808/)
Sometimes, a gentle nudge can be helpful to remember that it’s time to begin work on a project or task. Add a reminder and receive a notification when that time arrives.
[ Learn how to get notifications for time-sensitive to-dos. ](https://culturedcode.com/things/support/articles/2803585/)
Deadlines are added through the flag button. Contrary to start dates, which describe when you want to working on a task, deadlines define the date by which you must the to-do. Usually, deadlines are tied to external pressure, and missing them could incur negative consequences: Haven’t paid a bill? There might be late fees. Didn’t finish the report for your boss on time? It might come up during your yearly review.
Tasks with a deadline remain active in Anytime. If you need more than a day to finish them, add a start date a few days prior to the deadline. 
  * On Mac: Click the button inside a to-do.
  * On iPad & iPhone: Tap the button inside a to-do.
  * On Mac, iPad, and Vision: Use a or .


To remove a deadline from a to-do or project, tap the deadline and hit the button inside the date picker.
In addition to the default lists, Things also has two special date-based lists that you can access via Quick Find:
  * limits your focus to the to-dos you’ve planned for the next day.
  * shows all items with a deadline, in chronological order.


To access these lists, just type their name into . You can also create a for them, or access them through a custom .
Didn’t find what you were looking for? 


Except for unprocessed to-dos in the Inbox.
To assign a to-do to Anytime from the Inbox, use → .
This will assign the to-do to Upcoming until the start date arrives. Then the task will hop over to Today. The days remaining until the deadline will show next to the to-do and count down.


```

File: /Users/darin/docs/culturedcode.com/things/support/articles/3289315.md
```md
---
title: How to Prioritize To-Dos in Things - Things Support
url: https://culturedcode.com/things/support/articles/3289315
scraped_at: 2025-07-02 14:48:44
---

# How to Prioritize To-Dos in Things - Things Support

#  How to Prioritize To-Dos in Things 
_This article is part of a series of articles that offer ideas on using Things in your daily life – it’s meant to inspire and guide, not dictate. Feel free to adapt the suggestions to fit your needs._
In Things, prioritizing to-dos is as easy as adding them to your list. This gives you a clear view of what to finish before the end of the day. In addition, you can drag and drop to-dos in the order you want to tackle them, placing more important tasks at the top.
When you have a really long list, assign custom priority labels to your to-dos. In Things, are the perfect tool for this. They also make it possible to locate these to-dos across multiple lists, or across multiple days on your schedule.
Here’s how to use them.
## Use tags to prioritize to-dos
We recommend that you start off simple by creating a single tag, for example . Then apply this tag to your important to-dos by pressing the button inside the open to-do.
If you need more than a single priority tag, you can of course create as many as you want. But we do suggest you try working with just for a while to see if it fits your needs. It’s a simpler workflow, and you don’t have to constantly evaluate where to-dos fall on a subjective scale of importance. 
For detailed instructions on creating and applying tags, visit .
Viewing your priorities is easy, too:
. In a list, apply a filter to hide everything but the to-dos you need to focus on. Things smartly only offers filters for tags used in the current list, so it’s easy to spot if you even have anything important going on or not.
On the left: Your entire list, unfiltered. On the right: The tag is selected and narrows your focus to the to-dos with the highest importance.
. To see all of your important to-dos at once, use . You’ll jump directly into a dedicated tag list, which shows all to-dos with that tag, no matter where they live in Things.
Search for your tag to jump directly into the tag list. Results are neatly grouped by parent list.
. To quickly glance at your important to-dos, add a widget to your Home Screen. It can show you a filtered view, or the search results across all of Things.
A widget can display your important to-dos at a glance. It can also launch you directly into your tag-filtered view inside the app.
## Make it fit your needs
As we mentioned above, we recommend starting with a single priority tag. This gives you a simple “on/off” system for elevating your high-priority to-dos above the rest.
But if you find that you need more than one tag, maybe a set like and will suit you better; or a different approach where you identify and to-dos will drive your focus. There’s no right or wrong here—what matters is finding what works best for you. Don’t hesitate to experiment.
Lastly, don’t forget that you can give a to-do both a tag and a date. Maybe something isn’t important right now, but you already know it’ll be the top to-do for you on the weekend. Save yourself some effort by scheduling the to-do for the weekend, and when you launch Things into the list on that day, it will be right there waiting for you.
We hope this inspires you to take another look at how tags can help you better organize your to-dos. Find more resources to support this workflow below, and if you need any extra help, get in touch with our support team.


Didn’t find what you were looking for? 


Tap & hold the widget to configure it. .


```

File: /Users/darin/docs/culturedcode.com/things/support/articles/4001304.md
```md
---
title: An In-Depth Look at Today, Upcoming, Anytime, and Someday - Things Support
url: https://culturedcode.com/things/support/articles/4001304
scraped_at: 2025-07-02 14:48:44
---

# An In-Depth Look at Today, Upcoming, Anytime, and Someday - Things Support

#  An In-Depth Look at Today, Upcoming, Anytime, and Someday 
The default, date-based lists in Things allow you to control when tasks come to your attention.
In , you can look at your to-dos from two different perspectives: The first is , provided by areas and projects that you create yourself. The other way to view to-dos is by looking at you are going to do them.
Things provides several default lists that help you plan the current day, and what you want to achieve in the future. This page explains the purpose of each of these default lists.
is the list for to-dos that you want to start before the day ends. They’re your priorities.
Think of it as a filter across the entire app: if the , , or of any to-do matches today’s date, it shows up here. Enable to also see today’s calendar events at the top.
Ideally, start the day by quickly reviewing the list – works best if it contains only those to-dos you‘ll work on today. Then, drag and drop to-dos into the order you’ll most likely tackle them. Pick whatever is at the top when you come back throughout the day.
💡Tip: If your list is very long, you might prefer having it grouped by project or area instead. Enable this in Things → Settings → General. This setting will sync to your other devices.
If something needs to be handled later in the day, assign it to . These to-dos will move into their own section at the bottom – still present, so you know there’s more to do, but unobtrusive enough to not bother you until you have time.
As you go about your day, check off what you’ve . If you aren’t able to finish everything, you can easily reschedule the remaining items for another day.
The list is your future agenda: a place for tasks that you can't tackle right now but want to conquer on a specific day down the road.
For example: It’s the middle of the week, and you realize that your bedroom needs a new coat of paint. This is more of a weekend task, and you don’t need to see it during the workweek. Simply schedule the to-do for next Saturday, then forget about it. Come Saturday, it hops into Today, a gentle nudge of commitment.
At the top of , you’ll see the next seven days listed separately, starting with tomorrow. This bird's-eye view of the upcoming week helps to prevent overloading a single day during your weekly review, and you can tell at first glance what’s next. Change a to-do’s start date by simply dragging and dropping it on another day.
To ensure your focus remains on what you can do right now, projects with start dates from the sidebar (Mac/iPad) and the main lists view (iPhone) while they’re in hibernation mode. Within projects, inactive to-dos take a back seat beneath their active counterparts.
Once their start date arrives, the inactive to-dos from transform into actionable items in Today and projects reappear in the sidebar.
[ Learn how to plan to-dos and projects to see them when they become relevant. ](https://culturedcode.com/things/support/articles/2803579/#gxir)
As the name implies, the content in can be tackled “at any time” – nothing’s blocking you from working on any task in this list right now. Because the list contains only to-dos, its contents and what you see in Upcoming and Someday are mutually exclusive.
Unlike tasks with future start dates, those with deadlines will remain in as they are active and can be tackled at any time. 
Additionally, Today‘s tasks will appear in with a yellow star in front of them because they are also active tasks that can be done at any time. Once you’ve completed these priorities, come back here and pick out more to-dos.
The order of to-dos in reflects the sidebar/main lists view: loose to-dos without a parent ( project or area) float at the top, and then to-dos are grouped under their direct parent list. If one of your projects or areas doesn’t contain any active to-dos the list’s name will not appear here, to keep everything tidy.
All the other date-based lists contain to-dos that you have a very clear vision for: they are ready to be tackled at any time, or when their start date arrives.
The content in falls on the other end of the spectrum: there’s no plan for it yet, and you might decide to discard some of it eventually.
Why, then, would you keep something so vague around? Well, let’s be honest – we don’t always have all the answers right away, or the time to look for them.
Picture this: you stumble upon an article about watercolor painting and think, “Hey, that could be a cool hobby!” Or maybe a friend shares something about their job, and you get an idea for improving your own workplace. With either one of these ideas you might lack a clear starting point or the time to dive in right now. Instead of dismissing them, though, capture these ideas to . This keeps them safe until you can think more about how or if you want to realize them.
While they slumber in , neither to-dos nor projects will show up in Anytime or Upcoming, and inactive projects disappear from the sidebar. They are also designed to take a backseat . This way, these inactive items won’t distract you from what's actionable right now.
Review this list every couple of months. Nothing here is urgent, but you might find that – as time has passed – your perspective on some ideas has changed, and you finally have the time look into watercolor classes.
Although not a date-based list, the is one of Things’ default lists. It’s a staging ground for your unprocessed thoughts.
You can send tasks here via , on the Mac, or by adding to-dos while you are . It’s ok if you don’t know the exact title for these tasks yet, or haven’t added any details. The purpose of the is simply to catch everything you throw at it.
Of course, after filling it up, it’s helpful to regularly review your and turn each thought, email, or link into a . Even if you don’t get through everything, clarifying what you’ve captured will make it easier to stay focused.
After you’ve moved a to-do to a list, or assigned it a future date, it’ll move out of the . A temporary section will appear at its bottom, labeled “x to-dos were moved out of the Inbox”. It’ll disappear once you jump into another list, so feel free to ignore it. 
For completeness’ sake, the last default list – the – deserves a short mention. It serves an as archive: all your completed or cancelled to-dos and end up here.
To include logged to-dos or projects in a search, follow the tips . If you want to review only logged projects, type “Logged Projects” into search. Every logged item stays in the indefinitely, a complete reference for everything you’ve achieved in the past.
If you want to clear it out, you can use to select everything on Mac or . On iPhone, you’ll have to create a custom to do it for you, or use the to grab batches of to-dos to delete them. Deletions on iPhone, iPad, and Vision are permanent and can’t be undone. On Mac, empty the Trash to permanently erase content.
  * [iPad & Vision Keyboard Shortcuts](https://culturedcode.com/things/support/articles/2939808/)


Didn’t find what you were looking for? 


Need to find your completed to-dos again? They are stored in the .
Use the dialog to easily add to-dos to inactive projects.
They will appear in Upcoming to provide a quick overview of future days’ workload.
The checkboxes of to-dos are outlined in a dashed line instead of a solid one. The same goes for a project’s progress circle.
For example: turn the title “Kindergarten vacay” into “Notify Kindergarten about our vacation dates”. Then add any necessary details inside the to-do (a phone number or email address to contact the Kindergarten). If necessary, give the to-do a reminder or deadline before filing it into its corresponding area (“Family”) or project (“Vacation in Rome”).
It can be useful, though, if you’ve assigned a date to a to-do but forgot to also send it to a list (or vice versa). Instead of hunting down the to-do in the app, just scroll to the bottom of the Inbox and keep editing it.
To complete a project, enter it and hit the circle in front of the project’s name.


```

File: /Users/darin/docs/culturedcode.com/things/support/articles/4438545.md
```md
---
title: Writing Notes in Things - Things Support
url: https://culturedcode.com/things/support/articles/4438545
scraped_at: 2025-07-02 14:48:44
---

# Writing Notes in Things - Things Support

It’s easy to add notes to to-dos and projects in Things. Although most notes will only be a line or two, others can be and include detailed plans, references, or brainstorms.
As a note gets longer, it becomes increasingly important to it to quickly find relevant information. Here are some ways Things can help.
  1. [ Search notes with Find in Text ](https://culturedcode.com/things/support/articles/4438545/#bejrz)


Bullet lists in Things are as easy to use as typing followed by a space. You can use them to organize information so that it’s easier to read.
In addition to using for bullets, you can also type , , or . To indent a row, simply put the cursor in front of the bullet and hit the key, or use on Mac and .
Keyboard shortcuts are localized. Please look up the correct combination for your keyboard’s language here: and .
You can format the text in the notes section to make it or , or to phrases that deserve extra attention. In long notes, add structure with .
is a bit different from the Rich Text editors (Apple Pages etc.) that you might be used to. To apply the formatting, you just need to add a few easily-accessible characters, like , , or . Things will then turn this Markdown syntax into styled notes or checklists. The special characters will remain visible, making it easy for you to edit them later on.
Learn more in our .
### Use keyboard shortcuts or the menu to format text
If you are used to doing everything from the keyboard, then you’ll be happy to discover that you can fall back on shortcuts, and they are the same between the Mac, iPad, and Vision. The most common ones you’ll probably already know: makes text and makes it . 
Learn more about keyboard shortcuts and .
If you have trouble remembering the basic Markdown syntax, you can also use menus to style your text.
  1. On your Mac, open Things.
  2. Select any text inside section of a to-do or project.
  3. Right-click on the selection and select → .


Alternatively, you can also go to the menu bar at the top of your screen and click → .
  1. On your mobile device, open Things.
  2. Open a to-do and tap inside section or a text selection.
  3. In the pop-over, tap and select the style you want to use.


For more style options, hit at the end of the popover.
In for Vision, please follow the same steps as described in the tab above.
On the Mac, autocorrect and substitutions in the notes section can be customized. Here's how:
  1. Right-click into the notes section.
  2. Check or uncheck options according to your preferences.


On mobile devices, these settings are global and can’t be changed on a per-app basis.
If you want to write code snippets or commands in the notes and keep dumb quotes and dashes, but have smart quotes and dashes in regular text, use code fences:
## Search notes with Find in Text
With longer notes you might need some help quickly locating a specific word or phrase.
The content of notes was already included in searches when using → . With the new feature, the scope of the search is narrowed down to the note you are working on.
Of course, you can trigger from the keyboard on both and . If you prefer using the menu, here’s how:
  1. On your Mac, open Things.
  2. Open a to-do or project.
  3. Place your cursor inside the note or checklist.
  4. In the menu bar at the top of your screen, click → 


Hold down while in to change the menu to **Find and Replace in Text**.
  1. On your mobile device, open Things.
  2. Tap > in the at the bottom. 


At this time, Find is limited to notes inside of on mobile devices. Find in Text is not available in checklists and project notes.
On an iPad with a hardware keyboard, you can also use these .
In for Vision, please follow the same steps as described in the tab above. 

Can I hide the Markdown syntax?
    No. Though we might consider hiding links in the future. 

Can I style my to-do titles?
    In order to keep your lists looking tidy, the styling will show in to-do titles or names of projects or areas. For eye-catching titles, consider using . 

Can I change the text size?
    Yes. You can adjust the size of the text in Things on all of your devices. . 

Can I change the text color?
    No, it’s not possible to change the text color. 

Can I hide links behind text?
    Not at this time. Links will be displayed at full length. 

Can I use buttons instead of writing these special characters?
    Yes, there are menu options. to see them. 

Can I add images to my notes?
    Images, or attachments of any kind, are not supported at this time. You can upload them to a cloud service and copy the URL to your photo or file into the notes, though.
  * [Changing the text size in Things](https://culturedcode.com/things/support/articles/8537373/)


Didn’t find what you were looking for? 


Each to-do in Things can contain a note of up to 40,000 characters.
Formatting will not be applied to the title. Formatting in checklists is limited.
Formatting will not be applied to the title. Formatting in checklists is limited.
Don’t see the toolbar? Dismiss the keyboard to make it appear.
All Operating Sytems come with a large selection of emojis. You can add them to the titles of your to-dos, lists, or even tags to make some pop out more.


```

File: /Users/darin/docs/culturedcode.com/things/support/articles/4651820.md
```md
---
title: Markdown Guide - Things Support
url: https://culturedcode.com/things/support/articles/4651820
scraped_at: 2025-07-02 14:48:44
---

# Markdown Guide - Things Support

Things supports Markdown for formatting text in your notes. It allows you to add style and structure by typing a few special punctuation marks.
If you don’t know Markdown, here’s how it works. To emphasize a word, surround it with asterisks, like so: . Things will detect this and render the word in italics. If you remove the asterisks, it goes back to normal again. ​Here are a few more examples: ​
Things detects the Markdown characters and applies the desired style. 
And that’s it! You now know Markdown. The examples above show the most useful features for structuring and styling your notes, and you can go ahead and try it yourself.
These styles can also be applied via keyboard shortcuts like for italics, and for bold.
On the Mac, there’s a formatting menu in → . On iOS, you can double-tap a word to select it, then tap and choose a style from the popover.
Here’s an overview of all the Markdown styles you can use to structure your notes. If a keyboard shortcut is available, we've also listed it here. 
  * To make a heading, use hashes at the beginning of a line, followed by a space.


  * To add emphasis, put an asterisk around the text.
  * You can also use an underscore instead.


  * To add strong emphasis, put two asterisks around the text.
  * You can also use underscores instead.


  * To call attention to a part of your text, wrap it in double-colons.


  * Wrap words in two tildes to strike them through.


  * To quote a block of text, use followed by a space.


  * To write lists, simply type and some text.
  * You can also use , , or to start a list.
  * To increase or decrease list indentation, use or .
  * To convert selected text to a list, use .


  * To write numbered lists, type followed by some text.
  * To increase or decrease list indentation, use or .
  * To convert selected text to a numbered list, use .


Task List ... ... 
  * To write task lists, type followed by some text.
  * Mark a task complete like so: . You can also use .
  * Mark a task canceled like so: . You can also use .
  * To increase or decrease list indentation, use or .
  * To convert selected text to a task list, use .


  * To highlight a short string as code, wrap it in backticks.


  * For a multi-line block, use three at the beginning and end.
  * After the first three backticks you can note the language your code is written in. Things will not syntax-highlight any languages.
  * Any smart punctuation will be disabled when writing or pasting within code blocks.


  * Link syntax is supported for compatibility with other Markdown apps.
  * You don't have to use this syntax, Things will detect pasted links without it.


  * If you need to insert a break in your text, use three or more hyphens.
  * Alternatively, you can also use three or more asterisks.


Please note that the Markdown syntax is always displayed in Things. This is intentional and there’s no way to hide it (though we might at some point consider changing how links are displayed).


Didn’t find what you were looking for? 


Keyboard shortcuts are localized. If your keyboard does not have a US-English layout, check out the localized shortcuts for and .


```
</file_contents>

