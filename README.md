 **Console Control**

Easy way to create commands in a console
- Parameter validation
- Instant help menu
- Command file format

Add commands:

menu_name.addcommand("command_name", method_name_without_parenthesis, d="description", p=list_of_parameters)

Available parameter types:
- "string"
- "int"
- "float"
- "complex"
- "bool"


The cm_... commands are to perform commands from a file

**cm_dir**

Prints all files that are in the correct format for cm_do.
The correct format just implies that the file starts with the line 
"%command%". Every subsequent line is treated as a command or parameter

**cm_t**

Prints the type that cm_do uses. 
"param" means that every line is a command's parameter. The third
parameter in this command is the command whose parameters is in the
given file.
"raw" means every line is a unique command, and does not need the last
paramter to be used. (Aka. 'com')

**cm_do**

Runs commands from a given file. The 'type' parameters is listed in
cm_t. The 'com' parameter is not used unless 'type' is "param", 
however a string should still be inserted for a placeholder