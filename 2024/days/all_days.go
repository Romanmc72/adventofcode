package days

import "github.com/Romanmc72/adventofcode/2024/util"

var logger = util.GetLogger()

type Solution func(int, bool) error

var Solutions = []Solution{
	Solve01,
	Solve02,
	Solve03,
	Solve04,
	Solve05,
	Solve06,
	Solve07,
	Solve08,
	Solve09,
	Solve10,
	Solve11,
	Solve12,
	Solve13,
	Solve14,
	Solve15,
	Solve16,
	Solve17,
	Solve18,
	Solve19,
	Solve20,
	Solve21,
	Solve22,
	Solve23,
	Solve24,
	Solve25,
}
