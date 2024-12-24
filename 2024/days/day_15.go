package days

import (
	_ "embed"
	"fmt"
)

//go:embed data/15/input.txt
var real15Data []byte

//go:embed data/15/example.txt
var example15Data []byte

func Solve15(part int, example bool) error {
	var data string
	if example {
		data = string(example15Data)
	} else {
		data = string(real15Data)
	}
	logger.Debug(data)
	if part < 1 || part == 1 {
		fmt.Println("Day 15 Part 1 Solution: _____")
	}
	if part < 1 || part == 2 {
		fmt.Println("Day 15 Part 2 Solution: _____")
	}
	return nil
}
