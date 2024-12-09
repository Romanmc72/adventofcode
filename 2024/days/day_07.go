package days

import (
	_ "embed"
	"fmt"
	"math"
	"strconv"
	"strings"
)

//go:embed data/07/input.txt
var real07Data []byte

//go:embed data/07/example.txt
var example07Data []byte

type Equation struct {
	Total int
	Numbers []int
}

type Operator func(int, int) int

func Add(x int, y int) int { return x + y }

func Multiply(x int, y int) int { return x * y }

func Concat(x int, y int) int { return x * int(math.Pow(10.0, float64(len(strconv.Itoa(y))))) + y }

var operatorLookup = map[rune]Operator{
	'0': Add,
	'1': Multiply,
	'2': Concat,
}

// Because this is an either/or scenario we can leverage base 2 or 3 to represent
// all possible operator combinations as strings
func MakePermutations(operands int, part int) [][]Operator {
	ops := operands - 1
	base := 2
	if part == 2 || part < 1 {
		base = 3
	}
	permutations := int(math.Pow(float64(base), float64(ops)))
	operators := make([][]Operator, permutations)
	for i := 0; i < permutations; i++ {
		o := make([]Operator, ops)
		asBinary := leftPad(strconv.FormatInt(int64(i), base), ops, '0')
		for pos, char := range asBinary {
			o[pos] = operatorLookup[char]
		}
		operators[i] = o
	}
	return operators
}

func leftPad(original string, length int, pad rune) string {
	padding := length - len(original)
	if padding <= 0 { return original }
	return strings.Join([]string{strings.Repeat(string(pad), padding), original}, "")
}

func (e Equation) IsCalibrated(part int) bool {
	operands := len(e.Numbers)
	allOperations := MakePermutations(operands, part)
	forEachOperation:
		for _, op := range allOperations {
			total := e.Numbers[0]
			for n := 1; n < len(e.Numbers); n++ {
				y := e.Numbers[n]
				total = op[n - 1](total, y)
				if total > e.Total {
					continue forEachOperation
				}
			}
			if total == e.Total { return true }
		}
	return false
}

func Solve07(part int, example bool) error {
	var data string
	if example {
		data = string(example07Data)
	} else {
		data = string(real07Data)
	}
	lines := strings.Split(data, "\n")
	part1Total := 0
	part2Total := 0
	for _, line := range lines {
		eq, err := parseEquation(line)
		if err != nil {
			return err
		}
		if eq.IsCalibrated(1) {
			part1Total += eq.Total
		}
		if eq.IsCalibrated(2) {
			part2Total += eq.Total
		}
	}
	if part < 1 || part == 1 {
		fmt.Println("Day 07 Part 1 Solution:", part1Total)
	}
	if part < 1 || part == 2 {
		fmt.Println("Day 07 Part 2 Solution:", part2Total)
	}
	return nil
}


func parseEquation(data string) (e Equation, err error) {
	halves := strings.Split(data, ": ")
	total, err := strconv.Atoi(halves[0])
	if err != nil {
		return e, err
	}
	numStrings := strings.Split(halves[1], " ")
	nums := make([]int, len(numStrings))
	for i, ns := range numStrings {
		num, err := strconv.Atoi(ns)
		if err != nil {
			return e, err
		}
		nums[i] = num
	}
	e.Numbers = nums
	e.Total = total
	return e, nil
}
