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


---
Copyright 2022 Alberto Morón Hernández  
