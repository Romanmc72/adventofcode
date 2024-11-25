package days

import (
	_ "embed"
	"fmt"

	"github.com/Romanmc72/adventofcode/2024/util"
)

//go:embed data/10/input.txt
var real10Data []byte
//go:embed data/10/input.txt
var example10Data []byte

func Solve10(part int, example bool) error {
  logger := util.GetLogger()
	var data string
  if example {
    data = string(example10Data)
  } else {
    data = string(real10Data)
  }
  logger.Debug(data)
  if (part < 1 || part == 1) {
    fmt.Println("Day 10 Part 1 Solution: _____")
  }
  if (part < 1 || part == 2) {
    fmt.Println("Day 10 Part 2 Solution: _____")
  }
  return nil
}

