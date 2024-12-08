package day6

import (
	"github.com/Romanmc72/adventofcode/2024/util"
)

var directionToCharacter = map[util.Coordinate]string{
	{X: 0, Y: 1}:  "v",
	{X: -1, Y: 0}: "<",
	{X: 0, Y: -1}: "^",
	{X: 1, Y: 0}:  ">",
}

type Guard struct {
	Position  util.Coordinate
	Direction util.Coordinate
}

// Guard always spawns as the "^" character which means he is always going "up"
// when he starts
func NewGuard(pos util.Coordinate) *Guard {
	return &Guard{
		Direction: util.Coordinate{X: 0, Y: -1},
		Position:  pos,
	}
}

func (g Guard) NextPosition() util.Coordinate {
	return util.Coordinate{
		X: g.Position.X + g.Direction.X,
		Y: g.Position.Y + g.Direction.Y,
	}
}

func (g *Guard) TurnRight() {
	rotations := map[util.Coordinate]util.Coordinate{
		{X: 0, Y: 1}:  {X: -1, Y: 0},
		{X: -1, Y: 0}: {X: 0, Y: -1},
		{X: 0, Y: -1}: {X: 1, Y: 0},
		{X: 1, Y: 0}:  {X: 0, Y: 1},
	}
	g.Direction = rotations[g.Direction]
}

func (g Guard) String() string {
	rotations := map[util.Coordinate]string{
		{X: 0, Y: 1}:  "v",
		{X: -1, Y: 0}: "<",
		{X: 0, Y: -1}: "^",
		{X: 1, Y: 0}:  ">",
	}
	return rotations[g.Direction]
}
