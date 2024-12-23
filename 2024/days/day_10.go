package days

import (
	_ "embed"
	"fmt"
	"strings"

	"github.com/Romanmc72/adventofcode/2024/util"
)

//go:embed data/10/input.txt
var real10Data []byte

//go:embed data/10/example.txt
var example10Data []byte

func Solve10(part int, example bool) error {
	var data string
	if example {
		data = string(example10Data)
	} else {
		data = string(real10Data)
	}
	trailMap, err := NewTrailMapFromData(data)
	if err != nil {
		return err
	}
	trailMap.TraverseTrails()
	if part < 1 || part == 1 {
		fmt.Println("Day 10 Part 1 Solution:", trailMap.GetScore())
	}
	if part < 1 || part == 2 {
		fmt.Println("Day 10 Part 2 Solution:", trailMap.GetRating())
	}
	return nil
}

type VisitedSpots map[TrailMarker]bool

func (v *VisitedSpots) AlreadyBeen(tm TrailMarker) bool {
	_, beenThere := (*v)[tm]
	return beenThere
}

func (v *VisitedSpots) Visit(tm TrailMarker) {
	(*v)[tm] = true
}

type TrailMarker struct {
	Height   int
	Location util.Coordinate
}

type TrailMap struct {
	trailHeads   []TrailMarker
	bounds       util.Coordinate
	trailMarkers [][]TrailMarker
	totalScore   int
	totalRating  int
}

// This will take the naive approach, but could benefit from some memoization
// on prior visited points from other trail heads.
// *must haves*
// Are the trail must not double count the same peak point.
// If it reached that 9 already then count it out.
//
// plan is to iterate all the trail heads and keep going up until an endpoint
// is reached and once it is to add 1 to the total score, using a set to track
// all prior visited endpoints for a given trail head.
func (m *TrailMap) TraverseTrails() {
	for _, th := range m.trailHeads {
		priorSpots := make(VisitedSpots)
		m.totalScore += m.hikeUpWhereYouCan(th, &priorSpots)
		m.totalRating += m.alwaysGoUp(th)
	}
}

func (m TrailMap) hikeUpWhereYouCan(spot TrailMarker, vs *VisitedSpots) int {
	n := 0
	for _, s := range m.getAvailableSteps(spot) {
		if vs.AlreadyBeen(s) {
			continue
		}
		vs.Visit(s)
		if s.Height == 9 {
			n += 1
			continue
		}
		n += m.hikeUpWhereYouCan(s, vs)
	}
	return n
}

func (m TrailMap) alwaysGoUp(spot TrailMarker) int {
	n := 0
	for _, s := range m.getAvailableSteps(spot) {
		if s.Height == 9 {
			n += 1
			continue
		}
		n += m.alwaysGoUp(s)
	}
	return n
}

func (m TrailMap) GetScore() int {
	return m.totalScore
}

func (m TrailMap) GetRating() int {
	return m.totalRating
}

func NewTrailMapFromData(data string) (tm TrailMap, err error) {
	lines := strings.Split(data, "\n")
	tm.bounds.Y = len(lines)
	tm.bounds.X = len(lines[0])
	tm.trailMarkers = make([][]TrailMarker, tm.bounds.Y)
	for y, line := range lines {
		row := make([]TrailMarker, tm.bounds.X)
		heights, err := parseLineToListOfInts(line, "")
		if err != nil {
			return tm, err
		}
		for x, h := range heights {
			marker := TrailMarker{
				Location: util.Coordinate{X: x, Y: y},
				Height:   h,
			}
			row[x] = marker
			if h == 0 {
				tm.trailHeads = append(tm.trailHeads, marker)
			}
		}
		tm.trailMarkers[y] = row
	}
	return tm, nil
}

func (m TrailMap) getTrailMarker(c util.Coordinate) (TrailMarker, error) {
	if c.X >= 0 && c.X < m.bounds.X && c.Y >= 0 && c.Y < m.bounds.Y {
		return m.trailMarkers[c.Y][c.X], nil
	}
	return TrailMarker{}, fmt.Errorf("could not fetch that location, it is out of bounds, %s", c)
}

func (m TrailMap) getAbove(tm TrailMarker) (TrailMarker, bool) {
	above, err := m.getTrailMarker(util.Coordinate{X: tm.Location.X, Y: tm.Location.Y - 1})
	return above, err == nil
}

func (m TrailMap) getBelow(tm TrailMarker) (TrailMarker, bool) {
	below, err := m.getTrailMarker(util.Coordinate{X: tm.Location.X, Y: tm.Location.Y + 1})
	return below, err == nil
}

func (m TrailMap) getLeft(tm TrailMarker) (TrailMarker, bool) {
	left, err := m.getTrailMarker(util.Coordinate{X: tm.Location.X - 1, Y: tm.Location.Y})
	return left, err == nil
}

func (m TrailMap) getRight(tm TrailMarker) (TrailMarker, bool) {
	right, err := m.getTrailMarker(util.Coordinate{X: tm.Location.X + 1, Y: tm.Location.Y})
	return right, err == nil
}

func (m TrailMap) getAvailableSteps(tm TrailMarker) (viableNextSteps []TrailMarker) {
	if above, ok := m.getAbove(tm); ok && above.Height == tm.Height+1 {
		viableNextSteps = append(viableNextSteps, above)
	}
	if below, ok := m.getBelow(tm); ok && below.Height == tm.Height+1 {
		viableNextSteps = append(viableNextSteps, below)
	}
	if left, ok := m.getLeft(tm); ok && left.Height == tm.Height+1 {
		viableNextSteps = append(viableNextSteps, left)
	}
	if right, ok := m.getRight(tm); ok && right.Height == tm.Height+1 {
		viableNextSteps = append(viableNextSteps, right)
	}
	return viableNextSteps
}
