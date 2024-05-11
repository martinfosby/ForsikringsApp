import json 

def json_resource():
    try:
        with open('res/strings_res.json') as f:
            json_strings = json.load(f)
    except FileNotFoundError:
        # testing only
        with open('flask_app/res/strings_res.json') as f:
            json_strings = json.load(f)
    return json_strings

def string_resource(key: str, *args, **kwargs) -> str:
    try:
        string: str = json_resource()[key]
        if args or kwargs:
            string =string.format(*args, **kwargs)
        return string
    except KeyError as e:
        return key
