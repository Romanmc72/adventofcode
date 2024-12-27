package days

import (
	_ "embed"
	"fmt"
	"strconv"
	"strings"
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
	sl.Blink(25)
	if part < 1 || part == 1 {
		fmt.Println("Day 11 Part 1 Solution:", sl.Count())
	}
	sl.Blink(50)
	if part < 1 || part == 2 {
		fmt.Println("Day 11 Part 2 Solution:", sl.Count())
	}
	return nil
}

// TODO: Make a graph connecting a "stone" to all of its children and use that
// to register and move stones around in a cycle instead of recalculating the
// same numbers every time. Basically only calculate if you need to otherwise
// split off of the existing graph and increment things along the way. The
// graph will need to be "copied" every time and iterated on to where the
// numbers get zeroed out on the copy and added to as the original is
// iterated.
//
// Literally, just use a map and do this inline. make the stone emit numbers, not stones.
type StoneLine map[Stone]int

func (sl *StoneLine) String() string {
	sls := []string{}
	for s := range *sl {
		sls = append(sls, s.String())
	}
	return fmt.Sprintf("{[%s]}", strings.Join(sls, ", "))
}

func NewStoneLine(data string) (sl StoneLine, err error) {
	nums, err := parseLineToListOfInts(data, " ")
	if err != nil {
		return sl, err
	}
	sl = StoneLine{}
	for _, n := range nums {
		s := NewStone(n)
		if c, ok := sl[*s]; ok {
			sl[*s] = c + 1
		} else {
			sl[*s] = 1
		}
	}
	return sl, err
}

func (sl *StoneLine) Blink(times int) {
	for i := 0; i < times; i++ {
		sl.blinkOnce()
	}
}

func (sl *StoneLine) Count() int {
	total := 0
	for _, c := range *sl {
		total += c
	}
	return total
}

func (sl *StoneLine) SetInStone(branch Stone, count int) {
	if c, ok := (*sl)[branch]; ok {
		(*sl)[branch] = c + count
	} else {
		(*sl)[branch] = count
	}
}

func (sl *StoneLine) blinkOnce() {
	newStones := make(StoneLine)
	for stone, c := range *sl {
		// shmoke wheat #Stoner
		stoneL, stoneR := stone.Mutate()
		if stoneR != nil {
			newStones.SetInStone(*stoneR, c)
		}
		newStones.SetInStone(*stoneL, c)
	}
	*sl = newStones
}

// eventually everything will be multiples out of 2024, which we can model and pre-compute
// the per-blink number of stones created up until the pattern repeats. The shite part here
// is that we iterate 75 times and each time we potentially (though not actually) double the
// number of stones. This means our algorithm is 2^N which if we do it 75 times will exhaust
// the 64-bit integer space available to us through golang just by counting the stones
// (forget the numbers on the stones themselves). This is bad news. I am guessing it might
// go almost right up to that number (without passing) because not every operation doubles
// the number of stones.
//
// Wondering now if we can get the junctures at which when multiplied, 2024 yields an even number of digits...
//
// One thing that I am assuming here as well is that every number at some point will EVENTUALLY decompose all
// digits to become 0, just the question is when/how long will that take for each, or is that even true?
// Better yet, does it matter?...
// ...
// Have not been able to discern a pattern yet (not that there isn't one) but I do know that
// Found that the patterns do repeat after about 80 iterations and there forms a cyclic
// graph between all numbers. I will next construct that graph and then use that to count
// up the splitting and iterating without blowing up the number of nodes that need to be checked.
type Stone struct {
	value         int
	splitsToLeft  *Stone
	splitsToRight *Stone
}

func NewStone(n int) *Stone {
	return &Stone{value: n}
}

func (s Stone) String() string {
	return strconv.Itoa(s.value)
}

func (s *Stone) Mutate() (*Stone, *Stone) {
	if s.splitsToLeft != nil {
		return s.splitsToLeft, s.splitsToRight
	}
	if s.value == 0 {
		s.splitsToLeft = NewStone(1)
		return s.splitsToLeft, nil
	}
	valueString := s.String()
	if len(valueString)%2 == 0 {
		leftHalf, _ := strconv.Atoi(valueString[:len(valueString)/2])
		s.splitsToLeft = NewStone(leftHalf)
		rightHalf, _ := strconv.Atoi(valueString[len(valueString)/2:])
		s.splitsToRight = NewStone(rightHalf)
		return s.splitsToLeft, s.splitsToRight
	}
	s.splitsToLeft = NewStone(s.value * 2024)
	return s.splitsToLeft, nil
}
