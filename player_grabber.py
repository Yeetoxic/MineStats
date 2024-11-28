

import sys
from nbt import nbt
import os
import json

complex_tag_types = [
    nbt.TAG_LIST,
    nbt.TAG_COMPOUND
]

def main(read_file, write_file):
    nbtfile = nbt.NBTFile(read_file)
    # read and/or set tags
    write_new_data(nbtfile, filename=write_file)
    return 0

#recursively gets data into a root dict
def get_data(item):
    if item.id in complex_tag_types:
        if item.id == nbt.TAG_LIST:
            children = []
            for child in item.tags:
                children.append(get_data(child))
        else:
            children = {}
            for child in item.tags:
                children[child.name] = get_data(child)
    else:
        children = item.value
    return children

#gets and saves data to the given file
def write_new_data(tag, filename = "./test.json"):
    json_data = get_data(tag)
    write_playerdata(filename, json_data)

#puts playerdata in the file
def write_playerdata(filename, data={}):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w") as file_handler:
            json.dump(data, file_handler, indent=4)
        print(f"playerdata successfully saved to {filename}")

if __name__ == "__main__":
    sys.exit(main(f".\\TeamCreeper-own\\playerdata\\52b3b7ca-1a0b-4f6f-9b8c-db92a833dc79.dat", f".\\TeamCreeper-own\\output_data\\some.json"))

