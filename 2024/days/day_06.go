package days

import (
	_ "embed"
	"fmt"

	"github.com/Romanmc72/adventofcode/2024/util"
)

//go:embed data/06/input.txt
var real06Data []byte
//go:embed data/06/input.txt
var example06Data []byte

func Solve06(part int, example bool) error {
  logger := util.GetLogger()
	var data string
  if example {
    data = string(example06Data)
  } else {
    data = string(real06Data)
  }
  logger.Debug(data)
  if (part < 1 || part == 1) {
    fmt.Println("Day 06 Part 1 Solution: _____")
  }
  if (part < 1 || part == 2) {
    fmt.Println("Day 06 Part 2 Solution: _____")
  }
  return nil
}

