package day6

import (
	"fmt"
	"strings"

	"github.com/Romanmc72/adventofcode/2024/util"
)

type Matrix struct {
	grid     [][]*Space
	guard    *Guard
	xBound   int
	yBound   int
	blockers map[util.Coordinate]interface{}
	history  []Space
}

func NewMatrixFromData(data string) Matrix {
	lines := strings.Split(data, "\n")
	yBound := len(lines)
	xBound := len(lines[0])
	grid := make([][]*Space, yBound)
	guard := NewGuard(util.Coordinate{X: 0, Y: 0})
	for yPos, line := range lines {
		row := make([]*Space, xBound)
		for xPos, char := range line {
			space, tempGuard := NewSpaceFromRune(char, xPos, yPos)
			if tempGuard != nil {
				guard = tempGuard
			}
			row[xPos] = &space
		}
		grid[yPos] = row
	}
	return Matrix{
		grid:     grid,
		guard:    guard,
		xBound:   xBound,
		yBound:   yBound,
		blockers: make(map[util.Coordinate]interface{}),
		history: []Space{
			grid[guard.Position.Y][guard.Position.X].Copy(),
		},
	}
}

func (m Matrix) isBlocked(spot util.Coordinate) bool {
	return m.grid[spot.Y][spot.X].Blocked
}

func (m *Matrix) MoveGuard() error {
	spot := m.guard.NextPosition()
	m.guard.Position = spot

	newSpot := m.grid[spot.Y][spot.X]
	if newSpot.Visited && newSpot.VisitedDirection == m.guard.Direction {
		return fmt.Errorf("this is an infinite loop")
	}
	m.grid[spot.Y][spot.X].Visited = true
	m.grid[spot.Y][spot.X].VisitedDirection = m.guard.Direction
	m.history = append(m.history, m.grid[spot.Y][spot.X].Copy())
	return nil
}

func (m *Matrix) Walk() error {
	for 0 <= m.guard.NextPosition().X && m.guard.NextPosition().X < m.xBound && 0 <= m.guard.NextPosition().Y && m.guard.NextPosition().Y < m.yBound {
		if m.isBlocked(m.guard.NextPosition()) {
			m.guard.TurnRight()
			continue
		}
		err := m.MoveGuard()
		if err != nil {
			return err
		}
	}
	return nil
}

func (m *Matrix) FindBlockableSpots() {
	m.Walk()
	for len(m.history) > 1 {
		m.WipeVisitedHistory()
		addBarrierHere, err := m.MoonwalkGuardOneStep()
		if err != nil {
			break
		}
		m.grid[addBarrierHere.Position.Y][addBarrierHere.Position.X].Blocked = true
		since := len(m.history) - 1
		err = m.Walk()
		if err != nil {
			m.blockers[addBarrierHere.Position] = true
		}
		m.history = m.history[:since+1]
		m.grid[addBarrierHere.Position.Y][addBarrierHere.Position.X].Blocked = false
	}
	m.WipeVisitedHistory()
}

func (m *Matrix) WipeVisitedHistory() {
	for _, row := range m.grid {
		for _, space := range row {
			space.Visited = false
			space.VisitedDirection = util.Coordinate{}
		}
	}
}

func (m *Matrix) MoonwalkGuardOneStep() (Space, error) {
	if len(m.history) <= 1 {
		return Space{}, fmt.Errorf("cannot go back, already at the end of the history")
	}
	last := len(m.history) - 1
	oneStepBack := m.history[last]
	m.history = m.history[:last]
	m.guard.Position = m.history[last-1].Position
	m.guard.Direction = m.history[last-1].VisitedDirection
	return oneStepBack, nil
}

func (m Matrix) CountBlockableSpots() int {
	return len(m.blockers)
}

func (m Matrix) CountVisitedSpots() int {
	visitedSpots := 0
	for _, row := range m.grid {
		for _, space := range row {
			if space.Visited {
				visitedSpots++
			}
		}
	}
	return visitedSpots
}

func (m Matrix) String() string {
	rows := make([][]string, len(m.grid))
	for y, row := range m.grid {
		rowOfChars := make([]string, len(row))
		for x, space := range row {
			rowOfChars[x] = space.String()
		}
		rows[y] = rowOfChars
	}
	rows[m.guard.Position.Y][m.guard.Position.X] = m.guard.String()
	for blockableSpot := range m.blockers {
		rows[blockableSpot.Y][blockableSpot.X] = "O"
	}
	outRows := make([]string, len(m.grid))
	for index, row := range rows {
		outRows[index] = strings.Join(row, "")
	}
	return strings.Join(outRows, "\n")
}
