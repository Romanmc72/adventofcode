package days

import (
	"testing"
)

func TestDay2Part2(t *testing.T) {
	type testCase struct{
		report []int
		safe bool
		desc string
	}
	testCases := []testCase{
		{
			report: []int{11, 11},
			safe: true,
			desc: "2 or less should always pass",
		},
		{
			report: []int{11, 11, 11},
			safe: false,
			desc: "no matter what you remove a rule is violated",
		},
		{
			report: []int{11, 9, 10, 11, 12},
			safe: true,
			desc: "removing the first element makes it valid",
		},
		{
			report: []int{11, 9, 10, 11, 12, 1000},
			safe: true,
			desc: "removing the first element makes it valid except for the last element!",
		},
		{
			report: []int{10, 9, 11, 12, 13},
			safe: true,
			desc: "removing the second element makes it valid",
		},
		{
			report: []int{10, 11, 13, 12, 13},
			safe: true,
			desc: "removing the third element makes it valid",
		},
		{
			report: []int{1, 2, 3, 2, 1},
			safe: false,
			desc: "multiple violations are at play",
		},
	}
	for _, tc := range testCases {
		got := isSafe2(tc.report)
		if got != tc.safe {
			t.Errorf("%s\n Test Case `%v` did not pass, wanted=%v but got=%v", tc.desc, tc.report, tc.safe, got)
		}
	}
}
