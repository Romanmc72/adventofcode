package day9

import (
	"testing"
	"time"
)

func TestCompactAndDefragFileSystemAndChecksum(t *testing.T) {
	// the example input
	input := "2333133121414131402"
	fs, err := NewFileSystemFromData(input)
	if err != nil {
		t.Errorf("NewFileSystemFromData(), wanted err=nil, got err=%s", err)
	}
	timeoutSec := 3
	timeout := time.After(time.Duration(timeoutSec) * time.Second)
	done := make(chan bool)
	//																																											Final-swap
	//																																											v			v
	//																																											v			v
	want := "[0][0](.)(.)(.)[1][1][1](.)(.)(.)[2](.)(.)(.)[3][3][3](.)[4][4](.)[5][5][5][5](.)[6][6][6][6](.)[7][7][7](.)[8][8][8][8][9][9]"
	got := fs.String()
	if want != got {
		t.Errorf("(pre-defrag) Wanted file system to print as \n%s\n but got \n%s\n", want, got)
	}
	go func() {
		fs.Compact()
		done <- true
	}()
	select {
		case <- timeout:
			t.Fatalf("Compact timed out after %d seconds", timeoutSec)
		case <- done:
	}
	want = "[0][0][9][9][8][1][1][1][8][8][8][2][7][7][7][3][3][3][6][4][4][6][5][5][5][5][6][6](.)(.)(.)(.)(.)(.)(.)(.)(.)(.)(.)(.)(.)(.)"
	got = fs.String()
	if want != got {
		t.Errorf("(post-defrag) Wanted file system to print as \n%s\n but got \n%s\n", want, got)
	}
	wantNum := 1928
	gotNum := fs.Checksum()
	if wantNum != gotNum {
		t.Errorf("Compact() && Checksum(), wanted=%d but got=%d", wantNum, gotNum)
	}
	want = "[0:2](.:3)[1:3](.:3)[2:1](.:3)[3:3](.:1)[4:2](.:1)[5:4](.:1)[6:4](.:1)[7:3](.:1)[8:4][9:2]"
	got = fs.FileString()
	if want != got {
		t.Errorf("Wanted FileString()=\n%s\nbut got=\n%s\n", want, got)
	}
	fs.Defrag()
	want = "[0:2][9:2][2:1][1:3][7:3](.:1)[4:2](.:1)[3:3](.:1)(.:2)(.:1)[5:4](.:1)[6:4](.:1)(.:3)(.:1)[8:4](.:2)"
	got = fs.FileString()
	if want != got {
		t.Errorf("Wanted FileString()=\n%s\nbut got=\n%s\n", want, got)
	}
	wantNum = 2858
	gotNum = fs.ChecksumFiles()
	if wantNum != gotNum {
		t.Errorf("Wanted %d but got %d for the Defrag() and ChecksumFiles() combo", wantNum, gotNum)
	}
}

func TestDefragAndChecksumEdgeCases(t *testing.T) {
	// edge cases that were not covered are cases where there is consecutive
	// empty space which could and should raise an error
	input := "14048"
	_, err := NewFileSystemFromData(input)
	if err == nil {
		t.Errorf("Wanted an error but got=nil creating edge cases for file system of\n%s\n", input)
	}
	// when empty spaces are moved around they should reconstruct connecting and
	// combining with one another to create a single empty space
	// instead of up to several consecutive empty ones.
	input = "143280301"
	fs, err := NewFileSystemFromData(input)
	if err != nil {
		t.Errorf("Wanted err=nil but got err=%s", err)
	}
	wantFs := "[0:1](.:4)[1:3](.:2)[2:8][3:3][4:1]"
	gotFs := fs.FileString()
	if wantFs != gotFs {
		t.Errorf("Wanted=%s but got %s for pre-defrag edge case", wantFs, gotFs)
	}
	fs.Defrag()
	wantFs = "[0:1][4:1][3:3][1:3](.:2)[2:8](.:3)(.:1)"
	gotFs = fs.FileString()
	if wantFs != gotFs {
		t.Errorf("Wanted=\n%s\nbut got=\n%s\nfor post-defrag edge case", wantFs, gotFs)
	}
	want := 265
	got := fs.ChecksumFiles()
	if want != got {
		t.Errorf("Wanted=\n%d\nbut got=\n%d\nfor defrag edge cases", want, got)
	}
}

func TestFileSystemIterator(t *testing.T) {
	input := "12345"
	fs, err := NewFileSystemFromData(input)
	if err != nil {
		t.Errorf("Unexpected error %s parsing %s", err, input)
	}
	forwards := []int{0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 2, 2, 2, 2, 2}
	backwards := []int{2, 2, 2, 2, 2, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0}
	i := 0
	for block := range fs.Iter {
		if block.FileId != forwards[i] {
			t.Errorf("Wanted=%d but got=%d in forwards file id list", forwards[i], block.FileId)
		}
		i++
	}
	tail := fs.Tail
	i = 0
	for tail.PreviousFileBlock != nil {
		if tail.FileId != backwards[i] {
			t.Errorf("Wanted=%d but got=%d in backwards file id list", backwards[i], tail.FileId)
		}
		tail = tail.PreviousFileBlock
		i++
	}
}
