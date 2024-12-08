package day6

import (
	"strings"
	"testing"
)

func TestMatrixWalk(t *testing.T) {
	type testCase struct {
		data    string
		want    int
		wantErr bool
		desc    string
	}

	cases := []testCase{
		{
			data: strings.Join([]string{
				"....#.....",
				".........#",
				"..........",
				"..#.......",
				".......#..",
				"..........",
				".#..^.....",
				"........#.",
				"#.........",
				"......#...",
			}, "\n"),
			want:    41,
			wantErr: false,
			desc:    "example data",
		},
		{
			data: strings.Join([]string{
				"..#.....",
				"......#.",
				".#......",
				"..^..#..",
			}, "\n"),
			want:    9,
			wantErr: true,
			desc:    "should raise an error on a loop",
		},
		{
			data: strings.Join([]string{
				"..#.....",
				"......#.",
				"........",
				"..^.....",
			}, "\n"),
			want:    8,
			wantErr: false,
			desc:    "should exit fine and take a turn",
		},
	}

	for _, c := range cases {
		matrix := NewMatrixFromData(c.data)
		err := matrix.Walk()
		gotErr := err != nil
		if gotErr != c.wantErr {
			t.Errorf("%s\nWanted error=%v; got error=%v; err=%s; matrix=\n%s\n", c.desc, c.wantErr, gotErr, err, matrix)
		}
		got := matrix.CountVisitedSpots()
		if got != c.want {
			t.Errorf("%s\nWanted=%d; got=%d; err=%s; matrix=\n%s\n", c.desc, c.want, got, err, matrix)
		}
	}
}

func TestMatrixFindBlockableSpots(t *testing.T) {
	type testCase struct {
		data     string
		want     int
		desc     string
		shouldBe string
	}

	cases := []testCase{
		{
			data: strings.Join([]string{
				"....#.....",
				".........#",
				"..........",
				"..#.......",
				".......#..",
				"..........",
				".#..^.....",
				"........#.",
				"#.........",
				"......#...",
			}, "\n"),
			want: 6,
			desc: "example data",
			shouldBe: strings.Join([]string{
				"....#.....",
				".........#",
				"..........",
				"..#.......",
				".......#..",
				"..........",
				".#.O.....>",
				"......OO#.",
				"#O.O......",
				"......#O..",
			}, "\n"),
		},
		{
			data: strings.Join([]string{
				"..#.....",
				"......#.",
				"........",
				"..^..#..",
			}, "\n"),
			want: 1,
			desc: "should have 1 blockable spot",
			shouldBe: strings.Join([]string{
				"..#.....",
				"......#.",
				".O......",
				"....v#..",
			}, "\n"),
		},
		{
			data: strings.Join([]string{
				"..#.....",
				"......#.",
				"........",
				"..^.....",
			}, "\n"),
			want: 0,
			desc: "zero blockable spots",
			shouldBe: strings.Join([]string{
				"..#.....",
				"......#.",
				"........",
				".......>",
			}, "\n"),
		},
	}

	for _, c := range cases {
		matrix := NewMatrixFromData(c.data)
		err := matrix.Walk()
		if err != nil {
			t.Errorf("%s\nWanted error=false; got error=true; err=%s; matrix=\n%s\n", c.desc, err, matrix)
			return
		}
		matrix.FindBlockableSpots()
		got := matrix.CountBlockableSpots()
		if got != c.want {
			t.Errorf("%s\nWanted=%d; got=%d; matrix=\n%s\n", c.desc, c.want, got, matrix)
		}
		is := matrix.String()
		if is != c.shouldBe {
			t.Errorf("Matrix looks like:\n%s\nBut should look like:\n%s\n", is, c.shouldBe)
		}
	}
}
