package day6

import (
	"strings"
	"testing"
)

func TestMatrixString(t *testing.T) {
	data := strings.Join([]string{
		"..#.....",
		"......#.",
		"........",
		"..^.....",
	}, "\n")
	want := strings.Join([]string{
		"..#.....",
		"..^>>>#.",
		"..^..v..",
		"..^..v..",
	}, "\n")
	matrix := NewMatrixFromData(data)
	matrix.Walk()
	got := matrix.String()
	if want != got {
		t.Errorf("Wanted\n%s\n but got\n%s\n", want, got)
	}
}

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
	}
}
