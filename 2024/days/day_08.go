package days

import (
	_ "embed"
	"fmt"

	"github.com/Romanmc72/adventofcode/2024/util"
)

//go:embed data/08/input.txt
var real08Data []byte

//go:embed data/08/example.txt
var example08Data []byte

func Solve08(part int, example bool) error {
	logger := util.GetLogger()
	var data string
	if example {
		data = string(example08Data)
	} else {
		data = string(real08Data)
	}
	logger.Debug(data)
	if part < 1 || part == 1 {
		fmt.Println("Day 08 Part 1 Solution: _____")
	}
	if part < 1 || part == 2 {
		fmt.Println("Day 08 Part 2 Solution: _____")
	}
	return nil
}
