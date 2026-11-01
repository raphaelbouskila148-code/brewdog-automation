import json


def get_data(name):
    file = open("data/test_data.json")
    data = json.load(file)
    file.close()
    return data[name]
