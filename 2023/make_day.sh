#!/usr/bin/env bash

set -euo pipefail

main() {
    echo-help-and-exit() {
        echo '| make_day( $1 )'
        echo '+============================================================='
        echo '| Description'
        echo '| -----------'
        echo '| Generates the bare bones empty file structure for a given'
        echo '| day in the current way I have these rust programs set up.'
        echo '|'
        echo '| Params'
        echo '| ------'
        echo '| $1 : string : day_to_create'
        echo '| The day number that will be generated as a folder with the'
        echo '| accompanying empty files and symlinked common code file.'
        echo '|'
        echo '| Example'
        echo '| -------'
        echo '| By running:'
        echo '|'
        echo '| `./make_day.sh 09`'
        echo '|'
        echo '| this script will erase the contents of folder ./09 if it'
        echo '| exists, then recreate that folder and inside of it place'
        echo '| the following file structure:'
        echo '|'
        echo '| └── 09'
        echo '|     ├── common.rs -> ../common.rs'
        echo '|     ├── example.txt'
        echo '|     ├── input.txt'
        echo '|     └── main.rs'
        echo '|'
        echo ''
    }
    case "$#" in
        '1' )
            case "$1" in
                'h' | 'help' | '-h' | '--help' )
                    echo-help-and-exit
                    return 1
                    ;;
                * )
                    day_to_create="$1"
                    ;;
            esac
            ;;
        * )
            echo-help-and-exit
            return 1
            ;;
    esac
    rm -rf "./${day_to_create}"
    mkdir "./${day_to_create}"
    touch "./${day_to_create}/example.txt"
    touch "./${day_to_create}/input.txt"
    touch "./${day_to_create}/main.rs"
    pushd "./${day_to_create}"
    ln -s ../common.rs common.rs
    popd
    echo "Folder ${day_to_create} has been populated"
}

main $@
