package cmd

import (
	"fmt"
	"tumbo/cmd/cats"

	"github.com/nultero/tics"
	"github.com/spf13/cobra"

	"github.com/spf13/viper"
)

var cfgFile string
var flavorText = tics.Blue(cats.TumboHat())

var confMap = map[string]string{
	"confFile": "$USER/.config/tumbo/tumbo.yaml",
	"dataDir":  "$USER/.config/tumbo",
}

var defaultSettings = []string{
	"shell flavor: 'bash'",
	"dashes in dir: 20",
}

var valCrudArgs = []string{"alias", "type"}

var rootCmd = &cobra.Command{
	Use:   "tumbo",
	Short: "an alias manager that wears hats\n" + flavorText,

	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println(cats.TumboNoArgs())
		fmt.Println("\n  (run '-h' or '--help' to see opts)")
	},
}

func init() {
	cobra.OnInitialize(initConfig)
	rootCmd.PersistentFlags().StringVar(&cfgFile, "config", "", "config file (default is $HOME/.config/tumbo/tumbo.yaml)")
}

func initConfig() {

	confMap = tics.CobraRootInitBoilerPlate(confMap, true)
	confPath := confMap["confFile"]
	viper.SetConfigFile(confPath)
	viper.AutomaticEnv()

	// If a config file is found, read it in, else make one with prompt.
	err := viper.ReadInConfig()
	if err != nil {

		// TODO replace $SHELL in defaults
		// actually, that's already an env
		// maybe just slice shell from env?

		tics.RunConfPrompts("tumbo", confMap, defaultSettings)
		tics.ThrowQuiet("")
	}
}

func Execute() {
	cobra.CheckErr(rootCmd.Execute())
}
