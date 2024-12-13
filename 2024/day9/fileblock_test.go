package day9

import "testing"

func TestFileBlockPointerSwap(t *testing.T) {
	fb1 := &FileBlock{FileId: 1, Empty: false, PreviousFileBlock: nil}
	fb2 := &FileBlock{FileId: 2, Empty: false, PreviousFileBlock: fb1}
	fb1.NextFileBlock = fb2
	fb3 := &FileBlock{FileId: 3, Empty: false, PreviousFileBlock: fb2}
	fb2.NextFileBlock = fb3
	fb4 := &FileBlock{FileId: 4, Empty: false, PreviousFileBlock: fb3}
	fb3.NextFileBlock = fb4
	fb5 := &FileBlock{FileId: 5, Empty: false, PreviousFileBlock: fb4}
	fb4.NextFileBlock = fb5
	fb6 := &FileBlock{FileId: 6, Empty: false, PreviousFileBlock: fb5, NextFileBlock: nil}
	fb5.NextFileBlock = fb6

	head := fb1
	for i := 1; i <= 6; i++ {
		if head.FileId != i {
			t.Errorf("Ensuring correct initial order, wanted FileId=%d but got FileId=%d", i, head.FileId)
		}
		head = head.NextFileBlock
	}
	fb2.SwapSpots(fb4)
	head = fb1
	wantedOrder := []int{1, 4, 3, 2, 5, 6}
	for _, wantedFileId := range wantedOrder {
		if wantedFileId != head.FileId {
			t.Errorf("Checking post-swap order, wanted FileId=%d but got FileId=%d", wantedFileId, head.FileId)
		}
		head = head.NextFileBlock
	}
	tail := fb6
	wantedOrder = []int{6, 5, 2, 3, 4, 1}
	for _, wantedFileId := range wantedOrder {
		if wantedFileId != tail.FileId {
			t.Errorf("Checking post-swap order (reverse), wanted FileId=%d but got FileId=%d", wantedFileId, tail.FileId)
		}
		tail = tail.PreviousFileBlock
	}
	fb1.SwapSpots(fb6)
	head = fb6
	wantedOrder = []int{6, 4, 3, 2, 5, 1}
	for _, wantedFileId := range wantedOrder {
		if wantedFileId != head.FileId {
			t.Errorf("Checking post-swap order swapping ends, wanted FileId=%d but got FileId=%d", wantedFileId, head.FileId)
		}
		head = head.NextFileBlock
	}
	tail = fb1
	wantedOrder = []int{1, 5, 2, 3, 4, 6}
	for _, wantedFileId := range wantedOrder {
		if wantedFileId != tail.FileId {
			t.Errorf("Checking post-swap order swapping ends (reverse), wanted FileId=%d but got FileId=%d", wantedFileId, tail.FileId)
		}
		tail = tail.PreviousFileBlock
	}
	head = fb6
	fb2.SwapSpots(fb3)
	wantedOrder = []int{6, 4, 2, 3, 5, 1}
	for _, wantedFileId := range wantedOrder {
		if wantedFileId != head.FileId {
			t.Errorf("Checking post-swap on adjacent blocks, wanted FileId=%d but got FileId=%d", wantedFileId, head.FileId)
		}
		head = head.NextFileBlock
	}
	tail = fb1
	wantedOrder = []int{1, 5, 3, 2, 4, 6}
	for _, wantedFileId := range wantedOrder {
		if wantedFileId != tail.FileId {
			t.Errorf("Checking post-swap on adjacent blocks (reverse), wanted FileId=%d but got FileId=%d", wantedFileId, tail.FileId)
		}
		tail = tail.PreviousFileBlock
	}
}
