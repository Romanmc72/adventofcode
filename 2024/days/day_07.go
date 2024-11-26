package days

import (
	_ "embed"
	"fmt"

	"github.com/Romanmc72/adventofcode/2024/util"
)

//go:embed data/07/input.txt
var real07Data []byte

//go:embed data/07/example.txt
var example07Data []byte

func Solve07(part int, example bool) error {
	logger := util.GetLogger()
	var data string
	if example {
		data = string(example07Data)
	} else {
		data = string(real07Data)
	}
	logger.Debug(data)
	if part < 1 || part == 1 {
		fmt.Println("Day 07 Part 1 Solution: _____")
	}
	if part < 1 || part == 2 {
		fmt.Println("Day 07 Part 2 Solution: _____")
	}
	return nil
}
