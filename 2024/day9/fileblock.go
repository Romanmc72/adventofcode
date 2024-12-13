package day9

import "fmt"

type FileBlock struct {
	FileId int
	Empty bool
	NextFileBlock *FileBlock
	PreviousFileBlock *FileBlock
}

func (fb FileBlock) String() string {
	if fb.Empty { return "(.)" }
	return fmt.Sprintf("[%d]", fb.FileId)
}

// Move the pointers around!
func (fb *FileBlock) SwapSpots(other *FileBlock) {
	if fb == other || other == nil { return }

	// in the event that these 2 are adjacent already, then we need
	// to not have them point to themselves on a swap.
	if fb.NextFileBlock == other {
		selfPrevious := fb.PreviousFileBlock
		otherNext := other.NextFileBlock

		selfPrevious.NextFileBlock = other
		other.PreviousFileBlock = selfPrevious
		otherNext.PreviousFileBlock = fb
		fb.NextFileBlock = otherNext
		fb.PreviousFileBlock, other.NextFileBlock = other, fb
		return
	}
	if fb.PreviousFileBlock == other {
		selfNext := fb.NextFileBlock
		otherPrevious := other.PreviousFileBlock

		selfNext.PreviousFileBlock = other
		other.NextFileBlock = selfNext
		otherPrevious.NextFileBlock = fb
		fb.PreviousFileBlock = otherPrevious
		fb.NextFileBlock, other.PreviousFileBlock = other, fb
		return
	}

	selfPrevious := fb.PreviousFileBlock
	selfNext := fb.NextFileBlock
	otherPrevious := other.PreviousFileBlock
	otherNext := other.NextFileBlock

	if selfPrevious != nil {
		selfPrevious.NextFileBlock = other
	}
	other.PreviousFileBlock = selfPrevious
	if selfNext != nil {
		selfNext.PreviousFileBlock = other
	}
	other.NextFileBlock = selfNext

	if otherPrevious != nil {
		otherPrevious.NextFileBlock = fb
	}
	fb.PreviousFileBlock = otherPrevious

	if otherNext != nil {
		otherNext.PreviousFileBlock = fb
	}
	fb.NextFileBlock = otherNext
}
