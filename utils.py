import json


def o_save(obj, path):
    with open(path, 'w', encoding='utf8') as f: 
        json.dump(obj, fp=f, ensure_ascii=False, indent=2)


def o_load(path):
    with open(path, 'r', encoding='utf8') as f: 
        return json.load(f)