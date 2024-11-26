package days

import (
	_ "embed"
	"fmt"

	"github.com/Romanmc72/adventofcode/2024/util"
)

//go:embed data/03/input.txt
var real03Data []byte

//go:embed data/03/example.txt
var example03Data []byte

func Solve03(part int, example bool) error {
	logger := util.GetLogger()
	var data string
	if example {
		data = string(example03Data)
	} else {
		data = string(real03Data)
	}
	logger.Debug(data)
	if part < 1 || part == 1 {
		fmt.Println("Day 03 Part 1 Solution: _____")
	}
	if part < 1 || part == 2 {
		fmt.Println("Day 03 Part 2 Solution: _____")
	}
	return nil
}
