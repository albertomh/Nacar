# Nacar roadmap

## Schema
`Schema::set_missing_optional_attributes`
- Add more optional attributes to Schema.
- Extrapolate default values of optional attributes to a config file to make changing easier.
- Make more elegant by iterating over map of `attributepath: default` read from config file.

`Schema::get_options_for_screen`  
- Check if screen is in get_screen_names(blueprint) and throw exception if not.


## Validator
`NacarValidator::validate`  
- Enforce maximum nested screens level? e.g 4 or 5 max breadcrumb depth.


## Translator

`itranslator.py`  
- Add method that adds comments documenting all methods in the output script.

`BlueprintToBash::set_heading_template_variables`
- Test multiple authors.
- Add method to add comments documenting all methods in the output script.


## Main loop
`main::main`
- Add other target language translators and select via command line argument, with the Bash Translator as the default.


# blueprint.example.yml
- Add option to strip comments from target Nacar app bash file / minify target file.  
- Create a handful of colour schemes that can be selected with option.  
- Allow users to create custom colour schemes.  
- Enforce root node - first item in 'screens' array MUST have `name: home`.  
- Add optional 'key' item for links & actions (ensuring unique per screen), defaulting to [F]irst char.  


## Testing

`test_schema::test_set_missing_optional_attributes__meta_width()`
- Add other optional attributes to test parameters as they are added in `set_missing_optional_attributes()`.

`test_validator::test_cerberus_validation()`
- Add more per-attribute testcases to test parameters eg. wrong data type for attributes in YAML blueprint.
