## Common Python3 code used anywhere in the project
A place to house common/repeated code that can be used anywhere in the project.

#### conf.py
Configuration for the project, such as table names and the path to the root of
the project

#### utils.py
Useful utility functions
* run_command(command) - runs a native command
* capture_command_output(command) - runs a native command and returns stdout and stderr
* get_user() - returns the name of the UNIX user running the script
* get_project_root_dir() - returns absolute path of the project root directory
