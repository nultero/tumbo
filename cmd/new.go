package cmd

import (
	"fmt"
	"os"

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
			newType()
		}
	},
}

func newAlias() {
	aliasType := selectType()
	colorT := tics.Make(aliasType).Blue().String()
	fmt.Printf("alias to implement in %v? > ", colorT)
	alias := tics.GetInput()

	if len(alias) == 0 {
		tics.ThrowQuiet("new aliases must be at least 1 letter long")
	}

	aliases := getJsonByType(aliasType)

	if _, ok := aliases[alias]; ok {
		s := fmt.Sprintf(
			"alias `%v` found in aliases, update anyway? [ y / N ] : ",
			tics.Make(alias).Bold().String())

		if !tics.Confirmed(s) {
			tics.ThrowQuiet("")
		}
	}

	fmt.Printf("what should %v be aliased to? > ", tics.Make(alias).Blue().String())
	aliasContent := tics.GetInput()
	aliasContent = sanitizeAliasContent(aliasContent)

	aliases[alias] = aliasContent
	writeAliasOut(aliasType, aliases)
}

func newType() {
	fmt.Print("new alias type name? > ")
	typeName := tics.GetInput()

	if len(typeName) == 0 {
		tics.ThrowQuiet("new alias types must be at least 1 letter long")
	}

	if d, ok := confMap[dataDir]; ok {

		// check new name does not clash w/ existing one
		posConflicts := tics.SearchInDirNames(d, typeName)
		if len(posConflicts) > 0 {
			for _, existingName := range posConflicts {
				if typeName == existingName {
					tics.ThrowQuiet(tics.Make("this type name already exists").DarkBlue().String())
				}
			}
		}

		// all good, make new type
		path := d + "/" + typeName
		err := os.WriteFile(path, []byte("{}"), tics.Perm)
		if err != nil {
			tics.ThrowSys(newType, err)
		}

		fmt.Println("created blank type " + tics.Make(typeName).Blue().String())
	}
}

func init() {
	rootCmd.AddCommand(newCmd)
}
