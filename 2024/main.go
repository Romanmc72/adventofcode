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
	fmt.Printf("Running for day=`%s` and part=`%s` example=`%v`...\n", chosenDay, chosenPart, *example)
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
		return fmt.Errorf("unable to parse the provided part number, use 0, 1, or 2 part=`%d`", part)
	}
	return nil
}
