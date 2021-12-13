package serials

import (
	"fmt"
	"sort"
	"strings"

	"github.com/nultero/tics"
)

// Jank way to split on the selected chunk, but it does work.
const gj = "\033[38;5;206m\u00ad\033[0m"

func GetMaxLen(js map[string]interface{}) int {
	maxLen := 0
	for alias := range js {
		if len(alias) > maxLen {
			maxLen = len(alias)
		}
	}
	return maxLen + 3
}

func FmtJsonToStrs(js map[string]interface{}) []string {
	maxLen := GetMaxLen(js)
	strs := []string{}

	for alias, cmds := range js {
		strs = append(strs, fmt.Sprintf(
			"  %v%v%v\n",
			tics.Bold(alias),
			strings.Repeat(" ", maxLen-len(alias)),
			cmds,
		))
	}

	sort.Strings(strs)
	return strs
}

func FmtStrKeys(js map[string]interface{}) []string {

	maxLen := GetMaxLen(js)
	strs := []string{}

	for alias, cmds := range js {
		strs = append(strs, fmt.Sprintf(
			"%v%v%v%v",
			alias,
			gj,
			strings.Repeat(" ", maxLen-len(alias)),
			cmds,
		))
	}

	sort.Strings(strs)
	return strs
}

func Split(choice string) string {
	return strings.Split(choice, gj)[0]
}
