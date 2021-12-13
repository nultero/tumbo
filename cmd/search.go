package cmd

import (
	"encoding/json"
	"fmt"
	"strings"
	"tumbo/cmd/serials"

	"github.com/nultero/tics"
	"github.com/spf13/cobra"
)

//TODO search
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

	matches := map[string]interface{}{}

	if d, ok := confMap[dataDir]; ok {
		if !TypeFlag {
			dirMap := tics.GetDirContentsExclusive(d, tics.NotConfig)
			for _, file := range dirMap {
				searchWithinI(&arg, file, matches)
			}

		} else { // TODO impl dir name search
			fmt.Println("search within dir names")
		}
	}

	strs := serials.FmtStrsForSearch(matches)
	for _, s := range strs {
		s = strings.ReplaceAll(s, arg, tics.Pink(arg))
		fmt.Println(s)
	}
}

func searchWithinI(arg *string, i interface{}, matches map[string]interface{}) {
	bytes, ok := i.([]byte)
	if ok {
		js := map[string]interface{}{}
		json.Unmarshal(bytes, &js)

		for alias, cmds := range js {
			c, okok := cmds.(string)
			if okok {
				if strings.Contains(alias, *arg) || strings.Contains(c, *arg) {
					matches[alias] = c
				}
			}
		}
	}
}

func init() {
	rootCmd.AddCommand(searchCmd)
	s := "makes '" + tics.Blue("search") + "' only search the alias types in Tumbo's dir"
	searchCmd.Flags().BoolVarP(&TypeFlag, "type", "t", false, s)
}
