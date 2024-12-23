package day9

import "testing"

func TestFilePointerSwap(t *testing.T) {
	f1 := &File{FileId: 1, Empty: false, PreviousFile: nil}
	f2 := &File{FileId: 2, Empty: false, PreviousFile: f1}
	f1.NextFile = f2
	f3 := &File{FileId: 3, Empty: false, PreviousFile: f2}
	f2.NextFile = f3
	f4 := &File{FileId: 4, Empty: false, PreviousFile: f3}
	f3.NextFile = f4
	f5 := &File{FileId: 5, Empty: false, PreviousFile: f4}
	f4.NextFile = f5
	f6 := &File{FileId: 6, Empty: false, PreviousFile: f5, NextFile: nil}
	f5.NextFile = f6

	head := f1
	for i := 1; i <= 6; i++ {
		if head.FileId != i {
			t.Errorf("Ensuring correct initial order, wanted FileId=%d but got FileId=%d", i, head.FileId)
		}
		head = head.NextFile
	}
	f2.SwapSpots(f4)
	head = f1
	wantedOrder := []int{1, 4, 3, 2, 5, 6}
	for _, wantedFileId := range wantedOrder {
		if wantedFileId != head.FileId {
			t.Errorf("Checking post-swap order, wanted FileId=%d but got FileId=%d", wantedFileId, head.FileId)
		}
		head = head.NextFile
	}
	tail := f6
	wantedOrder = []int{6, 5, 2, 3, 4, 1}
	for _, wantedFileId := range wantedOrder {
		if wantedFileId != tail.FileId {
			t.Errorf("Checking post-swap order (reverse), wanted FileId=%d but got FileId=%d", wantedFileId, tail.FileId)
		}
		tail = tail.PreviousFile
	}
	f1.SwapSpots(f6)
	head = f6
	wantedOrder = []int{6, 4, 3, 2, 5, 1}
	for _, wantedFileId := range wantedOrder {
		if wantedFileId != head.FileId {
			t.Errorf("Checking post-swap order swapping ends, wanted FileId=%d but got FileId=%d", wantedFileId, head.FileId)
		}
		head = head.NextFile
	}
	tail = f1
	wantedOrder = []int{1, 5, 2, 3, 4, 6}
	for _, wantedFileId := range wantedOrder {
		if wantedFileId != tail.FileId {
			t.Errorf("Checking post-swap order swapping ends (reverse), wanted FileId=%d but got FileId=%d", wantedFileId, tail.FileId)
		}
		tail = tail.PreviousFile
	}
	head = f6
	f2.SwapSpots(f3)
	wantedOrder = []int{6, 4, 2, 3, 5, 1}
	for _, wantedFileId := range wantedOrder {
		if wantedFileId != head.FileId {
			t.Errorf("Checking post-swap on adjacent blocks, wanted FileId=%d but got FileId=%d", wantedFileId, head.FileId)
		}
		head = head.NextFile
	}
	tail = f1
	wantedOrder = []int{1, 5, 3, 2, 4, 6}
	for _, wantedFileId := range wantedOrder {
		if wantedFileId != tail.FileId {
			t.Errorf("Checking post-swap on adjacent blocks (reverse), wanted FileId=%d but got FileId=%d", wantedFileId, tail.FileId)
		}
		tail = tail.PreviousFile
	}
	head = f6
	f2.SwapSpots(f3)
	wantedOrder = []int{6, 4, 3, 2, 5, 1}
	for _, wantedFileId := range wantedOrder {
		if wantedFileId != head.FileId {
			t.Errorf("Checking post-swap on adjacent blocks, swap back, wanted FileId=%d but got FileId=%d", wantedFileId, head.FileId)
		}
		head = head.NextFile
	}
	head = f6
	f1.SwapSpots(f1)
	f1.SwapSpots(nil)
	wantedOrder = []int{6, 4, 3, 2, 5, 1}
	for _, wantedFileId := range wantedOrder {
		if wantedFileId != head.FileId {
			t.Errorf("Checking post-swap on self/nil, wanted FileId=%d but got FileId=%d", wantedFileId, head.FileId)
		}
		head = head.NextFile
	}
}

func TestFileSplitEmpty(t *testing.T) {
	l := File{Empty: false, FileId: 0, Size: 3}
	e := File{Empty: true, Size: 6, PreviousFile: &l}
	l.NextFile = &e
	r := File{Empty: false, FileId: 1, PreviousFile: &e, Size: 2}
	e.NextFile = &r
	le, re := e.SplitEmpty(6)
	if le != nil || re != nil {
		t.Errorf("Wanted nil, nil but got %s, %s", le, re)
	}
	le, re = e.SplitEmpty(2)
	if le.Size != 2 || re.Size != 4 {
		t.Errorf("Wanted 2, 4 but got %s, %s after splitting", le, re)
	}
	if le.PreviousFile != &l || re.NextFile != &r {
		t.Errorf("Wanted pointers to %s, %s but got %s, %s for new empties", l, r, le.PreviousFile, re.NextFile)
	}
	if l.NextFile != le || r.PreviousFile != re {
		t.Errorf("Wanted pointers to %s, %s but got %s, %s for pre-existing files", le, re, l.NextFile, r.PreviousFile)
	}
	if e.PreviousFile != nil || e.NextFile != nil {
		t.Errorf("Wanted nil, nil but got %s, %s", e.PreviousFile, e.NextFile)
	}
}
