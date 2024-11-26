package util

import (
	"testing"
)

func TestDayToFolder(t *testing.T) {
	type args struct {
		day  int
		want string
	}
	testCases := []args{
		{
			day:  1,
			want: "01",
		},
		{
			day:  10,
			want: "10",
		},
		{
			day:  2000,
			want: "2000",
		},
	}
	for _, testCase := range testCases {
		got := DayToFolder(testCase.day)
		if got != testCase.want {
			t.Errorf("Wanted=%s but got=%s for DayToFolder(%d)", testCase.want, got, testCase.day)
		}
	}
}
