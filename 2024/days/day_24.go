package days

import (
	_ "embed"
	"fmt"

	"github.com/Romanmc72/adventofcode/2024/util"
)

//go:embed data/24/input.txt
var real24Data []byte
//go:embed data/24/input.txt
var example24Data []byte

func Solve24(part int, example bool) error {
  logger := util.GetLogger()
	var data string
  if example {
    data = string(example24Data)
  } else {
    data = string(real24Data)
  }
  logger.Debug(data)
  if (part < 1 || part == 1) {
    fmt.Println("Day 24 Part 1 Solution: _____")
  }
  if (part < 1 || part == 2) {
    fmt.Println("Day 24 Part 2 Solution: _____")
  }
  return nil
}

