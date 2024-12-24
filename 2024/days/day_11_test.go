package days

import "testing"

func TestDay11Stone(t *testing.T) {
	st := NewStone(0)
	s1, s2, err := st.Mutate()
	if s1.value != 1 {
		t.Errorf("Wanted=1 but got=%d", s1.value)
	}
	if s2 != nil || err != nil {
		t.Errorf("Wanted= nil, nil but got= %v, %s", s2, err)
	}
	s1, s2, err = st.Mutate()
	if s1.value != 2024 {
		t.Errorf("Wanted=2024 but got=%d", s1.value)
	}
	if s2 != nil || err != nil {
		t.Errorf("Wanted= nil, nil but got= %v, %s", s2, err)
	}
	s1, s2, err = st.Mutate()
	if s1.value != 20 {
		t.Errorf("Wanted=20 but got=%d", s1.value)
	}
	if s2.value != 24 || err != nil {
		t.Errorf("Wanted= 24, nil but got= %v, %s", s2, err)
	}
	s3, s4, err := s1.Mutate()
	s5, s6, err2 := s2.Mutate()
	if s3.value != 2 || s4.value != 0 || s5.value != 2 || s6.value != 4 || err != nil || err2 != nil {
		t.Errorf("Wanted 2, 0, 2, 4, nil, nil but got %v, %v, %v, %v, %s, %s", s3, s4, s5, s6, err, err2)
	}
}

func TestStoneLineBlink(t *testing.T) {
	sl, err := NewStoneLine("0")
	if err != nil {
		t.Error("Could not parse example stone line")
	}
	pattern := []int{1, 1, 2, 4, 4, 7, 14, 16, 20, 39, 62, 81, 110, 200, 328}
	//               0  0  1  2  0  3   7   2   4  19  23  19   29   90  128
	// see if at any point we get back to a 0 or a 1 on the leading stone,
	// this will tell us how long it takes that one to repeat
	for i := 0; i < len(pattern); i++ {
		want := pattern[i]
		err := sl.Blink(1)
		got := sl.Count()
		if err != nil {
			t.Errorf("Wanted=nil but got=%s", err)
		}
		if want != got {
			t.Errorf("Wanted=%d but got=%d for %v on iteration=%d", want, got, sl, i)
		}
	}
}
