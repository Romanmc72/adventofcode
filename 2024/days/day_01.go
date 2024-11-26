package days

import (
	_ "embed"
	"fmt"

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
		fmt.Println("Day 01 Part 1 Solution: _____")
	}
	if part < 1 || part == 2 {
		fmt.Println("Day 01 Part 2 Solution: _____")
	}
	return nil
}
