package days

import (
	_ "embed"
	"fmt"
)

//go:embed data/20/input.txt
var real20Data []byte

//go:embed data/20/example.txt
var example20Data []byte

func Solve20(part int, example bool) error {
	var data string
	if example {
		data = string(example20Data)
	} else {
		data = string(real20Data)
	}
	logger.Debug(data)
	if part < 1 || part == 1 {
		fmt.Println("Day 20 Part 1 Solution: _____")
	}
	if part < 1 || part == 2 {
		fmt.Println("Day 20 Part 2 Solution: _____")
	}
	return nil
}
