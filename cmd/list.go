package cmd

import (
	"tumbo/cmd/out"

	"github.com/nultero/tics"
	"github.com/spf13/cobra"
)

var listCmd = &cobra.Command{
	Use:   "list " + tics.Make("{string} (optional)").Blue().String(),
	Short: "show given aliases / alias types",

	Args: cobra.MaximumNArgs(1), //TODO clean up this jank
	ValidArgsFunction: func(cmd *cobra.Command, args []string, toComplete string) ([]string, cobra.ShellCompDirective) {
		if len(args) != 0 {
			return nil, cobra.ShellCompDirectiveNoFileComp
		}

		s := []string{}
		if d, ok := confMap[dataDir]; ok {
			s = append(s, tics.GetDirFilesExclusive(d, tics.NotConfig)...)
		}

		return s, cobra.ShellCompDirectiveNoFileComp
	},

	Run: func(cmd *cobra.Command, args []string) {

		if d, ok := confMap[dataDir]; ok {

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
	s := "makes '" +
		tics.Make("list").Blue().String() +
		"' only print the alias types in Tumbo's dir"
	listCmd.Flags().BoolVarP(&TypeFlag, "type", "t", false, s)
}
