package days

import (
	_ "embed"
	"fmt"

	"github.com/Romanmc72/adventofcode/2024/util"
)

//go:embed data/22/input.txt
var real22Data []byte

//go:embed data/22/example.txt
var example22Data []byte

func Solve22(part int, example bool) error {
	logger := util.GetLogger()
	var data string
	if example {
		data = string(example22Data)
	} else {
		data = string(real22Data)
	}
	logger.Debug(data)
	if part < 1 || part == 1 {
		fmt.Println("Day 22 Part 1 Solution: _____")
	}
	if part < 1 || part == 2 {
		fmt.Println("Day 22 Part 2 Solution: _____")
	}
	return nil
}
