package days

import (
	_ "embed"
	"fmt"

	"github.com/Romanmc72/adventofcode/2024/util"
)

//go:embed data/12/input.txt
var real12Data []byte

//go:embed data/12/example.txt
var example12Data []byte

func Solve12(part int, example bool) error {
	logger := util.GetLogger()
	var data string
	if example {
		data = string(example12Data)
	} else {
		data = string(real12Data)
	}
	logger.Debug(data)
	if part < 1 || part == 1 {
		fmt.Println("Day 12 Part 1 Solution: _____")
	}
	if part < 1 || part == 2 {
		fmt.Println("Day 12 Part 2 Solution: _____")
	}
	return nil
}
