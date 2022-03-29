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

## write_nacar_app_to_file()
Writes an in-memory representation of a Nacar app to a file and sets the relevant 
file modes. This is the last utility invoked by the entrypoint's `run()` method. 
It takes as parameters the content of the resulting Nacar app, the file path the 
app will be written to, and the target language:

The file content should be a string, the output of a 
[Translator's](./Translators.md) `translate_blueprint()` method.

The path argument is the absolute path where the resulting app will be written to. 
Customarily this file will be a sibling to the YAML blueprint, and have the 
same filename eg. the app created by running Nacar's bash translator on 
`app-blueprint.yml` should produce the file `app-blueprint.sh`.  

Finally, the target language argument should be a value of the `translate` 
module's `TargetLanguage` enum.


---
Copyright 2022 Alberto Morón Hernández  
