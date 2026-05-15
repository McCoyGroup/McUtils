
import pickle
import json
import sys
import os
import base64

path_modifications = `path_modifications`
for p in path_modifications:
    sys.path.insert(0, p)

serialization_mode = "`serialization_mode`"
state = """`state`"""
deserializer = """`deserializer`"""
if serialization_mode == "mcutils":
    from McUtils.Scaffolding import BaseSerializer
    deserializer = BaseSerializer.construct(deserializer)
    state = deserializer.loads(state)
else:
    deserializer = pickle.loads(base64.b64decode(state))
    state = deserializer(state)

func = pickle.loads(base64.b64decode("""`func`"""))

res = func(*state["args"], **state["kwargs"])

function_post_processor = "`post_processor`"
if function_post_processor == 'print':
    print(res)
elif function_post_processor == 'none':
    ...
else:
    function_post_processor = pickle.loads(base64.b64decode(function_post_processor))
    function_post_processor(res)