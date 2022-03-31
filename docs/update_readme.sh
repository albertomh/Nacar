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

    source $VENV_DIR/bin/activate

    printf "    Installing requirements with pip.\n"
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

# Badges: Python 3.7+ | tests % | version
set_badges_in_readme() {
    printf "Setting badges in README.\n"
    local readme_path="$ROOT_DIR/README.md"

    # Set tests badge.
    local test_badge_re='\/badge\/tests.+?brightgreen'
    local new_test_badge="\/badge\/tests-${passed_count}%20"
    new_test_badge="${new_test_badge}%5B${passed_percent}%25%5D%20%E2%9C%94"
    new_test_badge="${new_test_badge}-brightgreen"
    sed -i -E "s/$test_badge_re/$new_test_badge/g" "$readme_path"
    printf "Set badge ( tests | ${passed_count}\U2714 [${passed_percent}%%] )\n"

    # Set version badge.
    local version_path="$ROOT_DIR/nacar/__version__.py"
    local version_text=$(cat $version_path)
    local version_re="__version__ = '([0-9]\.[0-9]\.[0-9])'"
    local version=""
    if [[ $version_text =~ $version_re ]]; then
        version=${BASH_REMATCH[1]}
    fi
    local version_badge_re='\/badge\/version.+?white'
    local new_version_badge="\/badge\/version-${version}-white"
    sed -i -E "s/$version_badge_re/$new_version_badge/g" "$readme_path"
    printf "Set badge ( version | ${version} )\n"
}

cleanup() {
    printf "Removing virtual environment at '/docs/.venv/'.\n"
    rm -rf $VENV_DIR
}


main() {
    printf "\n=============== BEGIN UPDATE_README ===============\n"

    create_venv

    run_tests

    set_badges_in_readme

    cleanup

    printf "======================= END =======================\n\n"
}
main
