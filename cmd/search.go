package cmd

import (
	"encoding/json"
	"fmt"
	"os"
	"strings"

	"github.com/nultero/tics"
	"github.com/spf13/cobra"
)

var searchCmd = &cobra.Command{
	Use:   "search [string]",
	Short: "looks within aliases for matching terms",
	Args:  cobra.MaximumNArgs(1),
	Run:   search,
}

func search(cmd *cobra.Command, args []string) {
	if len(args) == 0 {
		fmt.Print("search for? > ")
		searchStr := tics.GetInput()
		args = append(args, searchStr)
	}
	arg := args[0]

	if d, ok := confMap[dataDir]; ok {

		if !TypeFlag {
			dir := tics.GetDirFilesExclusive(d, tics.NotConfig)
			for _, file := range dir {
				fileName := d + "/" + file
				searchWithin(fileName, file, arg)
			}

		} else { // TODO impl dir name search
			fmt.Println("search within dir names")
		}
	}
}

func searchWithin(fileName, shortName, arg string) {
	bytes, err := os.ReadFile(fileName)
	if err != nil {
		tics.ThrowSys(searchWithin, err)
	}

	aliasJson := map[string]interface{}{}
	aliases, cmds := []string{}, []string{}

	json.Unmarshal(bytes, &aliasJson)

	for al, cm := range aliasJson {
		if cmd, ok := cm.(string); ok {
			if strings.Contains(al, arg) || strings.Contains(cmd, arg) {
				aliases = append(aliases, al)
				cmds = append(cmds, cmd)
			}
		}
	}

	if len(aliases) > 0 {
		fmt.Printf("--- in %v:\n", tics.DarkBlue(shortName))
		maxLen := getMaxLen(&aliases)
		for i := range aliases {
			fmt.Printf(
				"%v%v%v\n",
				strings.ReplaceAll(aliases[i], arg, tics.Pink(arg)),
				strings.Repeat(" ", maxLen-len(aliases[i])),
				strings.ReplaceAll(cmds[i], arg, tics.Pink(arg)),
			)
		}
		fmt.Println("")
	}
}

func getMaxLen(strs *[]string) int {
	mx := 0
	for _, s := range *strs {
		if len(s) > mx {
			mx = len(s)
		}
	}
	return mx + 3
}

func init() {
	rootCmd.AddCommand(searchCmd)
	s := "makes '" + tics.Blue("search") + "' only search the alias types in Tumbo's dir"
	searchCmd.Flags().BoolVarP(&TypeFlag, "type", "t", false, s)
}
