package util

import "fmt"

func DayToFolder(day int) string {
	return fmt.Sprintf("%02d", day)
}
