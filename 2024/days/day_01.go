package days

import (
	_ "embed"
	"fmt"
	"sort"
	"strconv"
	"strings"
)

//go:embed data/01/input.txt
var real01Data []byte

//go:embed data/01/example.txt
var example01Data []byte

func Solve01(part int, example bool) error {
	var data string
	if example {
		data = string(example01Data)
	} else {
		data = string(real01Data)
	}

	lines := strings.Split(data, "\n")
	leftList := make([]int, len(lines))
	rightList := make([]int, len(lines))
	numberMapping := make(map[int]int)

	for index, line := range lines {
		left, right, err := parseStringToInt(line)
		if err != nil {
			return err
		}
		leftList[index] = left
		rightList[index] = right
		rightP, ok := numberMapping[right]
		if !ok {
			numberMapping[right] = 1
		} else {
			numberMapping[right] = rightP + 1
		}
	}

	if part < 1 || part == 1 {
		part1(leftList, rightList)
	}
	if part < 1 || part == 2 {
		part2(leftList, numberMapping)
	}
	return nil
}

func part1(leftList []int, rightList []int) {
	sort.Ints(leftList)
	sort.Ints(rightList)
	totalDiff := 0
	for index, leftItem := range leftList {
		rightItem := rightList[index]
		diff := leftItem - rightItem
		if diff < 0 {
			diff = -diff
		}
		totalDiff += diff
	}
	fmt.Println("Day 01 Part 2 Solution:")
	fmt.Println(totalDiff)
}

func part2(leftList []int, numberMapping map[int]int) {
	totalValue := 0
	for _, leftVal := range leftList {
		p := numberMapping[leftVal]
		totalValue += leftVal * p
	}
	fmt.Println("Day 01 Part 2 Solution:")
	fmt.Println(totalValue)
}

// Parse a line of string and receive a pair of integers or an error if the
// integers were not parsable from the string
func parseStringToInt(line string) (int, int, error) {
	splits := strings.Split(line, "   ")
	
	left, err := strconv.Atoi(splits[0])
	if err != nil {
		return 0, 0, err
	}
	right, err := strconv.Atoi(splits[1])
	if err != nil {
		return 0, 0, err
	}
	return left, right, nil
}
