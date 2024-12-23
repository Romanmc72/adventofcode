package days

import (
	_ "embed"
	"fmt"

	"github.com/Romanmc72/adventofcode/2024/day9"
)

//go:embed data/09/input.txt
var real09Data []byte

//go:embed data/09/example.txt
var example09Data []byte

func Solve09(part int, example bool) error {
	var data string
	if example {
		data = string(example09Data)
	} else {
		data = string(real09Data)
	}
	fileSystem, err := day9.NewFileSystemFromData(data)
	if err != nil { return err }
	if part < 1 || part == 1 {
		fileSystem.Compact()
		checksum := fileSystem.Checksum()
		fmt.Println("Day 09 Part 1 Solution:", checksum)
	}
	if part < 1 || part == 2 {
		fmt.Printf("Files Pre\n%s\n", fileSystem.FileString())
		fileSystem.Defrag()
		fmt.Printf("Files Post\n%s\n", fileSystem.FileString())
		checksum := fileSystem.ChecksumFiles()
		fmt.Println("Day 09 Part 2 Solution:", checksum)
	}
	return nil
}
