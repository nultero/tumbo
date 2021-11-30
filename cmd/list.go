package cmd

import (
	"tumbo/cmd/out"

	"github.com/nultero/tics"
	"github.com/spf13/cobra"
)

var TypeFlag bool

var listCmd = &cobra.Command{
	Use:   "list {string}",
	Short: "show given aliases / alias types",

	Args: cobra.MaximumNArgs(1),
	Run: func(cmd *cobra.Command, args []string) {

		if d, ok := confMap["dataDir"]; ok {

			if len(args) == 0 {
				if TypeFlag {
					out.PrintDir(d)

				} else {
					out.PrintAll(d)
				}

			} else {
				if TypeFlag {
					out.PrintMatchingFileNames(d, args[0])

				} else {
					out.PrintMatchType(d, args[0])
				}
			}
		}
	},
}

func init() {
	rootCmd.AddCommand(listCmd)
	s := "makes '" + tics.Blue("list") + "' only print the alias types in Tumbo's dir"
	listCmd.Flags().BoolVarP(&TypeFlag, "type", "t", false, s)
}
