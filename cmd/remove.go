package cmd

import (
	"fmt"

	"github.com/spf13/cobra"
)

var removeCmd = &cobra.Command{
	Use:   "remove",
	Short: "delete an alias, or an entire type of alias (requires prompt)",

	Args:      cobra.MaximumNArgs(1),
	ValidArgs: valCrudArgs,
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("remove called")
	},
}

func init() {
	rootCmd.AddCommand(removeCmd)
}
