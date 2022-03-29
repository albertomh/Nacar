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


---
Copyright 2022 Alberto Morón Hernández  
