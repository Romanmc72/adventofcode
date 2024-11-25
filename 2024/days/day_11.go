package days

import (
	_ "embed"
	"fmt"

	"github.com/Romanmc72/adventofcode/2024/util"
)

//go:embed data/11/input.txt
var real11Data []byte
//go:embed data/11/example.txt
var example11Data []byte

func Solve11(part int, example bool) error {
  logger := util.GetLogger()
	var data string
  if example {
    data = string(example11Data)
  } else {
    data = string(real11Data)
  }
  logger.Debug(data)
  if (part < 1 || part == 1) {
    fmt.Println("Day 11 Part 1 Solution: _____")
  }
  if (part < 1 || part == 2) {
    fmt.Println("Day 11 Part 2 Solution: _____")
  }
  return nil
}
