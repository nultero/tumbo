package cmd

import (
	"encoding/json"
	"fmt"
	"os"
	"sort"
	"strings"
	"tumbo/cmd/cats"
	"tumbo/cmd/serials"

	"github.com/nultero/tics"
)

// Reusable func by the CRUDs -- new, remove, and update,
// that selects between the available tumbo alias types.
func selectType() string {
	s := ""
	if d, ok := confMap[dataDir]; ok {
		dir := tics.GetDirFilesExclusive(d, tics.NotConfig)
		s = tics.SelectBetween("kind of new alias?", dir)
	} else {
		tics.ThrowSys(selectType, fmt.Errorf("failure in config mapping"))
	}

	return s
}

func getJsonByType(typeName string) map[string]interface{} {
	m := map[string]interface{}{}
	if d, ok := confMap[dataDir]; ok {
		path := d + "/" + typeName
		bytes := tics.GetFile(path)
		json.Unmarshal(bytes, &m)
	}
	return m
}

func sanitizeAliasContent(alias string) string {
	alias = strings.TrimLeft(alias, " \t")
	if alias[len(alias)-1] != ' ' {
		alias += " "
	}

	return alias
}

func writeAliasOut(typeName string, aliases map[string]interface{}) {
	bytes, err := json.Marshal(aliases)
	if err != nil {
		tics.ThrowSys(writeAliasOut, err)
	}

	if d, ok := confMap[dataDir]; ok {
		path := d + "/" + typeName
		err = os.WriteFile(path, bytes, tics.Perm)
		if err != nil {
			tics.ThrowSys(writeAliasOut, err)
		}

		cats.RandomCat()

	} else {
		tics.ThrowSys(writeAliasOut, fmt.Errorf("failure in config mapping"))
	}
}

func selectAlias(action, colorT string, aliases map[string]interface{}) string {
	keys := serials.FmtStrKeys(aliases)
	sort.Strings(keys)
	chc := tics.SelectBetween(
		fmt.Sprintf("alias to %v from %v? > ", action, colorT), keys,
	)

	return chc
}

func checkArgs(args []string, funcName string) string {
	if len(args) == 0 {
		s := fmt.Sprintf("`%v` needs a selector:", funcName)
		choice := tics.SelectBetween(s, valCrudArgs)
		return choice
	} else {
		return args[0]
	}
}
