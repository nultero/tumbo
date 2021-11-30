package serials

import (
	"fmt"
	"sort"
	"strings"

	"github.com/nultero/tics"
)

func FmtJsonToStrs(js map[string]interface{}) []string {

	maxLen := 0
	for alias := range js {
		if len(alias) > maxLen {
			maxLen = len(alias)
		}
	}
	maxLen += 3

	strs := []string{}

	for alias, cmds := range js {
		strs = append(strs, fmt.Sprintf(
			"  %v%v%v\n",
			tics.Bold(alias),
			strings.Repeat(" ", maxLen-len(alias)),
			cmds,
		))
	}

	return sortAliases(strs)
}

func sortAliases(al []string) []string {
	sort.Strings(al)
	return al
}
