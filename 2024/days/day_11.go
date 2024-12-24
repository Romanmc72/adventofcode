package days

import (
	_ "embed"
	"fmt"
	"strconv"
)

//go:embed data/11/input.txt
var real11Data []byte

//go:embed data/11/example.txt
var example11Data []byte

func Solve11(part int, example bool) error {
	var data string
	if example {
		data = string(example11Data)
	} else {
		data = string(real11Data)
	}
	sl, err := NewStoneLine(data)
	if err != nil {
		return err
	}
	err = sl.Blink(25)
	if err != nil {
		return err
	}
	if part < 1 || part == 1 {
		fmt.Println("Day 11 Part 1 Solution:", sl.Count())
	}
	err = sl.Blink(50)
	if err != nil {
		return err
	}
	if part < 1 || part == 2 {
		fmt.Println("Day 11 Part 2 Solution:", sl.Count())
	}
	return nil
}

type StoneLine struct {
	stones []*Stone
}

func NewStoneLine(data string) (sl StoneLine, err error) {
	nums, err := parseLineToListOfInts(data, " ")
	if err != nil {
		return sl, err
	}
	sl.stones = make([]*Stone, len(nums))
	for i, n := range nums {
		sl.stones[i] = NewStone(n)
	}
	return sl, err
}

func (sl *StoneLine) Blink(times int) error {
	for i := 0; i < times; i++ {
		err := sl.blinkOnce()
		if err != nil {
			return err
		}
	}
	return nil
}

func (sl StoneLine) Count() int {
	return len(sl.stones)
}

func (sl *StoneLine) blinkOnce() error {
	newStones := []*Stone{}
	for _, s := range sl.stones {
		s1, s2, err := s.Mutate()
		if err != nil {
			return err
		}
		if s2 == nil {
			newStones = append(newStones, s1)
			continue
		}
		newStones = append(newStones, s1, s2)
	}
	sl.stones = newStones
	return nil
}

// eventually everything will be multiples out of 2024, which we can model and pre-compute the per-blink number of stones created up until the pattern repeats.
type Stone struct {
	value int
}

func NewStone(n int) *Stone {
	return &Stone{value: n}
}

func (s *Stone) Mutate() (*Stone, *Stone, error) {
	if s.value == 0 {
		s.value = 1
		return s, nil, nil
	}
	valueString := strconv.Itoa(s.value)
	if len(valueString)%2 == 0 {
		leftHalf, err := strconv.Atoi(valueString[:len(valueString)/2])
		if err != nil {
			return nil, nil, err
		}
		rightHalf, _ := strconv.Atoi(valueString[len(valueString)/2:])
		if err != nil {
			return nil, nil, err
		}
		s.value = leftHalf
		return s, &Stone{value: rightHalf}, nil
	}
	s.value = s.value * 2024
	return s, nil, nil
}
