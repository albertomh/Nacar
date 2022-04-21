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
