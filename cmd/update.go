package cmd

import (
	"fmt"
	"tumbo/cmd/serials"

	"github.com/nultero/tics"
	"github.com/spf13/cobra"
)

// TODO update type cmd
var updateCmd = &cobra.Command{
	Use:   "update",
	Short: "change any value of an alias, or rename a type of alias",

	Args:      cobra.MaximumNArgs(1),
	ValidArgs: valCrudArgs,
	Run: func(cmd *cobra.Command, args []string) {

		arg := checkArgs(args, "update")

		if arg == valCrudArgs[0] {
			updateAlias()

		} else if arg == valCrudArgs[1] {
			fmt.Println("arg:", valCrudArgs[1])
		}
	},
}

func updateAlias() {
	aliasType := selectType()
	colorT := tics.Make(aliasType).Blue().String()
	aliases := getJsonByType(aliasType)

	choice := selectAlias("update", colorT, aliases)
	alias := serials.Split(choice)

	fmt.Print("updated alias shorthand? (ENTER to keep current) > ")
	updtAlias := tics.GetInput()

	if len(updtAlias) == 0 {
		updtAlias = alias
	}

	fmt.Print("updated alias content? (ENTER to keep current) > ")
	aliasContent := tics.GetInput()

	keepValFlag := false
	if len(aliasContent) == 0 {
		keepValFlag = true
	} else {
		aliasContent = sanitizeAliasContent(aliasContent)
	}

	js := map[string]interface{}{}
	for al, cmd := range aliases {
		if al != alias {
			js[al] = cmd

		} else {
			if keepValFlag {
				js[updtAlias] = cmd

			} else {
				js[updtAlias] = aliasContent
			}
		}
	}

	writeAliasOut(aliasType, js)
}

func init() {
	rootCmd.AddCommand(updateCmd)

	// TODO  ? update config flag, so that it can be called to change conf
}
