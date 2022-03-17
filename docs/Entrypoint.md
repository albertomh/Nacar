# Application entrypoint

The `main.py` module is the script's entrypoint when it is run from the 
command line. It is responsible for running initial checks, catching any 
exceptions, and orchestrating core functionalities.

First the script verifies that it has been passed a path to a file, that this 
file exists, and that it is a YAML file.

If these checks are successful, the Nacar constructor is called.
The constructor takes instances of `FileIO`, `Schema`, and `NacarValidator` 
as its first three arguments. Finally, a reference to a Translator class (ie. a
class that extends `ITranslator` and overrides all its methods) must be passed 
as the fourth and final argument of the constructor. 

At this point a call to the `run()` method of the newly-created Nacar instance 
will be issued. This method consists of the following steps:
- Read the YAML file passed to the script and parsing it to an in-memory representation as a Python object.  
- Assemble the custom schema used to validate any candidate blueprints.  
- Pass this schema to the validator passed to the `Nacar()` constructor.
- If the validator approves of the blueprint it will add any missing optional attributes.]
- It will then instantiate the Translator and call `translate_blueprint()` on it.
- Finally, the translation is persisted to a file and the appropriate permissions 
  set to make it executable. This is the resulting 'Nacar app'.


---
Copyright 2022 Alberto Morón Hernández  
