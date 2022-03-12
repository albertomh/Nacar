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
eg. Format comments according to the language spec, or return the maximum
line length (eg. as defined by PEP8 for Python).

**File heading**  
Get title, copyright, and info lines for the target Nacar app.

**Nacar app config**  
Nacar app settings (eg. screen width, title) used internally by the app itself, 
may be stored internally as constants in the output app code.

**Utilities**  
The code to create utilities for internal use by the target app. 
These may include methods to clear the screen, repeat a string, or set shell styles.

**Screen-building utilities**  
Methods called internally by the Nacar app to display screens in a composable manner.
There may be separate methods for drawing the top or bottom of screens, or display breadcrumbs.

**Screen flow**  
Generate code to create links between screens and navigate between them. Manage 
state variables holding the active screen or the current breadcrumb path. 
Dynamically define the input loop to listen for keystrokes.

**Screen rendering**  
Generate methods to show each screen as defined in the blueprint, invoke actions
when requested by the keystroke listener, and show the exit screen.

**Main loop**  
Show the relevant screen while an active screen is defined, handle behaviour on exit, and capture interrupts.

**Translate blueprint to <target_language>**  
A single method that brings together all the pieces performed by the above sections.


## Separation of concerns

Do note that Translators are only responsible for building valid programs (as strings) 
in a target language from objects in memory. Actually persisting this program 
(eg. as a `.sh` file) is the responsibility of the main loop in `nacar.py`, which 
will write the translator's output to a file by handing it to the `file_io` module.  


---
Copyright 2022 Alberto Morón Hernández  
