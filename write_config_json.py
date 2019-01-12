import json

#data = {
#    "president": {
#        "name": "Zaphod Beeblebrox",
#        "species": "Betelgeusian"
#    }
#}
#
#with open("data_file.json", "w") as write_file:
#    json.dump(data, write_file)


ociVersion = "1.0.1-dev"

print(json.dumps({"c": 0, "b": 0, "a": 0}, sort_keys=True))
print(json.dumps({ociVersion}))

