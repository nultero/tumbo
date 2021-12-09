package cmd

import (
	"fmt"

	"github.com/spf13/cobra"
)

// TODO update cmd
var updateCmd = &cobra.Command{
	Use:   "update",
	Short: "change any value of an alias, or rename a type of alias",

	Args:      cobra.MaximumNArgs(1),
	ValidArgs: valCrudArgs,
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("update called")
	},
}

func init() {
	rootCmd.AddCommand(updateCmd)

	// TODO  ? update config flag, so that it can be called to change conf
}
