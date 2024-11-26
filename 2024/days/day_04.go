package days

import (
	_ "embed"
	"fmt"

	"github.com/Romanmc72/adventofcode/2024/util"
)

//go:embed data/04/input.txt
var real04Data []byte

//go:embed data/04/example.txt
var example04Data []byte

func Solve04(part int, example bool) error {
	logger := util.GetLogger()
	var data string
	if example {
		data = string(example04Data)
	} else {
		data = string(real04Data)
	}
	logger.Debug(data)
	if part < 1 || part == 1 {
		fmt.Println("Day 04 Part 1 Solution: _____")
	}
	if part < 1 || part == 2 {
		fmt.Println("Day 04 Part 2 Solution: _____")
	}
	return nil
}
