import sys
from nbt import nbt
import os
import json


class PlayerGrabber:
    complex_tag_types = [
        nbt.TAG_LIST,
        nbt.TAG_COMPOUND
    ]

    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file


    def process_data(self):
        """
        Main method to process the NBT data from the input file
        and save it to the output file.
        """
        try:
            nbtfile = nbt.NBTFile(self.input_file)
            self.write_new_data(nbtfile, self.output_file)
            print(f"Successfully processed {self.input_file} into {self.output_file}")
        except Exception as e:
            print(f"An error occurred while processing: {e}")


    def get_data(self, item):
        """
        Recursively extracts data from the NBT structure into a dictionary.
        """
        if item.id in self.complex_tag_types:
            if item.id == nbt.TAG_LIST:
                children = []
                for child in item.tags:
                    children.append(self.get_data(child))
            else:  # TAG_COMPOUND
                children = {}
                for child in item.tags:
                    children[child.name] = self.get_data(child)
        else:
            children = item.value
        return children


    def write_new_data(self, tag, filename="./output_data/test.json"):
        """
        Converts the NBT data to JSON format and writes it to a file.
        """
        json_data = self.get_data(tag)
        self.write_playerdata(filename, json_data)


    def write_playerdata(self, filename, data={}):
        """
        Writes the processed player data to a file in JSON format.
        """
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w") as file_handler:
            json.dump(data, file_handler, indent=4)
        print(f"Playerdata successfully saved to {filename}")




# Now called in MinecraftStatsHandler.py
if __name__ == "__main__":
    # Update paths to use relative locations in './output_data'
    input_file = "../world/playerdata/adc76802-d75c-4143-89a6-ede25720ecce.dat"
    output_file = "./output_data/playerdata/playerdata_adc76802-d75c-4143-89a6-ede25720ecce.json"
    handler = PlayerGrabber(input_file, output_file)
    handler.process_data()
