package cmd

import (
	"fmt"

	"github.com/spf13/cobra"
)

var newCmd = &cobra.Command{
	Use:   "new [alias, type]",
	Short: "create a new alias or type of alias",

	Args:      cobra.OnlyValidArgs,
	ValidArgs: valCrudArgs,
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("new called")
	},
}

func init() {
	rootCmd.AddCommand(newCmd)
}
