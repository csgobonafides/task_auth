import json

bl_list = {
    "assens": [],
    "refresh": []
    }

def exit_list():
    with open('black_list.json', 'w') as fl:
        json.dump(bl_list, fl)

def open_list():
    with open('black_list.json', 'r') as file:
        # a = file.read()
        global bl_list
        bl_list = json.load(file)