package days

import (
	_ "embed"
	"fmt"

	"github.com/Romanmc72/adventofcode/2024/util"
)

//go:embed data/17/input.txt
var real17Data []byte

//go:embed data/17/example.txt
var example17Data []byte

func Solve17(part int, example bool) error {
	logger := util.GetLogger()
	var data string
	if example {
		data = string(example17Data)
	} else {
		data = string(real17Data)
	}
	logger.Debug(data)
	if part < 1 || part == 1 {
		fmt.Println("Day 17 Part 1 Solution: _____")
	}
	if part < 1 || part == 2 {
		fmt.Println("Day 17 Part 2 Solution: _____")
	}
	return nil
}
