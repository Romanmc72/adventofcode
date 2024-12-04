package days

import (
	_ "embed"
	"fmt"
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

// Need to establish the overall order and return if it
// is violated but not track its ongoing state
// The list order can be determined definitively using the first
// 4 elements even if the error occurs in one of those positions.
//   {1, 2, 3, 4} ASC
//   {3, 2, 1, 0} DESC
//   {1, 5, 3, 4} ASC
//   {5, 1, 3, 4, ...} ASC   (remove first)
//   {1, 3, 2, 4, ...} ASC   (remove second)
//   {1, 2, 5, 4, ...} ASC   (remove third)
//   {2, 1, 3, 4} ERROR (jagged)
func isSafe2(report []int) bool {
	if len(report) <= 2 { return true }
	mulligan := true
	moveUpTheRear := false
	ptr := 1
	leadPtr := 2
	previousOrder := false
	for (leadPtr < len(report)) {
		this := report[ptr]
		next := report[leadPtr]
		newOrder := this > next
		if ptr > 0 {
			if previousOrder != newOrder {
				if !mulligan {
					return false
				}
				mulligan = false
				leadPtr += 1
				moveUpTheRear = true
				continue
			}
		}
		if !isSafeDistance(next, this) {
			if !mulligan {
				return false
			}
			mulligan = false
			leadPtr += 1
			moveUpTheRear = true
			continue
		}
		if moveUpTheRear {
			ptr += 2
			moveUpTheRear = false
		} else {
			ptr += 1
		}
		leadPtr += 1
		previousOrder = newOrder
	}
	return true
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
