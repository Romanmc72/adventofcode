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
)

//go:embed data/$day_text/input.txt
var real${day_text}Data []byte

//go:embed data/$day_text/example.txt
var example${day_text}Data []byte

func Solve$day_text(part int, example bool) error {
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

make_supporting_files() {
  echo 'Creating all supporting files...'
  cat <<EOF > main.go
package main

import (
	"flag"
	"fmt"
	"strconv"

	"github.com/Romanmc72/adventofcode/2024/days"
	"github.com/Romanmc72/adventofcode/2024/util"
)

func main() {
	day := flag.Int("day", 0, "The day to run the solution for. Pick a number from 1-25. Leaving the flag blank or zero will run ALL DAYS (not recommended).")
	part := flag.Int("part", 0, "The part to run for, choose 1 or 2. If left blank, then both parts will run for the chosen day(s).")
	example := flag.Bool("example", false, "Pass the flag in to run the example, otherwise run the main input.")
	flag.Parse()

	chosenDay := "ALL"
	chosenPart := "ALL"
	if *day > 0 && *day <= 25 {
		chosenDay = util.DayToFolder(*day)
	}
	if *part == 1 || *part == 2 {
		chosenPart = strconv.Itoa(*part)
	}

	logger := util.GetLogger()

	if *day == 0 {
		logger.Warn("Running for all the days!", "days", chosenDay, "part", chosenPart, "example", *example)
		for _, solve := range days.Solutions {
			err := solvePart(solve, *part, *example)
			if err != nil {
				logger.Error("Ran into an error on solving one of the parts!", "error", err)
				return
			}
		}
		return
	}

	index := *day - 1
	if index < -1 || index >= len(days.Solutions) {
		logger.Error("Could not find that day!", "day", day)
		return
	}
	fmt.Printf("Running for day=\`%s\` and part=\`%s\` example=\`%v\`...\n", chosenDay, chosenPart, *example)
	solve := days.Solutions[index]

	err := solvePart(solve, *part, *example)
	if err != nil {
		logger.Error("Ran into an error solving!", "error", err, "day", day, "part", part, "example", example)
		return
	}
	fmt.Println("Done!")
}

func solvePart(solver days.Solution, part int, example bool) error {
	if part == 0 || part == 1 {
		err := solver(1, example)
		if err != nil {
			return err
		}
	}
	if part == 0 || part == 2 {
		err := solver(2, example)
		if err != nil {
			return err
		}
	}
	if part < 0 || part > 2 {
		return fmt.Errorf("unable to parse the provided part number, use 0, 1, or 2 part=\`%d\`", part)
	}
	return nil
}
EOF
  mkdir -p util
  cat <<EOF > util/day.go
package util

import "fmt"

func DayToFolder(day int) string {
	return fmt.Sprintf("%02d", day)
}
EOF
  cat <<EOF > util/day_test.go
package util

import (
	"testing"
)

func TestDayToFolder(t *testing.T) {
	type args struct{
		day int
		want string
	}
	testCases := []args{
		{
			day: 1,
			want: "01",
		},
		{
			day: 10,
			want: "10",
		},
		{
			day: 2000,
			want: "2000",
		},
	}
	for _, testCase := range testCases {
		got := DayToFolder(testCase.day)
		if got != testCase.want {
			t.Errorf("Wanted=%s but got=%s for DayToFolder(%d)", testCase.want, got, testCase.day)
		}
	}
}
EOF
  cat <<EOF > util/logger.go
package util

import (
	"log/slog"
	"os"
	"strings"
)

var levelMap = map[string]slog.Leveler{
	"DEBUG": slog.LevelDebug,
	"INFO": slog.LevelInfo,
	"WARN": slog.LevelWarn,
	"ERROR": slog.LevelError,
}

// Get the logger at the level of your choice! Set GO_LOG_LEVEL env var to change the level.
func GetLogger() (*slog.Logger) {
	levelText, ok := os.LookupEnv("LOG_LEVEL")
	var level slog.Leveler
	if !ok {
		level = slog.LevelDebug
	} else {
		level = levelMap[strings.ToUpper(levelText)]
	}
	handler := slog.NewJSONHandler(os.Stderr, &slog.HandlerOptions{Level: level})
	return slog.New(handler)
}
EOF
  mkdir -p days
  cat <<EOF > days/all_days.go
package days

import "$GITHUB_PACKAGE_LOCATION/util"

var logger = util.GetLogger()

type Solution func (int, bool) error

var Solutions = []Solution{
	Solve01,
	Solve02,
	Solve03,
	Solve04,
	Solve05,
	Solve06,
	Solve07,
	Solve08,
	Solve09,
	Solve10,
	Solve11,
	Solve12,
	Solve13,
	Solve14,
	Solve15,
	Solve16,
	Solve17,
	Solve18,
	Solve19,
	Solve20,
	Solve21,
	Solve22,
	Solve23,
	Solve24,
	Solve25,
}
EOF
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
        echo '| Otherwise pass in no flags and optionally create every day from 1-25'
        echo '| along with every supporting file.'
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
                    CREATE_ALL="false"
                    ;;
            esac
            ;;
        '0' )
          echo 'Create All Days and wipe everything? (y/n)'
          read y_or_n
          if [[ $y_or_n == "y" ]]
          then
            start_day=1
            end_day=25
            CREATE_ALL="true"
          else
            echo 'Then pick a few days to start with!'
            echo-help-and-exit
            return 1
          fi
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

    if [[ $CREATE_ALL == "true" ]]
    then
      make_supporting_files
    fi

    i=$start_day
    while [[ $i -lt $(($end_day+1)) ]]
    do
      make_day $i
      i=$(($i+1))
    done
    gofmt -w ./..
    echo "All days from $start_day to $end_day have been created!"
}

main $@
