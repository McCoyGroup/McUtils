
import pickle
import json
import sys
import os
import base64
import argparse

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("state", required=False, help="state", type=str, default=None)
arg_parser.add_argument("--paths", help="path modfications", type=str, default=None)
arg_parser.add_argument("--mode", help="serialization mode", type=str, default=None)
arg_parser.add_argument("--deserializer", type=str, default=None)
arg_parser.add_argument("--callable", type=str, default=None)
arg_parser.add_argument("--post", type=str, default=None)
arg_parser.add_argument("--cleanup", action=argparse.BooleanOptionalAction, default=None)
parser = arg_parser.parse_args()

# templated block
path_modifications = "`path_modifications`"
if parser.paths is not None:
    path_modifications = parser.paths
serialization_mode = "`serialization_mode`"
if parser.mode is not None:
    serialization_mode = parser.mode
state = """`state`"""
if parser.state is not None:
    state = parser.state
deserializer = """`deserializer`"""
if parser.deserializer is not None:
    deserializer = parser.deserializer
func = """`func`"""
if parser.callable is not None:
    callable = parser.callable
function_post_processor = """`post_processor`"""
if parser.post is not None:
    function_post_processor = parser.post
cleanup = """`cleanup`"""
if parser.cleanup is not None:
    if parser.cleanup:
        cleanup = "True"
    else:
        cleanup = "False"

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
if function_post_processor == 'print' and res is not None:
    print(res)
elif function_post_processor == 'none':
    ...
else:
    function_post_processor = pickle.loads(base64.b64decode(function_post_processor))
    function_post_processor(res)

cleanup = cleanup.strip()
if cleanup == "True":
    os.remove(sys.argv[0])