package day6

import (
	"github.com/Romanmc72/adventofcode/2024/util"
)

type Space struct {
	Blocked          bool
	Visited          bool
	VisitedDirection util.Coordinate
	Position         util.Coordinate
}

func (s Space) String() string {
	if s.Blocked {
		return "#"
	}
	if s.Visited {
		return directionToCharacter[s.VisitedDirection]
	}
	return "."
}

func NewSpaceFromRune(char rune, x int, y int) (Space, *Guard) {
	position := util.Coordinate{X: x, Y: y}
	if char == '#' {
		return Space{Blocked: true, Visited: false, Position: position}, nil
	}
	if char == '^' {
		guard := NewGuard(position)
		space := Space{Blocked: false, Visited: true, VisitedDirection: guard.Direction, Position: position}
		return space, guard
	}
	return Space{Blocked: false, Visited: false, Position: position}, nil
}

func (s Space) Copy() Space {
	return Space{
		Position: util.Coordinate{
			X: s.Position.X,
			Y: s.Position.Y,
		},
		VisitedDirection: util.Coordinate{
			X: s.VisitedDirection.X,
			Y: s.VisitedDirection.Y,
		},
		Visited: s.Visited,
		Blocked: s.Blocked,
	}
}
