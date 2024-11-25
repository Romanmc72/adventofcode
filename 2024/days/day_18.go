package days

import (
	_ "embed"
	"fmt"

	"github.com/Romanmc72/adventofcode/2024/util"
)

//go:embed data/18/input.txt
var real18Data []byte
//go:embed data/18/input.txt
var example18Data []byte

func Solve18(part int, example bool) error {
  logger := util.GetLogger()
	var data string
  if example {
    data = string(example18Data)
  } else {
    data = string(real18Data)
  }
  logger.Debug(data)
  if (part < 1 || part == 1) {
    fmt.Println("Day 18 Part 1 Solution: _____")
  }
  if (part < 1 || part == 2) {
    fmt.Println("Day 18 Part 2 Solution: _____")
  }
  return nil
}
