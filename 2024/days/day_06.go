package days

import (
	_ "embed"
	"fmt"

	"github.com/Romanmc72/adventofcode/2024/day6"
)

//go:embed data/06/input.txt
var real06Data []byte

//go:embed data/06/example.txt
var example06Data []byte

func Solve06(part int, example bool) error {
	var data string
	if example {
		data = string(example06Data)
	} else {
		data = string(real06Data)
	}
	matrix := day6.NewMatrixFromData(data)
	if part < 1 || part == 1 {
		err := matrix.Walk()
		if err != nil {
			logger.Error("lol it broke!", "error", err)
		}
		fmt.Println("Day 06 Part 1 Solution:", matrix.CountVisitedSpots())
	}
	if part < 1 || part == 2 {
		matrix.FindBlockableSpots()
		fmt.Println("Day 06 Part 2 Solution:", matrix.CountBlockableSpots())
		fmt.Println(matrix)
	}
	return nil
}
