package days

import (
	"testing"

	"github.com/Romanmc72/adventofcode/2024/util"
)

func TestPaseAndShowAntennae(t *testing.T) {
	input := `............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............`
	wantAntenae := map[rune][]util.Coordinate{
		'0': {
			{X: 8, Y: 1},
			{X: 5, Y: 2},
			{X: 7, Y: 3},
			{X: 4, Y: 4},
		},
		'A': {
			{X: 6, Y: 5},
			{X: 8, Y: 8},
			{X: 9, Y: 9},
		},
	}
	wantBounds := util.Coordinate{X: 12, Y: 12}
	gotAntennae, gotBounds := parseAntennae(input)
	for a, wantedLocations := range wantAntenae {
		gotLocations := gotAntennae[a]
		for index, wantLocation := range wantedLocations {
			gotLocation := gotLocations[index]
			if wantLocation != gotLocation {
				t.Errorf("Wanted=%s but got=%s location with wanted output=`%v` out of received output=`%v`", wantLocation, gotLocation, wantAntenae, gotAntennae)
			}
		}
	}
	if wantBounds != gotBounds {
		t.Errorf("Wanted bounds=%s got bounds=%s", wantBounds, gotBounds)
	}
	wantShow := `#...........
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
...........#`
	gotShow := showAntennae(gotAntennae, map[util.Coordinate]bool{{X: 0, Y: 0}: true, {X: gotBounds.X - 1, Y: gotBounds.Y - 1}: true}, gotBounds)
	if wantShow != gotShow {
		t.Errorf("not showing antennae correctly wanted=\n%s\nbut got=\n%s\n", wantShow, gotShow)
	}
}

func TestGetAntinodeLocations(t *testing.T) {
	type testCase struct {
		a    util.Coordinate
		b    util.Coordinate
		want []util.Coordinate
		desc string
	}
	testCases := []testCase{
		{
			a:    util.Coordinate{X: 0, Y: 0},
			b:    util.Coordinate{X: 1, Y: 1},
			want: []util.Coordinate{{X: -1, Y: -1}, {X: 2, Y: 2}},
			desc: "Straight line diagonally",
		},
		{
			a:    util.Coordinate{X: 2, Y: 5},
			b:    util.Coordinate{X: 4, Y: 6},
			want: []util.Coordinate{{X: 0, Y: 4}, {X: 6, Y: 7}},
			desc: "Over two, down 1",
		},
		{
			a:    util.Coordinate{X: 4, Y: 2},
			b:    util.Coordinate{X: 4, Y: 8},
			want: []util.Coordinate{{X: 4, Y: -4}, {X: 4, Y: 14}},
			desc: "Horizontal",
		},
		{
			a:    util.Coordinate{X: 7, Y: 20},
			b:    util.Coordinate{X: 7, Y: 4},
			want: []util.Coordinate{{X: 7, Y: 36}, {X: 7, Y: -12}},
			desc: "Vertical",
		},
	}
	for _, tc := range testCases {
		got := getAntinodeLocations(tc.a, tc.b)
		if len(got) != 2 {
			t.Errorf("That is a few too many points")
		}
		for index, wantedAntinode := range tc.want {
			gotAntinode := got[index]
			if wantedAntinode != gotAntinode {
				t.Errorf("%s\nWanted=%s but got=%s for getAntinodeLocations(%s, %s)", tc.desc, wantedAntinode, gotAntinode, tc.a, tc.b)
			}
		}
	}
}

func TestIsWithinBounds(t *testing.T) {
	bottomRightBounds := util.Coordinate{X: 10, Y: 10}
	inBounds := util.Coordinate{X: 5, Y: 5}
	outOfBounds := util.Coordinate{X: 11, Y: 7}
	if !isWithinBounds(inBounds, bottomRightBounds) {
		t.Errorf("Wanted %s to be within bounds of %s but was NOT!", inBounds, bottomRightBounds)
	}
	if isWithinBounds(outOfBounds, bottomRightBounds) {
		t.Errorf("Wanted %s to NOT be within bounds of %s but WAS!", outOfBounds, bottomRightBounds)
	}
}
