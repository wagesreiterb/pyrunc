# from jsonschema import Draft4Validator
from jsonschema import validate, RefResolver
import json
import os


with open('schema/config-schema.json') as f:
    schema = json.load(f)
# Bugfix in jsonschema
# https://github.com/Julian/jsonschema/issues/313
schema_dir = os.path.dirname(os.path.abspath('schema/config-schema.json'))
resolver = RefResolver(base_uri='file://' + schema_dir + '/', referrer=schema)
# validate(obj, schema, resolver = resolver)


# https://stackoverflow.com/questions/30095032/nameerror-name-true-is-not-defined
true = True
false = False


with open('tmp/config.json') as f:
    config = json.load(f)

validate(instance=config, schema=schema, resolver=resolver)


# Todo: schemas shall point to github not locally
# "windows": {
#     "$ref": "config-windows.json#/windows"
# },
# "vm": {
#     "$ref": "https://raw.githubusercontent.com/opencontainers/runtime-spec/master/schema/config-vm.json#/vm"
