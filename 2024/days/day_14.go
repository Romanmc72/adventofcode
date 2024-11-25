package days

import (
	_ "embed"
	"fmt"

	"github.com/Romanmc72/adventofcode/2024/util"
)

//go:embed data/14/input.txt
var real14Data []byte
//go:embed data/14/input.txt
var example14Data []byte

func Solve14(part int, example bool) error {
  logger := util.GetLogger()
	var data string
  if example {
    data = string(example14Data)
  } else {
    data = string(real14Data)
  }
  logger.Debug(data)
  if (part < 1 || part == 1) {
    fmt.Println("Day 14 Part 1 Solution: _____")
  }
  if (part < 1 || part == 2) {
    fmt.Println("Day 14 Part 2 Solution: _____")
  }
  return nil
}
