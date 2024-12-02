package days

import (
	_ "embed"
	"fmt"
	"sort"
	"strconv"
	"strings"

	"github.com/Romanmc72/adventofcode/2024/util"
)

//go:embed data/01/input.txt
var real01Data []byte

//go:embed data/01/example.txt
var example01Data []byte

func Solve01(part int, example bool) error {
	logger := util.GetLogger()
	var data string
	if example {
		data = string(example01Data)
	} else {
		data = string(real01Data)
	}
	logger.Debug(data)

	if part < 1 || part == 1 {
		lines := strings.Split(data, "\n")
		leftList := make([]int, len(lines))
		rightList := make([]int, len(lines))
		for index, line := range lines {
			left, right, err := parse(line)
			if err != nil {
				return err
			}
			leftList[index] = left
			rightList[index] = right
		}
		sort.Slice(leftList, func(i, j int) bool {
			return leftList[i] < leftList[j]
		})
		sort.Slice(rightList, func(i, j int) bool {
			return rightList[i] < rightList[j]
		})
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

	if part < 1 || part == 2 {
		numberMapping := make(map[int]int)
		lines := strings.Split(data, "\n")
		leftList := make([]int, len(lines))
		for index, line := range lines {
			left, right, err := parse(line)
			leftList[index] = left
			logger.Debug("what the H?", "left", left, "right", right)
			if err != nil {
				return err
			}
			rightP, ok := numberMapping[right]
			if !ok {
				numberMapping[right] = 1
			} else {
				numberMapping[right] = rightP + 1
			}
		}
		fmt.Printf("%v", numberMapping)
		totalValue := 0
		for _, leftVal := range leftList {
			p := numberMapping[leftVal]
			totalValue += leftVal * p
		}
		fmt.Println("Day 01 Part 2 Solution:")
		fmt.Println(totalValue)
	}
	return nil
}

func parse(line string) (int, int, error) {
	splits := strings.Split(line, "   ")
	
	left, err := strconv.Atoi(splits[0])
	if err != nil {
		return 0, 0, err
	}
	right, err := strconv.Atoi(splits[1])
	if err != nil {
		return 0, 0, nil
	}
	return left, right, nil
}
