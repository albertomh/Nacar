# Translators

Translators are packages that take a Python object (previously parsed from a YAML blueprint) 
and turn it into a Nacar application written in a target language such as Bash.  
Translators live in the `translate` package. Here you will also find an `itranslator.py` interface 
that defines the methods a translator should implement.  


## Structure
The files for each translator should live inside a package of their own under `translate`.
This package should follow the naming convention `to_<target-language>`.

For instance, the default Blueprint to Bash translator lives under `translate/to_bash/`. 
Within this package there is a `to_bash.py` module which is the translator's entrypoint. 
All the methods defined by `itranslator.py` must be implemented by this module. 


## The `itranslator` interface

The most important method is `translate_blueprint()` which returns the body of 
the bash program as a string.  
`get_target_language()` must be defined and return a single option from the TargetLanguage enum.  

A compliant Translator comprises the following sections:

**<target_language> translator utilities**  

**File heading**  

**Nacar app config**  

**Utilities**  

**Screen-building utilities**  

**Screen flow**  

**Screen rendering**  

**Main loop**  

**Translate blueprint to <target_language>**  


---
Copyright 2022 Alberto Morón Hernández  
