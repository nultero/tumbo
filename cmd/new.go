package cmd

import (
	"fmt"

	"github.com/nultero/tics"
	"github.com/spf13/cobra"
)

// TODO -- new type cmd
var newCmd = &cobra.Command{
	Use:   "new [alias, type]",
	Short: "create a new alias or type of alias",

	Args:      cobra.MaximumNArgs(1),
	ValidArgs: valCrudArgs,
	Run: func(cmd *cobra.Command, args []string) {

		arg := checkArgs(args, "new")

		if arg == valCrudArgs[0] {
			newAlias()

		} else if arg == valCrudArgs[1] {
			fmt.Println("arg:", valCrudArgs[1])
		}
	},
}

func newAlias() {
	aliasType := selectType()
	colorT := tics.Blue(aliasType)
	fmt.Printf("alias to implement in %v? > ", colorT)
	alias := tics.GetInput()

	if len(alias) == 0 {
		tics.ThrowQuiet("new aliases must be at least 1 letter long")
	}

	aliases := getJsonByType(aliasType)

	if _, ok := aliases[alias]; ok {
		s := fmt.Sprintf(
			"alias `%v` found in aliases, update anyway? [ y / N ] : ",
			tics.Bold(alias))

		if !tics.Confirmed(s) {
			tics.ThrowQuiet("")
		}
	}

	fmt.Printf("what should %v be aliased to? > ", tics.Blue(alias))
	aliasContent := tics.GetInput()
	aliasContent = sanitizeAliasContent(aliasContent)

	aliases[alias] = aliasContent
	writeAliasOut(aliasType, aliases)
}

func init() {
	rootCmd.AddCommand(newCmd)
}
