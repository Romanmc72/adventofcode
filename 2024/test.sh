#!/usr/bin/env bash

set -euo pipefail

COVERAGE_FILE=.coverage.out

main() {
  go test -v -coverprofile=$COVERAGE_FILE ./... && go tool cover -html=$COVERAGE_FILE && rm $COVERAGE_FILE
}

main $@
