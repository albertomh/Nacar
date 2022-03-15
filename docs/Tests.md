# Tests

A full suite of unit tests is held under `/tests/`. To run it, install the dev 
requirements with  `pip3 install -r requirements/dev.txt` and run `pytest` from 
the project root.


## Running tests from PyCharm

1. Add a new configuration by clicking `Add Configuration...` in the top right corner.
2. Select `+` > `Python tests` > `pytest`.
3. Select `Script path` as the Target and enter the absolute path of the `/tests/` folder.  
   Optionally, enter `--capture=no` under `Additional Arguments` to pass output 
   to the console instead of having pytest capture it. 
4. Select the python binary in the virtual environment where all dependencies
are installed as the `Python interpreter`.
5. Finally, enter the absolute path to the Nacar root directory as the `Working directory`. 


## Fixtures

Fixtures shared by the entire test suite are defined in `/tests/conftest.py` 
and made available to the suite by importing in the relevant test modules.  
An example of one such code-defined fixture stored in `conftest` is a method 
that returns the location of the `test_data_dir` to allow tests to find YAML & 
JSON fixtures.
  
The directory `/tests/data/` holds YAML and JSON fixtures used by tests.


---
Copyright 2022 Alberto Morón Hernández  
