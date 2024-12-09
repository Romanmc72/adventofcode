package days

import (
	"fmt"
	"testing"
)

func TestDay07Operators(t *testing.T) {
	x := 13
	y := 47
	want := x * y
	got := Multiply(x, y)
	if got != want {
		t.Errorf("With x=%d and y=%d and Multiply() wanted=%d but got=%d", x, y, want, got)
	}
	want = x + y
	got = Add(x, y)
	if got != want {
		t.Errorf("With x=%d and y=%d and Add() wanted=%d but got=%d", x, y, want, got)
	}
	want = 1347
	got = Concat(x, y)
	if got != want {
		t.Errorf("With x=%d and y=%d and Concat() wanted=%d but got=%d", x, y, want, got)
	}
}

func TestDay07MakePermutations(t *testing.T) {
	operands := 4
	part := 2
	want := [][]Operator{
		{Add, Add, Add},
		{Add, Add, Multiply},
		{Add, Add, Concat},
		{Add, Multiply, Add},
		{Add, Multiply, Multiply},
		{Add, Multiply, Concat},
		{Add, Concat, Add},
		{Add, Concat, Multiply},
		{Add, Concat, Concat},
		{Multiply, Add, Add},
		{Multiply, Add, Multiply},
		{Multiply, Add, Concat},
		{Multiply, Multiply, Add},
		{Multiply, Multiply, Multiply},
		{Multiply, Multiply, Concat},
		{Multiply, Concat, Add},
		{Multiply, Concat, Multiply},
		{Multiply, Concat, Concat},
		{Concat, Add, Add},
		{Concat, Add, Multiply},
		{Concat, Add, Concat},
		{Concat, Multiply, Add},
		{Concat, Multiply, Multiply},
		{Concat, Multiply, Concat},
		{Concat, Concat, Add},
		{Concat, Concat, Multiply},
		{Concat, Concat, Concat},
	}
	got := MakePermutations(operands, part)
	for rowNum, operations := range want {
		for index, operator := range operations {
			wantOp := fmt.Sprintf("%v", operator)
			gotOp := fmt.Sprintf("%v", got[rowNum][index])
			if wantOp != gotOp {
				t.Errorf("Wanted=%s but got=%s for position [%d][%d] in MakePermutations(%d, %d)", wantOp, gotOp, rowNum, index, operands, part)
			}
		}
	}
}
