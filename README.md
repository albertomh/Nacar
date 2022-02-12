# 🐚 Nacar

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

Nacar is written in Python 3. It includes type annotations that are checked with `mypy` and is linted with `pycodestyle` to conform to PEP8.

1. Clone this repository and navigate into the project root.
2. Create a virtual environment: `python3 -m venv venv`.
3. Activate the virtual environment: `source venv/bin/activate`
4. Install dependencies: `pip3 install -r requirements/common.txt -r requirements/dev.txt`

---
Copyright 2022 Alberto Morón Hernández  
This software is provided under the MIT License.
