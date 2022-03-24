<img src="docs/img/nacar-wordmark-alt.svg" alt="Nacar" width="300"/>

Nacar is a tool for creating interactive text-based interfaces from simple user-defined blueprints.  
Say goodbye to remembering long, arcane shell commands!

**TODO: add side-by-side comparison video of a simple YAML blueprint and the resulting screen in bash.** 

You write a blueprint as a single YAML file, specifying the options and commands 
that should appear on each screen. Add links between screens for fluid 
keyboard-based navigation. Nacar will take that blueprint and produce a 
self-contained bash script containing your interface.

Both locally and on the server Nacar shines at creating management and 
health-check utilities that provide easy access to common tasks.     

<p>
    <img id="badge--python" src="https://img.shields.io/badge/python-3.7%2B-blue" alt="" />
    <img id="badge--tests" src="https://img.shields.io/badge/tests-34%20%5B100%25%5D%20%E2%9C%94-brightgreen" alt="" />
</p>


## Installing & running

TODO: document installing.


## Developing

Nacar is written in Python 3. It includes type annotations that are checked with 
`mypy` and is linted with `pycodestyle` to ensure PEP8 compliance.

1. Clone this repository and navigate into the project root.
2. Create a virtual environment: `python3 -m venv venv`.
3. Activate the virtual environment: `source venv/bin/activate`
4. Install dependencies: `pip3 install -r requirements/common.txt -r requirements/dev.txt`

You can now run Nacar with `python3 nacar/nacar.py <path-to-blueprint>.yml`.  
If you wish to make changes to Nacar itself, read the **Project Structure** 
section below for details on how the code is structured.

Before committing your changes, perform the following steps:
1. Check type annotations: `mypy -p nacar`.
2. Lint in accordance with PEP8: `pycodestyle nacar`.
3. Run the test suite by running `pytest` from the project root.
4. Run `docs/update_readme.sh` to update the test results and version badges in the README.

### Testing
A suite of unit & integration tests is held under `/tests/`. To run it, install 
the dev requirements as detailed above and run `pytest` from the project root.  
[Read more](docs/Tests.md) about how tests are structured, available fixtures
 & test data, and running tests from PyCharm.


## Project Structure

### Dependencies
Python dependencies are defined by two files in the `requirements` directory and 
can be installed using `pip`.  
`common.txt` defines the requirements necessary both for development and runtime, 
namely PyYAML for parsing YAML files and Cerberus for schema validation.  
`dev.txt` defines packages necessary only for development tasks, such as linting
and checking types.


### Application Entrypoint
The `main.py` module is the script's entrypoint when it is run from the command
line. It is responsible for running initial checks, and orchestrating the core 
functionalities such as reading YAML blueprints, parsing them into an in-memory 
representation, validating the blueprint, translating to the target language, 
and persisting the result to a file.

[Read more](docs/Entrypoint.md) about Nacar's entrypoint.


### Parsing blueprints


### Blueprint Schema & Validator
Nacar's `validator` module verifies that the parsed blueprint will be correctly 
interpreted by a Translator (see below).  
It is built on top of the Cerberus validator, checking the uniqueness of screen 
names, avoiding screens linking to themselves, and that 'link' directives point 
to existing screens.

[Read more](docs/Schema_Validator.md) about the blueprint Schema & Validator.


### Translators
Translators are packages that take a Python object (previously parsed from a 
YAML blueprint) and turn it into a Nacar application written in a target 
language such as Bash. Translators live in the `translate` package along 
with an `itranslator.py` interface that defines the methods a translator 
should implement.

[Read more](docs/Translators.md) about Translators.


---
**What's in a name?**  
*Nacar* means 'mother of pearl' in Spanish. This name reflects the tool's 
aim to make interacting with the shell smoother and more beautiful.


---
Copyright 2022 Alberto Morón Hernández  
This software is provided as open-source under the MIT License.
