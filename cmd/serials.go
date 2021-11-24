package cmd

import (
	"encoding/json"

	"github.com/nultero/tics"
)

func toJson(i interface{}) map[string]interface{} {

	var j map[string]interface{}

	b, ok := i.([]byte)
	if ok {
		err := json.Unmarshal(b, &j)
		if err != nil {
			tics.ThrowSysDescriptor(tics.BlameFunc(toJson), err)
		}
	}

	return j
}
