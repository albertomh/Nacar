#!/bin/bash

# Nacar
# Copyright 2022 Alberto Morón Hernández
# [github.com/albertomh/Nacar]
#
# README updater
# ▔▔▔▔▔▔▔▔▔▔▔▔▔▔
# Run this script to update badges in the README.md file.


SCRIPT_PATH=$(dirname $(realpath -s $0))
ROOT_DIR=$(dirname "$SCRIPT_PATH")
VENV_DIR="$ROOT_DIR/docs/.venv/"

# Create a venv (if it doesn't exist) and install requirements.
create_venv() {
    if [ ! -d $VENV_DIR ]; then
        printf "Creating new virtual environment at '/docs/.venv/'.\n"
        python3 -m venv $VENV_DIR
    fi

    printf "Activating virtual environment.\n"
    source $VENV_DIR/bin/activate

    printf "Installing requirements with pip.\n"
    local requirements_dir="$ROOT_DIR/requirements"
    pip3 install \
    -r "$requirements_dir/common.txt" -r "$requirements_dir/dev.txt" \
    --quiet
}


main() {
    create_venv
}
main
