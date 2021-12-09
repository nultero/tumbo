package cmd

import (
	"fmt"
	"strings"
	"tumbo/cmd/cats"

	"github.com/nultero/tics"
	"github.com/spf13/cobra"

	"github.com/spf13/viper"
)

var cfgFile string
var flavorText = tics.Blue(cats.TumboHat())

var TypeFlag bool = false

var dataDir = "dataDir"
var confFile = "confFile"

var confMap = map[string]string{
	confFile: "$USER/.config/tumbo/tumbo.yaml",
	dataDir:  "$USER/.config/tumbo",
}

var defaultSettings = []string{
	"shell flavor: 'bash'", // this default is overridden below, on initializing config
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
		defaultSettings[0] = strings.ReplaceAll(defaultSettings[0], "bash", getShellEnv())

		tics.RunConfPrompts("tumbo", confMap, defaultSettings)
		tics.ThrowQuiet("") // exits so that run won't be contaminated by not having conf
	}
}

func Execute() {
	cobra.CheckErr(rootCmd.Execute())
}

func getShellEnv() string {
	shellPath := viper.GetString("SHELL")
	spl := strings.Split(shellPath, "/")
	shell := spl[len(spl)-1]
	return shell
}
