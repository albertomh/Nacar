# File IO

The `file_io` module parses YAML files as input and writes in-memory 
representations of Nacar apps out as executable files. It is responsible for 
interacting with the filesystem, setting permissions on resulting apps, and 
handling any I/O exceptions.

An instance of this module is handed to the application entrypoint as a dependency. 


---
Copyright 2022 Alberto Morón Hernández  
