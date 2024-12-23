package day9

import (
	"fmt"
	"strconv"
	"strings"
)

type FileSystem struct {
	Head     *FileBlock
	Tail     *FileBlock
	HeadFile *File
	TailFile *File
}

func (fs *FileSystem) Defrag() {
	head := fs.HeadFile
	tail := fs.TailFile
controlLoop:
	for tail != nil && tail.PreviousFile != nil {
		// get the next empty head...
		for !head.Empty {
			// if you hit the end, move onto the next tail piece and restart
			if head.NextFile == nil || head == tail {
				if tail == nil || tail.PreviousFile == nil {
					break controlLoop
				}
				tail = tail.PreviousFile
				head = fs.HeadFile
				continue
			}
			head = head.NextFile
		}
		// get the next non-empty tail
		for tail.Empty {
			if tail.PreviousFile == nil {
				break controlLoop
			}
			if tail == head {
				head = fs.HeadFile
				tail = tail.PreviousFile
				continue
			}
			tail = tail.PreviousFile
		}
		if head.Size == tail.Size {
			head.SwapSpots(tail)
			tail = head.PreviousFile
			head = fs.HeadFile
		} else if head.Size < tail.Size {
			head = head.NextFile
			continue
		} else {
			leftHead, rightHead := head.SplitEmpty(tail.Size)
			if leftHead == nil || rightHead == nil {
				panic("Ah crap I messed up somewhere")
			}
			head = leftHead
			head.SwapSpots(tail)
			tail = head.PreviousFile
			head = fs.HeadFile
		}
		if tail.FileId == 0 && !tail.Empty {
			break
		}
	}
}

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

func (fs FileSystem) FileString() string {
	s := []string{}
	for f := range fs.IterFiles {
		s = append(s, f.String())
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

func (fs *FileSystem) IterFiles(yield func(*File) bool) {
	f := fs.HeadFile
	for f != nil {
		if !yield(f) {
			return
		}
		f = f.NextFile
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

func (fs FileSystem) ChecksumFiles() int {
	checksum := 0
	newPosition := 0
	for file := range fs.IterFiles {
		for i := 0; i < file.Size; i++ {
			checksum += file.FileId * newPosition
			newPosition++
		}
	}
	return checksum
}

// just going to store the file and the file blocks as independent things
func NewFileSystemFromData(data string) (fileSystem FileSystem, err error) {
	individualPieces := strings.Split(data, "")
	var fileBlock *FileBlock
	var previousBlock *FileBlock
	var file *File
	var previous *File
	isFileBlock := true
	for i := 0; i < len(data); i++ {
		if isFileBlock {
			fileId := i / 2
			fileSize, err := strconv.Atoi(individualPieces[i])
			if err != nil {
				return fileSystem, err
			}
			if fileSize == 0 {
				return fileSystem, fmt.Errorf("file blocks must be of size 0 or greater, block id=%d was size zero at position=%d", fileId, i)
			}
			if file == nil {
				file = &File{
					FileId:       fileId,
					Size:         fileSize,
					Empty:        false,
					PreviousFile: nil,
				}
				fileSystem.HeadFile = file
			} else {
				previous = file
				file = &File{
					FileId:       fileId,
					Size:         fileSize,
					Empty:        false,
					PreviousFile: previous,
				}
				previous.NextFile = file
			}
			for block := 0; block < fileSize; block++ {
				if fileBlock == nil {
					fileBlock = &FileBlock{FileId: fileId, Empty: false}
					fileSystem.Head = fileBlock
					continue
				}
				previousBlock = fileBlock
				fileBlock = &FileBlock{FileId: fileId, Empty: false, PreviousFileBlock: previousBlock}
				previousBlock.NextFileBlock = fileBlock
			}
		} else {
			emptySpaces, err := strconv.Atoi(individualPieces[i])
			if err != nil {
				return fileSystem, err
			}
			if emptySpaces > 0 {
				previous = file
				file = &File{
					Empty:        true,
					FileId:       0,
					Size:         emptySpaces,
					PreviousFile: previous,
				}
				previous.NextFile = file
			}
			for space := 0; space < emptySpaces; space++ {
				previousBlock = fileBlock
				fileBlock = &FileBlock{FileId: 0, Empty: true, PreviousFileBlock: previousBlock}
				previousBlock.NextFileBlock = fileBlock
			}
		}
		isFileBlock = !isFileBlock
	}
	fileSystem.Tail = fileBlock
	fileSystem.TailFile = file
	return fileSystem, nil
}
