import requests
import json

metadata_url = 'http://169.254.169.254/latest/'

#download the data from AWS
def expand_tree(url, arr):
    output = {}
    for item in arr:
        new_url = url + item
        r = requests.get(new_url)
        text = r.text
        if item[-1] == "/":
            list_of_values = r.text.splitlines()
            output[item[:-1]] = expand_tree(new_url, list_of_values)
        elif is_json(text):
            output[item] = json.loads(text)
        else:
            output[item] = text
    return output

#To Initiate the process.
def get_metadata():
    initial = ["meta-data/"]
    result = expand_tree(metadata_url, initial)
    return result

#Capture the data to JSON
def get_metadata_json():
    metadata = get_metadata()
    metadata_json = json.dumps(metadata, indent=4, sort_keys=True)
    return metadata_json

#Verify the JSON format
def is_json(myjson):
    try:
        json.loads(myjson)
    except ValueError:
        return False
    return True

#Convert the data to Dictionary
def gen_dict_extract(key, var):
    if hasattr(var, 'items'):
        for k, v in var.items():
            if k == key:
                yield v
            if isinstance(v, dict):
                for result in gen_dict_extract(key, v):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in gen_dict_extract(key, d):
                        yield result

#Find the Value to key
def find_key(key):
    metadata = get_metadata()
    return list(gen_dict_extract(key, metadata))


if __name__ == '__main__':
    print(get_metadata_json())
    key = input("What key would you like to find?\n")
    print(find_key(key))