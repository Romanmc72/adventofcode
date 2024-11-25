#!/usr/bin/env bash

set -euo pipefail

GITHUB_PACKAGE_LOCATION=github.com/Romanmc72/adventofcode/2024
SMALLEST_DAY=1
LARGEST_DAY=25

make_day() {
  day=$1
  day_text=$(printf %02d $day)
  mkdir -p "days/data/$day_text"
  echo "EXAMPLE!" > "./days/data/${day_text}/example.txt"
  echo "REAL DATA!" > "./days/data/${day_text}/input.txt"
  cat <<EOF > "./days/day_${day_text}.go"
package days

import (
	_ "embed"
	"fmt"

	"$GITHUB_PACKAGE_LOCATION/util"
)

//go:embed data/$day_text/input.txt
var real${day_text}Data []byte
//go:embed data/$day_text/example.txt
var example${day_text}Data []byte

func Solve$day_text(part int, example bool) error {
  logger := util.GetLogger()
	var data string
  if example {
    data = string(example${day_text}Data)
  } else {
    data = string(real${day_text}Data)
  }
  logger.Debug(data)
  if (part < 1 || part == 1) {
    fmt.Println("Day $day_text Part 1 Solution: _____")
  }
  if (part < 1 || part == 2) {
    fmt.Println("Day $day_text Part 2 Solution: _____")
  }
  return nil
}
EOF
  echo "Day ${day_text} has been populated"

}

main() {
    echo-help-and-exit() {
        echo '| make_days( $1 start_day, $2 end_day )'
        echo '+============================================================='
        echo '| Description'
        echo '| -----------'
        echo '| Generates the bare bones empty file structure for a given'
        echo '| day in the current way I have these golang programs set up.'
        echo '|'
        echo '| Params'
        echo '| ------'
        echo '| $1 : int : start_day'
        echo '| The day first day number that will be generated in the days folder'
        echo '| accompanying empty files and empty data directory.'
        echo '|'
        echo '| $2 : int : end_day'
        echo '| The last first day number that will be generated in the days folder'
        echo '| accompanying empty files and empty data directory.'
        echo '|'
        echo '| Example'
        echo '| -------'
        echo '| By running:'
        echo '|'
        echo '| `./make_days.sh 9 9`'
        echo '|'
        echo '| this script will erase the contents of folder ./days/data/09 if it'
        echo '| exists, then recreate that folder and inside of it place'
        echo '| the following file structure:'
        echo '|'
        echo '| └── ./days/'
        echo '|     ├── day_09.go'
        echo '|     └── data'
        echo '|         ├── example.txt'
        echo '|         └── input.txt'
        echo '|'
        echo ''
    }
    case "$#" in
        '2' )
            case "$1" in
                'h' | 'help' | '-h' | '--help' )
                    echo-help-and-exit
                    return 1
                    ;;
                * )
                    start_day=$1
                    end_day=$2
                    if [[
                      $start_day -lt $SMALLEST_DAY
                      || $start_day -gt $LARGEST_DAY
                      || $end_day -lt $SMALLEST_DAY
                      || $end_day -gt $LARGEST_DAY
                    ]]
                    then
                      echo "Need to use integers ${SMALLEST_DAY}-${LARGEST_DAY} for the days"
                      echo "start_day='$start_day'"
                      echo "end_day='$end_day'"
                      return 1
                    fi
                    echo "Creating days from $start_day to $end_day"
                    ;;
            esac
            ;;
        * )
            echo-help-and-exit
            return 1
            ;;
    esac

    if [[ $start_day -gt $end_day ]]
    then
      echo "Start day has to come on or before the end day you donkey. \U0001F434"
      echo "start_day=$start_day"
      echo "end_day=$end_day"
      echo-help-and-exit
      return 1
    fi
    i=$start_day
    while [[ $i -lt $(($end_day+1)) ]]
    do
      make_day $i
      i=$(($i+1))
    done
    echo "All days from $start_day to $end_day have been created!"
}



main $@
