package days

import (
	_ "embed"
	"fmt"

	"github.com/Romanmc72/adventofcode/2024/util"
)

//go:embed data/09/input.txt
var real09Data []byte

//go:embed data/09/example.txt
var example09Data []byte

func Solve09(part int, example bool) error {
	logger := util.GetLogger()
	var data string
	if example {
		data = string(example09Data)
	} else {
		data = string(real09Data)
	}
	logger.Debug(data)
	if part < 1 || part == 1 {
		fmt.Println("Day 09 Part 1 Solution: _____")
	}
	if part < 1 || part == 2 {
		fmt.Println("Day 09 Part 2 Solution: _____")
	}
	return nil
}
