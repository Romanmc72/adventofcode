package days

import (
	_ "embed"
	"fmt"
)

//go:embed data/25/input.txt
var real25Data []byte

//go:embed data/25/example.txt
var example25Data []byte

func Solve25(part int, example bool) error {
	var data string
	if example {
		data = string(example25Data)
	} else {
		data = string(real25Data)
	}
	logger.Debug(data)
	if part < 1 || part == 1 {
		fmt.Println("Day 25 Part 1 Solution: _____")
	}
	if part < 1 || part == 2 {
		fmt.Println("Day 25 Part 2 Solution: _____")
	}
	return nil
}
