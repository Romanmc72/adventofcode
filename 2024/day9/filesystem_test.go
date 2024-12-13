package day9

import (
	"testing"
	"time"
)

func TestDefragFileSystemAndChecksum(t *testing.T) {
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
			t.Fatalf("Defrag timed out after %d seconds", timeoutSec)
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
		t.Errorf("Defrag() && Checksum(), wanted=%d but got=%d", wantNum, gotNum)
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
