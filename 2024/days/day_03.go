package days

import (
	_ "embed"
	"fmt"
	"regexp"
	"strconv"
	"strings"
)

//go:embed data/03/input.txt
var real03Data []byte

//go:embed data/03/example.txt
var example03Data []byte

func Solve03(part int, example bool) error {
	var data string
	if example {
		data = string(example03Data)
	} else {
		data = string(real03Data)
	}
	logger.Debug(data)
	if part < 1 || part == 1 {
		exp := regexp.MustCompile(`mul\(\d+,\d+\)`)
		found := exp.FindAllString(data, -1)
		total := 0
		for _, each := range found {
			val, err := parseMulExpression(each)
			if err != nil {
				return err
			}
			total += val
		}
		fmt.Println("Day 03 Part 1 Solution:", total)
	}
	if part < 1 || part == 2 {
		exp := regexp.MustCompile(`(mul\(\d+,\d+\)|do\(\)|don't\(\))`)
		found := exp.FindAllString(data, -1)
		total := 0
		do := true
		for _, each := range found {
			if isMul(each) {
				if do {
					val, err := parseMulExpression(each)
					if err != nil {
						return err
					}
					total += val
				}
			} else {
				do = parseDosAndDonts(each)
			}
		}
		fmt.Println("Day 03 Part 2 Solution:", total)
	}
	return nil
}

func parseDosAndDonts(s string) bool {
	return s == "do()"
}

func isMul(s string) bool {
	return s[0] == 'm'
}

func parseMulExpression(exp string) (int, error) {
	sides := strings.Split(exp, ",")
	left := sides[0]
	right := sides[1]
	leftSides := strings.Split(left, "(")
	rightSides := strings.Split(right, ")")
	leftNum, err := strconv.Atoi(leftSides[1])
	if err != nil {
		return 0, err
	}
	rightNum, err := strconv.Atoi(rightSides[0])
	if err != nil {
		return 0, err
	}
	return leftNum * rightNum, nil
}
