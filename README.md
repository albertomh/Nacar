<img src="docs/img/nacar-wordmark-alt.svg" alt="Nacar" width="300"/>

Nacar is a tool for creating interactive text-based interfaces from user-defined blueprints.  
Say goodbye to remembering long, arcane shell commands!

**TODO: add side-by-side comparison video of a simple YAML blueprint and the resulting screen in bash.** 

You write a 'blueprint' of screens as a single YAML file, specifying the options and commands that should appear on each screen.
Additionally, you can link between screens for fluid keyboard-based navigation.  

Nacar will take that blueprint and produce a self-contained bash script containing your interface.

Both locally and on the server Nacar shines at creating management and 
health-check utilities that provide easy access to common tasks.     

Tested on Python 3.7+ | Type annotations checked by mypy | PEP8 compliant  


## Installing & running

TODO: document installing.


## Developing

Nacar is written in Python 3. It includes type annotations that are checked with 
`mypy` and is linted with `pycodestyle` to ensure PEP8 compliance.

1. Clone this repository and navigate into the project root.
2. Create a virtual environment: `python3 -m venv venv`.
3. Activate the virtual environment: `source venv/bin/activate`
4. Install dependencies: `pip3 install -r requirements/common.txt -r requirements/dev.txt`


## Project Structure

### Dependencies
Python dependencies are defined by two files in the `requirements` directory and 
can be installed using `pip`.  
`common.txt` defines the requirements necessary both for development and runtime, 
namely PyYAML for parsing YAML files and Cerberus for schema validation.  
`dev.txt` defines packages necessary only for development tasks, such as linting
and checking types.


### Application entrypoint


### Parsing blueprints


### Validator

Nacar's Validator verifies that the parsed blueprint will be correctly 
interpreted by a Translator (see below).  
It is built on top of the Cerberus validator, extending it to run checks not 
supported by Cerberus. These include checking that screen names are unique 
across a blueprint, verifying that screens do not link to themselves, 
and that 'link' directives point to existing screens.


### Translators

Translators are packages that take a Python object (previously parsed from a YAML blueprint) 
and turn it into a Nacar application written in a target language such as Bash.  
Translators live inside the `translate` package. Here you will also find an `itranslator.py` interface 
that defines the methods a translator should implement.  
The files for each translator should live inside a package of their own under `translate`.
This package should follow the naming convention `to_<target-language>`.

For instance, the default Blueprint to Bash translator lives under `translate/to_bash/`.  
Within this package there is a `to_bash.py` module which is the translator's entrypoint.  
All the methods defined by `itranslator.py` must be implemented by this module. 
The most important method is `translate_blueprint()` which returns the body of the bash program as a string.  

NOTE: Translators are only responsible for building valid programs (as strings) 
in a target language from objects in memory. Actually persisting this program 
(eg. as a `.sh` file) is the responsibility of the main loop in `nacar.py`, which 
will write the translator's output to a file by handing it to the `file_io` module.  


---
**What's in a name?**  
*Nacar* means 'mother of pearl' in Spanish. This name reflects the tool's 
aim to make interacting with the shell smoother and more beautiful.


---
Copyright 2022 Alberto Morón Hernández  
This software is provided as open-source under the MIT License.
