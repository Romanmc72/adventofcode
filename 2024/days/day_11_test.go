package days

import (
	"testing"
)

func TestDay11Stone(t *testing.T) {
	st := NewStone(0)
	s1, s2 := st.Mutate()
	if s1.value != 1 {
		t.Errorf("Wanted=1 but got=%d", s1.value)
	}
	if s2 != nil {
		t.Errorf("Wanted= nil but got= %s", s2)
	}
	s1, s2 = s1.Mutate()
	if s1.value != 2024 {
		t.Errorf("Wanted=2024 but got=%d", s1.value)
	}
	if s2 != nil {
		t.Errorf("Wanted= nil but got= %s", s2)
	}
	s1, s2 = s1.Mutate()
	if s1.value != 20 {
		t.Errorf("Wanted=20 but got=%d", s1.value)
	}
	if s2.value != 24 {
		t.Errorf("Wanted= 24 but got= %s", s2)
	}
	s3, s4 := s1.Mutate()
	s5, s6 := s2.Mutate()
	if s3.value != 2 || s4.value != 0 || s5.value != 2 || s6.value != 4 {
		t.Errorf("Wanted 2, 0, 2, 4 but got %s, %s, %s, %s", s3, s4, s5, s6)
	}
}

func TestUniqueNumbers(t *testing.T) {
	input := "572556 22 0 528 4679021 1 10725 2790"
	nums := map[int]bool{}
	sl, err := NewStoneLine(input)
	if err != nil {
		t.Errorf("Wanted err=nil but got err=%s", err)
	}
	hasNewNumbers := true
	i := 0
	for hasNewNumbers || i < 41 {
		newNums := 0
		for s := range sl {
			_, ok := nums[s.value]
			if !ok {
				nums[s.value] = true
				newNums++
			}
		}
		sl.Blink(1)
		if newNums == 0 {
			return
		}
		i++
	}
	t.Errorf("Starting with %s and going for %d iterations, was unable to find a cycle", input, i)
}

func TestDay11Part1And2(t *testing.T) {
	input := "125 17"
	sl, err := NewStoneLine(input)
	if err != nil {
		t.Errorf("NewStoneLine()\nWanted err=nil but got err=%s", err)
	}
	sl.Blink(25)
	want := 55312
	got := sl.Count()
	if want != got {
		t.Errorf("StoneLine.Blink(25) + StoneLine.Count()\nWanted=%d but got=%d", want, got)
	}
	sl.Blink(50)
	want = 65601038650482
	got = sl.Count()
	if want != got {
		t.Errorf("StoneLine.Blink(75) + StoneLine.Count()\nWanted more than %d but got=%d", want, got)
	}
}
