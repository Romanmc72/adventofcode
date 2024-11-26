package days

import (
	_ "embed"
	"fmt"

	"github.com/Romanmc72/adventofcode/2024/util"
)

//go:embed data/16/input.txt
var real16Data []byte

//go:embed data/16/example.txt
var example16Data []byte

func Solve16(part int, example bool) error {
	logger := util.GetLogger()
	var data string
	if example {
		data = string(example16Data)
	} else {
		data = string(real16Data)
	}
	logger.Debug(data)
	if part < 1 || part == 1 {
		fmt.Println("Day 16 Part 1 Solution: _____")
	}
	if part < 1 || part == 2 {
		fmt.Println("Day 16 Part 2 Solution: _____")
	}
	return nil
}
