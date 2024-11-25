package days

import (
	_ "embed"
	"fmt"

	"github.com/Romanmc72/adventofcode/2024/util"
)

//go:embed data/23/input.txt
var real23Data []byte
//go:embed data/23/example.txt
var example23Data []byte

func Solve23(part int, example bool) error {
  logger := util.GetLogger()
	var data string
  if example {
    data = string(example23Data)
  } else {
    data = string(real23Data)
  }
  logger.Debug(data)
  if (part < 1 || part == 1) {
    fmt.Println("Day 23 Part 1 Solution: _____")
  }
  if (part < 1 || part == 2) {
    fmt.Println("Day 23 Part 2 Solution: _____")
  }
  return nil
}
