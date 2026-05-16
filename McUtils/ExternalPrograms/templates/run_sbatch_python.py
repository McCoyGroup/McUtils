
import pickle
import json
import sys
import os
import base64
import argparse

# templated block
path_modifications = "`path_modifications`"
serialization_mode = "`serialization_mode`"
state = """`state`"""
deserializer = """`deserializer`"""
func = """`func`"""
function_post_processor = """`post_processor`"""

for p in path_modifications.split(","):
    sys.path.insert(0, p.strip())


if serialization_mode == "mcutils":
    from McUtils.Scaffolding import BaseSerializer
    deserializer = BaseSerializer.construct(deserializer)
    state = deserializer.loads(state)
else:
    deserializer = pickle.loads(base64.b64decode(state))
    state = deserializer(state)

func = pickle.loads(base64.b64decode(func))

res = func(*state["args"], **state["kwargs"])
if function_post_processor == 'print':
    print(res)
elif function_post_processor == 'none':
    ...
else:
    function_post_processor = pickle.loads(base64.b64decode(function_post_processor))
    function_post_processor(res)