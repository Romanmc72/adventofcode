package days

import (
	_ "embed"
	"fmt"

	"github.com/Romanmc72/adventofcode/2024/util"
)

//go:embed data/02/input.txt
var real02Data []byte

//go:embed data/02/example.txt
var example02Data []byte

func Solve02(part int, example bool) error {
	logger := util.GetLogger()
	var data string
	if example {
		data = string(example02Data)
	} else {
		data = string(real02Data)
	}
	logger.Debug(data)
	if part < 1 || part == 1 {
		fmt.Println("Day 02 Part 1 Solution: _____")
	}
	if part < 1 || part == 2 {
		fmt.Println("Day 02 Part 2 Solution: _____")
	}
	return nil
}
