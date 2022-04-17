# Schema

Nacar's `schema` module defines the rules used for validating parsed blueprints.  
The resulting schema is a nested dictionary accepted by the Validator (see below).
This module also contains a number of utilities that can be used to answer 
questions about a given blueprint such as 'which screens does this contain?' or 
'how do said screens all link to each other?'. 


## Subschemas
Subschemas are modular and composeable snippets built using nested dictionaries.  
They are defined in the `get_blueprint_subschemas` method. The aim behind using
subschemas rather than a massive main schema object is to make smaller sections
of the schema easier to debug and update.  
Subschemas are added to Cerberus' schema registry upon initialisation of a Nacar
Schema object.  


## The blueprint schema
The schema provided by `get_blueprint_schema` is the main object that defines 
how the modular subschemas fit in together to create a coherent schema against 
which all parsed blueprints are evaluated.  
It has three top-level properties named `title`, `meta`, and `screens`.  


## Schema utilities

**Subschemas and optional attributes**   
`get_blueprint_subschemas()` Return modular subschemas that can be used to recursively build more complex schemas against which to validate app blueprints.  
`add_blueprint_subschemas_to_registry()` Add modular blueprint schemas to Cerberus' default schema registry.  
`get_blueprint_schema()`  
`set_missing_optional_attributes()` Populate an in-memory blueprint with sensible defaults for missing attributes.  

**Getting blueprint properties**  
`get_screen_names()` Return a flat list of every screen name in the blueprint.  
`get_screen_links()` Return a list of [screen1, screen2] pairs showing how screens link to other screens.  
`get_max_screen_options_in_blueprint()` Return the number of options in the screen with most options.   
`get_options_for_screen()`  


## The InvalidSchemaError
The `InvalidSchemaError` is a custom exception raised by `main::run()` when the
Validator's `validate()` method returns False.  
It accepts a tree of validator errors as its only parameter. Its constructor
defines a recursive `walk_errors()` function that traverses the errors tree and
generates a dictionary of `breadcrumb: error description` pairs.  
When this exception is raised these validator errors are pretty-printed to the console.


---

# Validator

Nacar's `validator` module verifies that the parsed blueprint will be correctly 
interpreted by a [Translator](Translators.md).  
It is built on top of the [Cerberus](https://pypi.org/project/Cerberus/) 
validator, extending it to run checks not supported by Cerberus. These include 
checking that screen names are unique across a blueprint, verifying that screens
do not link to themselves, and that 'link' directives point to existing screens.


---
Copyright 2022 Alberto Morón Hernández  
