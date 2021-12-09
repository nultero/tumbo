package cmd

import (
	"encoding/json"
	"fmt"
	"os"
	"strings"
	"tumbo/cmd/cats"

	"github.com/nultero/tics"
	"github.com/spf13/cobra"
	"github.com/spf13/viper"
)

// TODO source for AFTER shell
var sourceCmd = &cobra.Command{
	Use:   "source",
	Short: "bake all aliases into a file and write to $HOME/<shell>_aliases",

	Args: cobra.NoArgs,
	Run: func(cmd *cobra.Command, args []string) {
		writeAliases()
	},
}

func unmarshalJsToStr(bytes []byte) string {
	m := map[string]interface{}{}
	json.Unmarshal(bytes, &m)

	s := ""
	for alias, cont := range m {
		s += fmt.Sprintf(`alias %v="%v"%v`, alias, cont, "\n")
	}
	s += "\n\n"
	return s
}

func writeAliases() {

	mainStr := ""

	if d, ok := confMap[dataDir]; ok {
		aliases := tics.GetDirContentsExclusive(d, tics.NotConfig)
		for k, v := range aliases {
			if bytes, ok := v.([]byte); ok {
				mainStr += fmt.Sprintf("## %v ##\n", k)
				mainStr += unmarshalJsToStr(bytes)

			} else {
				tics.ThrowSys(writeAliases, fmt.Errorf("file formatting issue at `%v`", k))
			}
		}
	}

	mainStr = strings.TrimRight(mainStr, " \n")
	p := getPath()

	bytes := []byte(mainStr)
	err := os.WriteFile(p, bytes, tics.Perm)
	if err != nil {
		tics.ThrowSys(writeAliases, err)
	}

	cats.RandomCat()
}

func getHome() string {
	h, err := os.UserHomeDir()
	if err != nil {
		tics.ThrowSys(getHome, err)
	}

	return h
}

func getPath() string {
	shell := viper.GetString("shell flavor")
	path := getHome() + "/." + shell + "_aliases"
	return path
}

func init() {
	rootCmd.AddCommand(sourceCmd)
}
