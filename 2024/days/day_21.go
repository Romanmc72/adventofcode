package days

import (
	_ "embed"
	"fmt"

	"github.com/Romanmc72/adventofcode/2024/util"
)

//go:embed data/21/input.txt
var real21Data []byte
//go:embed data/21/example.txt
var example21Data []byte

func Solve21(part int, example bool) error {
  logger := util.GetLogger()
	var data string
  if example {
    data = string(example21Data)
  } else {
    data = string(real21Data)
  }
  logger.Debug(data)
  if (part < 1 || part == 1) {
    fmt.Println("Day 21 Part 1 Solution: _____")
  }
  if (part < 1 || part == 2) {
    fmt.Println("Day 21 Part 2 Solution: _____")
  }
  return nil
}
