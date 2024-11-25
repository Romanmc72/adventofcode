package days

type Solution func (int, bool) error

var Solutions = map[int]Solution{
	1: Solve01,
	2: Solve02,
	3: Solve03,
	4: Solve04,
	5: Solve05,
	6: Solve06,
	7: Solve07,
	8: Solve08,
	9: Solve09,
	10: Solve10,
	11: Solve11,
	12: Solve12,
	13: Solve13,
	14: Solve14,
	15: Solve15,
	16: Solve16,
	17: Solve17,
	18: Solve18,
	19: Solve19,
	20: Solve20,
	21: Solve21,
	22: Solve22,
	23: Solve23,
	24: Solve24,
	25: Solve25,
}
