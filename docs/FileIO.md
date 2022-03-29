# File IO

The `file_io` module parses YAML files as input and writes in-memory 
representations of Nacar apps out as executable files. It is responsible for 
interacting with the filesystem, setting permissions on resulting apps, and 
handling any I/O exceptions.

An instance of this module is handed to the application entrypoint as a dependency. 


## parse_yml_file()
This method is responsible for checking a given YAML file exists at the given 
path, and if so will attempt to load its contents into memory as a Python dict.  
Performing this step also validates that the file in question is a valid YAML 
file. However, this does not guarantee the correctness of this file as a Nacar 
blueprint - that functionality is delegated to the `validator` module.

## make_file_executable()
Invoked when the final Nacar app is written to a file (see below) in order to 
make it executable. This method uses the standard library's `stat` module rather 
than raw octal values to aid readability.  
The file's default permissions are bitwise ORed with new permissions to make the
file executable by the owner, group, and others - effectively achieving the same 
result as invoking `chmod +x` on the file in question. 


---
Copyright 2022 Alberto Morón Hernández  
