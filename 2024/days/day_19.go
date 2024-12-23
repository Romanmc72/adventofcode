package days

import (
	_ "embed"
	"fmt"
)

//go:embed data/19/input.txt
var real19Data []byte

//go:embed data/19/example.txt
var example19Data []byte

func Solve19(part int, example bool) error {
	var data string
	if example {
		data = string(example19Data)
	} else {
		data = string(real19Data)
	}
	logger.Debug(data)
	if part < 1 || part == 1 {
		fmt.Println("Day 19 Part 1 Solution: _____")
	}
	if part < 1 || part == 2 {
		fmt.Println("Day 19 Part 2 Solution: _____")
	}
	return nil
}
