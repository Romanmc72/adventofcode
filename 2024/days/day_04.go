package days

import (
	_ "embed"
	"fmt"
	"strings"

	"github.com/Romanmc72/adventofcode/2024/util"
)

//go:embed data/04/input.txt
var real04Data []byte

//go:embed data/04/example.txt
var example04Data []byte

func Solve04(part int, example bool) error {
	logger := util.GetLogger()
	var data string
	if example {
		data = string(example04Data)
	} else {
		data = string(real04Data)
	}
	logger.Debug(data)
	matrix := RuneMatrix{
		Matrix: strings.Split(data, "\n"),
	}

	finds := 0
	xMASFinds := 0
	for rowNum, row := range matrix.Matrix {
		for columnNum, character := range row {
			if character == 'X' {
				finds += matrix.vivaMas(columnNum, rowNum)
			}
			if character == 'A' {
				if matrix.assMM(columnNum, rowNum) { xMASFinds++ }
			}
		}
	}
	if part < 1 || part == 1 {
		fmt.Println("Day 04 Part 1 Solution: ", finds)
	}
	if part < 1 || part == 2 {
		fmt.Println("Day 04 Part 2 Solution: ", xMASFinds)
	}
	return nil
}

type RuneMatrix struct {
	Matrix []string
}

func (rm *RuneMatrix) mas(x int, y int, xmod int, ymod int) bool {
	if rm.checkCharAtDirection(x, y, xmod, ymod, 'M') {
		if rm.checkCharAtDirection(x, y, xmod * 2, ymod * 2, 'A') {
			return rm.checkCharAtDirection(x, y, xmod * 3, ymod * 3, 'S')
		}
	}
	return false
}

func (rm *RuneMatrix) checkCharAtDirection(x int, y int, xmod int, ymod int, char byte) bool {
	return rm.Matrix[y + ymod][x + xmod] == char
}

// Also because we are looking for "MAS" since we already found the "X" at this point
// #TacoBell
func (rm *RuneMatrix) vivaMas(x int, y int) int {
	total := 0
	up := rm.canGoUp(y)
	down := rm.canGoDown(y)
	left := rm.canGoLeft(x)
	right := rm.canGoRight(x)
	if up {
		if rm.mas(x, y, 0, -1) { total++ }
	}
	if up && left {
		if rm.mas(x, y, -1, -1) { total++ }
	}
	if up && right {
		if rm.mas(x, y, 1, -1) { total++ }
	}
	if down && left {
		if rm.mas(x, y, -1, 1) { total++ }
	}
	if down {
		if rm.mas(x, y, 0, 1) { total++ }
	}
	if down && right {
		if rm.mas(x, y, 1, 1) { total++ }
	}
	if left {
		if rm.mas(x, y, -1, 0) { total++ }
	}
	if right {
		if rm.mas(x, y, 1, 0) { total++ }
	}
	return total
}

func (rm *RuneMatrix) canGoUp(y int) bool {
	return y >= 3
}

func (rm *RuneMatrix) canGoDown(y int) bool {
	return y <= (len(rm.Matrix) - 4)
}

func (rm *RuneMatrix) canGoLeft(x int) bool {
	return x >= 3
}

func (rm *RuneMatrix) canGoRight(x int) bool {
	return x <= (len(rm.Matrix[0]) - 4)
}

// cuz this lil elf is an ass and I hate him
// but it checks for the MM then the "SS" after if the
// "MM" is found since we already have "A"
func (rm *RuneMatrix) assMM(x int, y int) bool {
	if x == 0 || x == (len(rm.Matrix[0]) - 1) || y == 0 || y == (len(rm.Matrix) - 1) { return false }
	xmod, ymod, ok := rm.hasMM(x, y)
	if ok {
		return rm.hasSS(x, y, -1 * xmod, -1 * ymod)
	}
	return ok
}

func (rm *RuneMatrix) hasMM(x int, y int) (int, int, bool) {
	// left
	if rm.checkCharAtDirection(x, y, -1, 1, 'M') && rm.checkCharAtDirection(x, y, -1, -1, 'M') {
		return -1, 0, true
	}
	// right
	if rm.checkCharAtDirection(x, y, 1, 1, 'M') && rm.checkCharAtDirection(x, y, 1, -1, 'M') {
		return 1, 0, true
	}
	// up
	if rm.checkCharAtDirection(x, y, -1, -1, 'M') && rm.checkCharAtDirection(x, y, 1, -1, 'M') {
		return 0, -1, true
	}
	// down
	if rm.checkCharAtDirection(x, y, -1, 1, 'M') && rm.checkCharAtDirection(x, y, 1, 1, 'M') {
		return 0, 1, true
	}
	return 0, 0, false
}

func (rm *RuneMatrix) hasSS(x int, y int, xmod int, ymod int) bool {
	if xmod == 0 {
		return rm.checkCharAtDirection(x, y, -1, ymod, 'S') && rm.checkCharAtDirection(x, y, 1, ymod, 'S')
	}
	return rm.checkCharAtDirection(x, y, xmod, -1, 'S') && rm.checkCharAtDirection(x, y, xmod, 1, 'S')
}
