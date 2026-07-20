import pickle
import json
import sys
import os
import base64
import argparse
arg_parser = argparse.ArgumentParser()
parser = arg_parser.parse_args()
path_modifications = '`path_modifications`'
serialization_mode = '`serialization_mode`'
state = '`state`'
deserializer = '`deserializer`'
func = '`func`'
function_post_processor = '`post_processor`'
cleanup = '`cleanup`'
func = pickle.loads(base64.b64decode(func))
res = func(*state['args'], **state['kwargs'])
cleanup = cleanup.strip()