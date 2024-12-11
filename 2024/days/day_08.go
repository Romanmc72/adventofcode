package days

import (
	_ "embed"
	"fmt"
	"strings"

	"github.com/Romanmc72/adventofcode/2024/util"
)

//go:embed data/08/input.txt
var real08Data []byte

//go:embed data/08/example.txt
var example08Data []byte

func Solve08(part int, example bool) error {
	var data string
	if example {
		data = string(example08Data)
	} else {
		data = string(real08Data)
	}
	uniqueAntinodeLocations := make(map[util.Coordinate]bool)
	uniqueAntinodeFrequencyLocations := make(map[util.Coordinate]bool)
	antennae, mapBounds := parseAntennae(data)
	for _, antennaeLocations := range antennae {
		for index, loc := range antennaeLocations {
			if index == (len(antennaeLocations) - 1) {
				break
			}
			for i := index + 1; i < len(antennaeLocations); i++ {
				nextLoc := antennaeLocations[i]
				antinodes := getAntinodeLocations(loc, nextLoc)
				for _, a := range antinodes {
					if isWithinBounds(a, mapBounds) {
						uniqueAntinodeLocations[a] = true
					}
				}
				antinodes = getAntinodeFrequencyLocations(loc, nextLoc, mapBounds)
				for _, a := range antinodes {
					if isWithinBounds(a, mapBounds) {
						uniqueAntinodeFrequencyLocations[a] = true
					}
				}
			}
		}
	}
	if part < 1 || part == 1 {
		fmt.Println(showAntennae(antennae, uniqueAntinodeLocations, mapBounds))
		fmt.Println("Day 08 Part 1 Solution:", len(uniqueAntinodeLocations))
	}
	if part < 1 || part == 2 {
		fmt.Println(showAntennae(antennae, uniqueAntinodeFrequencyLocations, mapBounds))
		fmt.Println("Day 08 Part 2 Solution:", len(uniqueAntinodeFrequencyLocations))
	}
	return nil
}

func showAntennae(antennae map[rune][]util.Coordinate, antinodes map[util.Coordinate]bool, bounds util.Coordinate) string {
	m := make([][]string, bounds.Y)
	for y := 0; y < bounds.Y; y++ {
		row := make([]string, bounds.X)
		for x := 0; x < bounds.X; x++ {
			row[x] = "."
		}
		m[y] = row
	}
	for a := range antinodes {
		m[a.Y][a.X] = "#"
	}
	for c, locations := range antennae {
		for _, l := range locations {
			m[l.Y][l.X] = string(c)
		}
	}
	s := make([]string, bounds.Y)
	for i, r := range m {
		s[i] = strings.Join(r, "")
	}
	return strings.Join(s, "\n")
}

func isWithinBounds(c util.Coordinate, b util.Coordinate) bool {
	return c.X >= 0 && c.X < b.X && c.Y >= 0 && c.Y < b.Y
}

// slope = (x1 - x2) / (y1 - y2)
func getCoordinateDelta(a util.Coordinate, b util.Coordinate) util.Coordinate {
	return util.Coordinate{X: a.X - b.X, Y: a.Y - b.Y}
}

func getAntinodeLocations(a util.Coordinate, b util.Coordinate) []util.Coordinate {
	delta := getCoordinateDelta(a, b)
	return []util.Coordinate{{X: (a.X + delta.X), Y: (a.Y + delta.Y)}, {X: (b.X - delta.X), Y: (b.Y - delta.Y)}}
}

func getAntinodeFrequencyLocations(a util.Coordinate, b util.Coordinate, bounds util.Coordinate) []util.Coordinate {
	delta := getCoordinateDelta(a, b)
	locations := []util.Coordinate{}
	leftWise := util.Coordinate{X: 0, Y: 0}
	multiplier := 0
	for isWithinBounds(leftWise, bounds) {
		leftWise = util.Coordinate{X: (a.X + (delta.X * multiplier)), Y: (a.Y + (delta.Y * multiplier))}
		locations = append(locations, leftWise)
		multiplier++
	}
	rightWise := util.Coordinate{X: 0, Y: 0}
	multiplier = 0
	for isWithinBounds(rightWise, bounds) {
		rightWise = util.Coordinate{X: (b.X - (delta.X * multiplier)), Y: (b.Y - (delta.Y * multiplier))}
		locations = append(locations, rightWise)
		multiplier++
	}
	return locations
}

func parseAntennae(data string) (map[rune][]util.Coordinate, util.Coordinate) {
	antennae := make(map[rune][]util.Coordinate)
	lines := strings.Split(data, "\n")
	mapBounds := util.Coordinate{Y: len(lines), X: len(lines[0])}
	for y, line := range lines {
		for x, char := range line {
			if char == '.' { continue }
			coords, ok := antennae[char]
			position := util.Coordinate{X: x, Y: y}
			if ok {
				coords = append(coords, position)
			} else {
				coords = []util.Coordinate{position}
			}
			antennae[char] = coords
		}
	}
	return antennae, mapBounds
}
