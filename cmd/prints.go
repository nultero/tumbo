package cmd

import (
	"fmt"
	"strconv"
	"strings"
	"tumbo/cmd/dir"

	"github.com/nultero/tics"
	"github.com/spf13/viper"
)

func printAll(rootDir string) {
	mapOfDir := dir.GetDirContents(rootDir)

	longest := 0
	for dn := range mapOfDir {
		if len(dn) > longest {
			longest = len(dn)
		}
	}

	for dn, vals := range mapOfDir {
		printDirName(dn, longest)
		js := toJson(vals)

		for alias, cmds := range js {
			fmt.Println("  ", alias, cmds)
		}

		fmt.Printf("\n")
	}

}

func printDirName(dn string, ln int) {
	dashes, err := strconv.Atoi(viper.GetString("dashes in dir"))
	if err != nil {
		tics.ThrowSysDescriptor(tics.BlameFunc(printDirName), err)
	}

	dashes -= len(dn) - ln

	if dashes < 0 {
		dashes = 0
	}

	s := "\\> " + dn + " " + strings.Repeat("-", dashes) + "\n"
	s = tics.MakeT(s).Blue().Str()
	fmt.Println(s)
}
