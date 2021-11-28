package dir

import (
	"io/fs"
	"io/ioutil"
	"os"
	"strings"

	"github.com/nultero/tics"
)

func getDir(path string) []fs.FileInfo {
	f, err := ioutil.ReadDir(path)
	if err != nil {
		tics.ThrowSys(getDir, err)
	}

	return f
}

func getFile(path string) []byte {
	b, err := os.ReadFile(path)
	if err != nil {
		tics.ThrowSys(getFile, err)
	}

	return b
}

func GetDirFiles(path string) []string {
	files := []string{}
	dir := getDir(path)
	for _, file := range dir {
		if notConfig(file.Name()) {
			files = append(files, file.Name())
		}
	}

	return files
}

// func getFromDir(dirName, fileName string) {
// 	fmt.Println("placeholder")
// }

func GetDirContents(dirName string) map[string]interface{} {
	m := map[string]interface{}{}
	dir := getDir(dirName)

	for _, file := range dir {
		if notConfig(file.Name()) {
			p := dirName + "/" + file.Name()
			m[file.Name()] = getFile(p)
		}
	}

	return m
}

func notConfig(name string) bool {
	if len(name) > 4 {
		return name[len(name)-4:] != "yaml"
	}

	return true
}

func SearchInDirNames(dirPath, searchStr string) []string {
	dir := GetDirFiles(dirPath)
	matches := []string{}
	for _, d := range dir {
		if strings.Contains(d, searchStr) {
			matches = append(matches, d)
		}
	}

	return matches
}
