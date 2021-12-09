package cmd

import (
	"encoding/json"
	"fmt"
	"os"
	"strings"
	"tumbo/cmd/cats"

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
