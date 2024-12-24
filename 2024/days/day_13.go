package days

import (
	_ "embed"
	"fmt"
)

//go:embed data/13/input.txt
var real13Data []byte

//go:embed data/13/example.txt
var example13Data []byte

func Solve13(part int, example bool) error {
	var data string
	if example {
		data = string(example13Data)
	} else {
		data = string(real13Data)
	}
	logger.Debug(data)
	if part < 1 || part == 1 {
		fmt.Println("Day 13 Part 1 Solution: _____")
	}
	if part < 1 || part == 2 {
		fmt.Println("Day 13 Part 2 Solution: _____")
	}
	return nil
}
