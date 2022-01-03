package cats

import (
	"fmt"
	"math/rand"
	"time"

	"github.com/nultero/tics"
)

var tumboEars = "\n     /^__^\\\n"
var tumboBody = []string{
	"    / .  . \\",
	"   /        \\",
	"  /  \\/  \\/  \\",
	"  \\__________/",
}

var hat = []string{
	"\n     _____  ",
	"    |     |",
	" ___|_____|___",
}

func loopOver(tumboPart []string) string {
	s := ""
	for _, v := range tumboPart {
		s += v + "\n"
	}
	return s
}

// Returns a str of the fat cat.
func TumboCat() string {
	return tumboEars + loopOver(tumboBody)
}

// Returns Tumbo pointing his finger accusingly.
func TumboNoArgs() string {
	finger := tics.Make("\u261E  no args given to Tumbo").Red().String()
	return "\n     /^__^\\\n" +
		"    / .  . \\\n" +
		"   /        \\" + finger + "\n" +
		"  /  \\/      \\\n" +
		"  \\__________/"
}

// Returns Tumbo with the stovepipe on.
func TumboHat() string {
	return loopOver(hat) + loopOver(tumboBody)
}

func RandomCat() {

	// if no seed is selected, the rand values below
	// become deterministic... very boring
	rand.Seed(time.Now().UnixNano())

	funcs := []func() string{
		TumboCat,
		TumboHat,
	}

	i := rand.Intn(len(funcs))
	f := funcs[i]
	s := f()
	fmt.Println("\n", s)
}
