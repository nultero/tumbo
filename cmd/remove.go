package cmd

import (
	"fmt"
	"tumbo/cmd/serials"

	"github.com/nultero/tics"
	"github.com/spf13/cobra"
)

// TODO remove w/ type parameter, and all the checks after
var removeCmd = &cobra.Command{
	Use:   "remove",
	Short: "delete an alias, or an entire type of alias (requires prompt)",

	Args:      cobra.MaximumNArgs(1),
	ValidArgs: valCrudArgs,
	Run: func(cmd *cobra.Command, args []string) {

		if args[0] == valCrudArgs[0] {
			removeAlias()

		} else if args[0] == valCrudArgs[1] {
			fmt.Println("arg:", valCrudArgs[1])
		}
	},
}

func removeAlias() {
	aliasType := selectType()
	colorT := tics.Blue(aliasType)
	aliases := getJsonByType(aliasType)
	choice := selectAlias("remove", colorT, aliases)

	rmAlias := serials.Split(choice)

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
