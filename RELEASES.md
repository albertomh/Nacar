### 1.1.0
2022-04-17  
**The templating upgrade**
- Rewrote to use template-based translators, making them more lightweight and modular.
- No change to the user-facing API - ie. existing YML templates will continue to work.
- Made blueprint validation more robust by adding new checks, improving existing ones, and enhancing test coverage.
- Added git hook to automate running tests, running the PEP8 linter, mypy type checker, and updating README badges.


### 1.0.0
2022-03-08  
**MVP release**
- `FileIO` module: parses YAML files as input and writes in-memory representations of Nacar apps out as executable files. Interacts with the filesystem, sets permissions on resulting apps, and handles any I/O exceptions
- `Schema` module: defines the rules used for validating parsed blueprints.
- `Validator` module: built on top of the Cerberus validator. Verifies that the parsed blueprint will be correctly interpreted by a Translator.
- The `translate` package: contains Translators, packages that take a Python object (previously parsed from a YAML blueprint) and turn it into a Nacar application written in a target language such as bash.
`to_bash` translator module: implements the `ITranslator` interface to turn blueprints into bash Nacar apps.
- Test coverage: A suite of unit & integration tests is held under `/tests/`. It can be run with `pytest`.
