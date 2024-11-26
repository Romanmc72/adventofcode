package util

import (
	"log/slog"
	"os"
	"strings"
)

var levelMap = map[string]slog.Leveler{
	"DEBUG": slog.LevelDebug,
	"INFO":  slog.LevelInfo,
	"WARN":  slog.LevelWarn,
	"ERROR": slog.LevelError,
}

// Get the logger at the level of your choice! Set GO_LOG_LEVEL env var to change the level.
func GetLogger() *slog.Logger {
	levelText, ok := os.LookupEnv("LOG_LEVEL")
	var level slog.Leveler
	if !ok {
		level = slog.LevelDebug
	} else {
		level = levelMap[strings.ToUpper(levelText)]
	}
	handler := slog.NewJSONHandler(os.Stderr, &slog.HandlerOptions{Level: level})
	return slog.New(handler)
}
