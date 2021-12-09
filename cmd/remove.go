package cmd

import (
	"fmt"
	"sort"
	"tumbo/cmd/serials"

	"github.com/nultero/tics"
	"github.com/spf13/cobra"
)

// TODO remove cmd
var removeCmd = &cobra.Command{
	Use:   "remove",
	Short: "delete an alias, or an entire type of alias (requires prompt)",

	Args:      cobra.MaximumNArgs(1),
	ValidArgs: valCrudArgs,
	Run: func(cmd *cobra.Command, args []string) {
		removeAlias()
	},
}

func removeAlias() {
	aliasType := selectType()
	colorT := tics.Blue(aliasType)
	aliases := getJsonByType(aliasType)

	keys := serials.FmtStrKeys(aliases)

	sort.Strings(keys)

	chc := tics.SelectBetween(
		fmt.Sprintf("alias to remove from %v? > ", colorT), keys,
	)

	rmAlias := serials.Split(chc)

	js := map[string]interface{}{}
	for alias, cmds := range aliases {
		if alias != rmAlias {
			js[alias] = cmds
		}
	}

	writeAliasOut(aliasType, js)
}

func init() {
	rootCmd.AddCommand(removeCmd)
}
