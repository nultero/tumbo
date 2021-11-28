package serials

import (
	"encoding/json"

	"github.com/nultero/tics"
)

func ToJson(i interface{}) map[string]interface{} {

	var j map[string]interface{}

	b, ok := i.([]byte)
	if ok {
		err := json.Unmarshal(b, &j)
		if err != nil {
			tics.ThrowSys(ToJson, err)
		}
	}

	return j
}
