package days

import (
	_ "embed"
	"fmt"
	"slices"
	"strconv"
	"strings"

	"github.com/Romanmc72/adventofcode/2024/util"
)

//go:embed data/02/input.txt
var real02Data []byte

//go:embed data/02/example.txt
var example02Data []byte

func Solve02(part int, example bool) error {
	logger := util.GetLogger()
	var data string
	if example {
		data = string(example02Data)
	} else {
		data = string(real02Data)
	}
	logger.Debug(data)
	safeReports := 0
	safeReports2 := 0
	for _, line := range strings.Split(data, "\n") {
		report, err := parseLineToListOfInts(line, " ")
		if err != nil { return err }
		if isSafe(report) {
			safeReports += 1
		}
		if isSafe2(report) {
			safeReports2 += 1
		}
	}
	if part < 1 || part == 1 {
		fmt.Println("Day 02 Part 1 Solution: ", safeReports)
	}
	if part < 1 || part == 2 {
		fmt.Println("Day 02 Part 2 Solution: ", safeReports2)
	}
	return nil
}

func isSafe(report []int) bool {
	if len(report) <= 1 { return true }
	ptr := 0
	previousOrder := false
	for (ptr < len(report) - 1) {
		this := report[ptr]
		next := report[ptr + 1]
		newOrder := this > next
		if ptr > 0 {
			if previousOrder != newOrder {
				return false
			}
		}
		if !isSafeDistance(next, this) {
			return false
		}
		ptr += 1
		previousOrder = newOrder
	}
	return true
}

// brute force. it is fine. leave me alone
func isSafe2(report []int) bool {
	if len(report) <= 2 { return true }
	for index := 0; index < len(report); index++ {
		if isSafe(slices.Concat(report[:index], report[index+1:])) {
			return true
		}
	}
	return false
}

func isSafeDistance(num1 int, num2 int) bool {
	diff := num1 - num2
	if diff < 0 {
		diff = -diff
	}
	return !(diff > 3 || diff < 1)
}

func parseLineToListOfInts(line string, sep string) ([]int, error) {
	splits := strings.Split(line, sep)
	numbers := make([]int, len(splits))
	for index, value := range splits {
		num, err := strconv.Atoi(value)
		if err != nil {
			return []int{}, nil
		}
		numbers[index] = num
	}
	return numbers, nil
}
