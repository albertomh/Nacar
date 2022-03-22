# Schema

Nacar's `schema` module defines the rules used for validating parsed blueprints.  
The resulting schema is a nested dictionary accepted by the Validator (see below).
This module also contains a number of utilities that can be used to answer 
questions about a given blueprint such as 'which screens does this contain?' or 
'how do said screens all link to each other?'. 


## Subschemas


## The blueprint schema


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
