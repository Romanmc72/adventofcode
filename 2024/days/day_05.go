package days

import (
	_ "embed"
	"fmt"
	"strconv"
	"strings"
)

//go:embed data/05/input.txt
var real05Data []byte

//go:embed data/05/example.txt
var example05Data []byte

type SafetyManual struct {
	Pages []int
}

// need to navigate the remainder of the list
// to evaluate if every number is correctly ordered relative
// to its predecessors
// this will be n! but that is probably fine
// because these are small safety manuals
func (man *SafetyManual) isCorrectlyOrdered(rs RuleSet) bool {
	// if it is length 1, then there is nothing to do here
	if len(man.Pages) <= 1 {
		return true
	}
	for index, num := range man.Pages {
		remainingPages := man.Pages[index+1:]
		stillCorrect := rs.checkNumberAgainstRest(num, remainingPages)
		if !stillCorrect {
			return false
		}
	}
	return true
}

// check the number against the rest and if it is bad, swap it with
// the bad one and continue iterating without progressing the pointer
// (so as to get the newly swapped number also correctly sorted)
func (man *SafetyManual) correctPages(rs RuleSet) {
	leftPointer := 0
outerLoop:
	for leftPointer < len(man.Pages) {
		leftVal := man.Pages[leftPointer]
		for rightPointer := leftPointer + 1; rightPointer < len(man.Pages); rightPointer++ {
			rightVal := man.Pages[rightPointer]
			if !rs.areTwoNumbersOkay(leftVal, rightVal) {
				man.Pages[leftPointer], man.Pages[rightPointer] = man.Pages[rightPointer], man.Pages[leftPointer]
				continue outerLoop
			}
		}
		leftPointer++
	}
}

func (rs RuleSet) areTwoNumbersOkay(number int, followingNumber int) bool {
	rule, hasRule := rs[followingNumber]
	if hasRule {
		rules := *rule
		_, isBefore := rules[number]
		if isBefore {
			return false
		}
	}
	return true
}

func (rs RuleSet) checkNumberAgainstRest(number int, rest []int) bool {
	for _, followingNumber := range rest {
		if !rs.areTwoNumbersOkay(number, followingNumber) {
			return false
		}
	}
	return true
}

type RuleSet map[int]*map[int]bool

func Solve05(part int, example bool) error {
	var data string
	if example {
		data = string(example05Data)
	} else {
		data = string(real05Data)
	}
	ruleSet, safetyManuals, err := parseRuleSetAndSafetyManuals(data)
	if err != nil {
		return err
	}
	correctTotal := 0
	incorrectTotal := 0
	for _, man := range safetyManuals {
		if man.isCorrectlyOrdered(ruleSet) {
			correctTotal += man.Pages[len(man.Pages)/2]
		} else {
			man.correctPages(ruleSet)
			incorrectTotal += man.Pages[len(man.Pages)/2]
		}
	}
	if part < 1 || part == 1 {
		fmt.Println("Day 05 Part 1 Solution:", correctTotal)
	}
	if part < 1 || part == 2 {
		fmt.Println("Day 05 Part 2 Solution:", incorrectTotal)
	}
	return nil
}

func parseRuleSetAndSafetyManuals(data string) (rs RuleSet, mans []SafetyManual, err error) {
	halves := strings.Split(data, "\n\n")
	ruleSetString := halves[0]
	safetyManualString := halves[1]
	rs, err = parseRuleSet(ruleSetString)
	if err != nil {
		return rs, mans, err
	}
	mans, err = parseSafetyManuals(safetyManualString)
	return rs, mans, err
}

func parseRuleSet(ruleSetString string) (ruleSet RuleSet, err error) {
	ruleSet = map[int]*map[int]bool{}
	ruleStrings := strings.Split(ruleSetString, "\n")
	for _, ruleString := range ruleStrings {
		preAndPost := strings.Split(ruleString, "|")
		firstNumber, err := strconv.Atoi(preAndPost[0])
		if err != nil {
			return ruleSet, err
		}
		secondNumber, err := strconv.Atoi(preAndPost[1])
		if err != nil {
			return ruleSet, err
		}
		_, ok := ruleSet[firstNumber]
		if !ok {
			ruleSet[firstNumber] = &map[int]bool{}
		}
		innerMap := *ruleSet[firstNumber]
		innerMap[secondNumber] = true
	}
	return ruleSet, nil
}

func parseSafetyManuals(safetyManualString string) (mans []SafetyManual, err error) {
	manualStrings := strings.Split(safetyManualString, "\n")
	mans = make([]SafetyManual, len(manualStrings))
	for index, line := range manualStrings {
		pages, err := parseLineToListOfInts(line, ",")
		if err != nil {
			return mans, err
		}
		mans[index] = SafetyManual{Pages: pages}
	}
	return mans, nil
}
