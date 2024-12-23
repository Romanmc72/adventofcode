package day9

import "fmt"

type File struct {
	Empty bool
	Size int
	FileId int
	NextFile *File
	PreviousFile *File
}

func (f *File) SplitEmpty(space int) (*File, *File) {
	if !f.Empty || f.Size <= space { return nil, nil }
	left := File{
		Empty: true,
		Size: space,
		NextFile: nil,
		PreviousFile: f.PreviousFile,
		FileId: 0,
	}
	right := File{
		Empty: true,
		Size: f.Size - space,
		NextFile: f.NextFile,
		PreviousFile: &left,
		FileId: 0,
	}
	left.NextFile = &right
	f.PreviousFile.NextFile = &left
	f.NextFile.PreviousFile = &right
	f.PreviousFile = nil
	f.NextFile = nil
	return &left, &right
}


func (f File) String() string {
	if f.Empty { return fmt.Sprintf("(.:%d)", f.Size) }
	return fmt.Sprintf("[%d:%d]", f.FileId, f.Size)
}

// Move the pointers around!
func (f *File) SwapSpots(other *File) {
	if f == other || other == nil { return }

	// in the event that these 2 are adjacent already, then we need
	// to not have them point to themselves on a swap.
	if f.NextFile == other {
		selfPrevious := f.PreviousFile
		otherNext := other.NextFile

		selfPrevious.NextFile = other
		other.PreviousFile = selfPrevious
		otherNext.PreviousFile = f
		f.NextFile = otherNext
		f.PreviousFile, other.NextFile = other, f
		return
	}
	if f.PreviousFile == other {
		selfNext := f.NextFile
		otherPrevious := other.PreviousFile

		selfNext.PreviousFile = other
		other.NextFile = selfNext
		otherPrevious.NextFile = f
		f.PreviousFile = otherPrevious
		f.NextFile, other.PreviousFile = other, f
		return
	}

	selfPrevious := f.PreviousFile
	selfNext := f.NextFile
	otherPrevious := other.PreviousFile
	otherNext := other.NextFile

	if selfPrevious != nil {
		selfPrevious.NextFile = other
	}
	other.PreviousFile = selfPrevious
	if selfNext != nil {
		selfNext.PreviousFile = other
	}
	other.NextFile = selfNext

	if otherPrevious != nil {
		otherPrevious.NextFile = f
	}
	f.PreviousFile = otherPrevious

	if otherNext != nil {
		otherNext.PreviousFile = f
	}
	f.NextFile = otherNext
}

