package day9

import (
	"strconv"
	"strings"
)

type FileSystem struct {
	Head *FileBlock
	Tail *FileBlock
}

// TODO: implement Defrag and Files as well as empty chunks instead of individual blocks
// func (fs *FileSystem) Defrag() {}

func (fs *FileSystem) Compact() {
	lowestFileId := 0
	var highestFileId int
	head := fs.Head
	tail := fs.Tail
	controlLoop:
	for head.NextFileBlock != nil && tail.PreviousFileBlock != nil {
		for !head.Empty {
			if head.NextFileBlock == nil {
				break controlLoop
			}
			lowestFileId = head.FileId
			head = head.NextFileBlock
		}
		for tail.Empty {
			if tail.PreviousFileBlock == nil {
				break controlLoop
			}
			tail = tail.PreviousFileBlock
		}
		highestFileId = tail.FileId
		if lowestFileId >= highestFileId {
			break controlLoop
		}
		head.SwapSpots(tail)
		head, tail = tail, head
		head = head.NextFileBlock
		if tail.FileId == 0 && !tail.Empty {
			break
		}
		tail = tail.PreviousFileBlock
	}
}

func (fs FileSystem) String() string {
	s := []string{}
	for block := range fs.Iter {
		s = append(s, block.String())
	}
	return strings.Join(s, "")
}

func (fs *FileSystem) Iter(yield func(*FileBlock) bool) {
	fb := fs.Head
	for fb != nil {
		if !yield(fb) {
			return
		}
		fb = fb.NextFileBlock
	}
}

func (fs FileSystem) Checksum() int {
	checksum := 0
	newPosition := 0
	for block := range fs.Iter {
		if !block.Empty {
			checksum += block.FileId * newPosition
			newPosition++
		}
	}
	return checksum
}

func NewFileSystemFromData(data string) (fileSystem FileSystem, err error) {
	individualPieces := strings.Split(data, "")
	var fileBlock *FileBlock
	var previousBlock *FileBlock
	isFileBlock := true
	for i := 0; i < len(data); i++ {
		if isFileBlock {
			fileSize, err := strconv.Atoi(individualPieces[i])
			if err != nil { return fileSystem, err }
			for block := 0; block < fileSize; block++ {
				if fileBlock == nil {
					fileBlock = &FileBlock{FileId: i / 2, Empty: false}
					fileSystem.Head = fileBlock
					continue
				}
				previousBlock = fileBlock
				fileBlock = &FileBlock{FileId: i / 2, Empty: false, PreviousFileBlock: previousBlock}
				previousBlock.NextFileBlock = fileBlock
			}
		} else {
			emptySpaces, err := strconv.Atoi(individualPieces[i])
			if err != nil { return fileSystem, err }
			for space := 0; space < emptySpaces; space++ {
				previousBlock = fileBlock
				fileBlock = &FileBlock{FileId: 0, Empty: true, PreviousFileBlock: previousBlock}
				previousBlock.NextFileBlock = fileBlock
			}
		}
		isFileBlock = !isFileBlock
	}
	fileSystem.Tail = fileBlock
	return fileSystem, nil
}
