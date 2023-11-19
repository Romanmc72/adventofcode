#!/usr/bin/env bash

set -euo pipefail

main() {
    # Runs all the tests in the test directory
    python3 -m unittest discover test
}

main
