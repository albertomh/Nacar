#!/bin/bash

# Nacar
# Copyright 2022 Alberto Morón Hernández
# [github.com/albertomh/Nacar]
#
# Pre-commit checks
# ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
# Check types, lint code, and check style against PEP8.
# Run a full test suite and update badges in the README.md file.


SCRIPT_PATH=$(dirname $(realpath -s $0))
ROOT_DIR=$SCRIPT_PATH
# When invoked from a git hook, the context changes to the `.git/`
# directory. Use `pwd` instead when called by a git hook.
if [[ "$SCRIPT_PATH" == *".git"* ]]; then
    ROOT_DIR=$(pwd)
fi
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
    printf "\nRunning tests\n"
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

# Badges: Python 3.7+ | tests % | pep8 compliance | mypy validity | version
set_badges_in_readme() {
    printf "\nSetting badges in README.\n"
    local readme_path="$ROOT_DIR/README.md"

    # Set tests badge.
    local test_badge_re='\/badge\/tests.+?brightgreen'
    local new_test_badge="\/badge\/tests-${passed_count}%20"
    new_test_badge="${new_test_badge}%5B${passed_percent}%25%5D%20%E2%9C%94"
    new_test_badge="${new_test_badge}-brightgreen"
    sed -i -E "s/$test_badge_re/$new_test_badge/g" "$readme_path"
    printf "    Set badge ( tests | ${passed_count}\U2714 [${passed_percent}%%] )\n"

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
    printf "    Set badge ( version | ${version} )\n"

    # Set pycodestyle/PEP8 badge.
    local pep8_outcome="compliant"
    if [[ ! "$PEP8_STATUS" -eq "0" ]]; then
        pep8_outcome="not compliant"
    fi
    local pep8_badge_re='\/badge\/pep8.+?orange'
    local new_pep8_badge="\/badge\/pep8-${pep8_outcome}-orange"
    sed -i -E "s/$pep8_badge_re/$new_pep8_badge/g" "$readme_path"
    printf "    Set badge ( pep8 | ${pep8_outcome} types )\n"

    # Set mypy badge.
    local mypy_outcome="valid"
    if [[ ! "$MYPY_STATUS" -eq "0" ]]; then
        mypy_outcome="invalid"
    fi
    local mypy_badge_re='\/badge\/mypy.+?blueviolet'
    local new_mypy_badge="\/badge\/mypy-${mypy_outcome}%20types-blueviolet"
    sed -i -E "s/$mypy_badge_re/$new_mypy_badge/g" "$readme_path"
    printf "    Set badge ( mypy | ${mypy_outcome} types )\n"
}

cleanup() {
    printf "\nRemoving virtual environment at '/docs/.venv/'.\n"
    rm -rf $VENV_DIR
}

# ─────────────────────────────────────────────────────────────────────────────
PEP8_STATUS=0
MYPY_STATUS=0

main() {
    printf "\n───────────── BEGIN PRE_COMMIT_CHECKS ─────────────\n"

    create_venv

    printf "\nChecking style against PEP8\n"
    pycodestyle nacar
    PEP8_STATUS=$?

    printf "\nChecking types with mypy\n"
    mypy -p nacar
    MYPY_STATUS=$?

    run_tests

    set_badges_in_readme

    cleanup

    printf "─────────────────────── END ───────────────────────\n\n"
}
main
