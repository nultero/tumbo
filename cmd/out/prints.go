package out

import (
	"fmt"
	"sort"
	"strconv"
	"strings"
	"tumbo/cmd/serials"

	"github.com/nultero/tics"
	"github.com/spf13/viper"
)

func PrintAll(dirPath string) {
	mapOfDir := tics.GetDirContentsExclusive(dirPath, tics.NotConfig)

	longest := 0
	for dn := range mapOfDir {
		if len(dn) > longest {
			longest = len(dn)
		}
	}

	sortedKeys := []string{}
	for key := range mapOfDir {
		sortedKeys = append(sortedKeys, key)
	}
	sort.Strings(sortedKeys)

	for _, k := range sortedKeys {
		printDirName(k, longest)
		if vals, ok := mapOfDir[k]; ok {
			js := tics.ToJson(vals)
			printTumboJson(js)
			fmt.Printf("\n")
		}
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
	s = tics.Make(s).Blue().String()
	fmt.Println(s)
}

func PrintDir(dirPath string) {
	dirNames := tics.GetDirFilesExclusive(dirPath, tics.NotConfig)
	fmt.Println(tics.Make("\\> Types of aliases:").Blue().String())
	for _, d := range dirNames {
		fmt.Println(" ", d)
	}
}

func PrintMatchingFileNames(dirPath, arg string) {
	fmt.Printf("Searching '%v' for types that match '%v': \n", dirPath, tics.Make(arg).Blue().String())
	dir := tics.SearchInDirNames(dirPath, arg)
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
		tics.Make(subStr).Blue().String(),
	)
}

func PrintMatchType(dirPath, arg string) {

	aliasTypes := tics.SearchInDirNames(dirPath, arg)

	switch len(aliasTypes) {
	case 0:
		printNoMatches("type", arg)

	case 1:
		printSingleFile(dirPath, aliasTypes[0])

	default:
		file := tics.SelectBetween("multiple matches: select", aliasTypes)
		printSingleFile(dirPath, file)
	}
}

func printNoMatches(kind, arg string) {
	fmt.Printf("\n\\> no %v matches found for '%v' \n", kind, arg)
}

func printTumboJson(js map[string]interface{}) {
	aliases := serials.FmtJsonToStrs(js)
	for _, ln := range aliases {
		fmt.Print(ln)
	}
}

func printSingleFile(dirPath, file string) {
	b := tics.GetFile(dirPath + "/" + file)
	js := tics.ToJson(b)

	printDirName(file, 0)
	printTumboJson(js)
}
