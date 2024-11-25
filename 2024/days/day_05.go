package days

import (
	_ "embed"
	"fmt"

	"github.com/Romanmc72/adventofcode/2024/util"
)

//go:embed data/05/input.txt
var real05Data []byte
//go:embed data/05/input.txt
var example05Data []byte

func Solve05(part int, example bool) error {
  logger := util.GetLogger()
	var data string
  if example {
    data = string(example05Data)
  } else {
    data = string(real05Data)
  }
  logger.Debug(data)
  if (part < 1 || part == 1) {
    fmt.Println("Day 05 Part 1 Solution: _____")
  }
  if (part < 1 || part == 2) {
    fmt.Println("Day 05 Part 2 Solution: _____")
  }
  return nil
}

