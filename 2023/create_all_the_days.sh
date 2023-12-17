#!/usr/bin/env bash

set -euo pipefail

main() {
    FORCE='FORCE'
    if [[ $1 == $FORCE ]]
    then
        echo 'Proceeding to wipe and recreat all the days...'
    else
        echo "You will need to say ${FORCE} for this to work, exiting."
        return 1
    fi
    for day in {1..25}
    do
        day=$(printf %02d $day)
        ./make_day $day
    done
}

main $@
