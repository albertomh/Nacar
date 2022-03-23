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


## The InvalidSchemaError


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
