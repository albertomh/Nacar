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

run_tests() {
    printf "Running tests\n"
    cd $ROOT_DIR
    local test_result=$(pytest -s | tail -n1)

    local total_count=0
    local failed_re='([0-9]+) failed'
    local failed_count=0
    local passed_re='([0-9]+) passed'
    passed_count=0
    if [[ $test_result =~ $failed_re ]]; then
        failed_count=${BASH_REMATCH[1]}
        total_count=$(($total_count + $failed_count))
    fi
    if [[ $test_result =~ $passed_re ]]; then
        passed_count=${BASH_REMATCH[1]}
        total_count=$(($total_count + $passed_count))
    fi

    passed_percent=0
    if [[ $total_count -gt 0 ]]; then
        passed_percent=$(( ( $passed_count * 100 ) / $total_count ))
    fi
}

cleanup() {
    printf "Removing virtual environment at '/docs/.venv/'.\n"
    rm -rf $VENV_DIR
}


main() {
    create_venv

    run_tests

    cleanup
}
main
