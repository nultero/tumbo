package out

import (
	"fmt"
	"strconv"
	"strings"
	"tumbo/cmd/dir"
	"tumbo/cmd/serials"

	"github.com/nultero/tics"
	"github.com/spf13/viper"
)

func PrintAll(dirPath string) {
	mapOfDir := dir.GetDirContents(dirPath)

	longest := 0
	for dn := range mapOfDir {
		if len(dn) > longest {
			longest = len(dn)
		}
	}

	for dn, vals := range mapOfDir {
		printDirName(dn, longest)
		js := serials.ToJson(vals)
		printTumboJson(js)
		fmt.Printf("\n")
	}
}

func printDirName(dn string, ln int) {
	dashes, err := strconv.Atoi(viper.GetString("dashes in dir"))
	if err != nil {
		tics.ThrowSys(printDirName, err)
	}

	dashes -= len(dn) - ln

	if dashes < 0 {
		dashes = 0
	}

	s := "\\> " + dn + " " + strings.Repeat("-", dashes) + "\n"
	s = tics.MakeT(s).Blue().Str()
	fmt.Println(s)
}

func PrintDir(dirPath string) {
	dirNames := dir.GetDirFiles(dirPath)
	fmt.Println(tics.Blue("\\> Types of aliases:"))
	for _, d := range dirNames {
		fmt.Println(" ", d)
	}
}

func PrintMatchingFileNames(dirPath, arg string) {
	fmt.Printf("Searching '%v' for types that match '%v': \n", dirPath, tics.Blue(arg))
	dir := dir.SearchInDirNames(dirPath, arg)
	if len(dir) == 0 {
		printNoMatches("type", arg)

	} else {
		for _, d := range dir {
			fmt.Println(subStrFmt(d, arg))
		}
	}
}

func subStrFmt(s, subStr string) string {
	return strings.ReplaceAll(
		s, subStr,
		tics.Blue(subStr),
	)
}

func PrintMatchType(dirPath, arg string) {

	aliasTypes := dir.SearchInDirNames(dirPath, arg)

	switch len(aliasTypes) {
	case 0:
		printNoMatches("type", arg)

	case 1:
		fmt.Println("successful print")

	default:
		fmt.Println("select from different opts")
	}
}

func printNoMatches(kind, arg string) {
	fmt.Printf("\n\\> no %v matches found for '%v' \n", kind, arg)
}

func printTumboJson(js map[string]interface{}) {
	maxLen := 0
	for alias := range js {
		if len(alias) > maxLen {
			maxLen = len(alias)
		}
	}
	maxLen += 3

	for alias, cmds := range js {
		fmt.Printf(
			"  %v%v%v\n",
			tics.Bold(alias),
			strings.Repeat(" ", maxLen-len(alias)),
			cmds,
		)
	}
}

func printSingleFile(path string) {

}
