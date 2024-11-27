import os
import requests

username_map = {}

class MojangAPIGrabber:
    global username_map

    def __init__(self, uuid):
        self.uuid = uuid
        self.username = "notch"
        self.folder = os.listdir("playerdata") #TEMP DATA
        self.MojangAPI_URL = f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}"
        self.MineskinAPI_URL = f"https://mineskin.eu/helm/{self.username}/100.png"
        

    def get_minecraft_usernames(self):
        """
        Fetches the username history for a given Minecraft UUID using Mojang's API.

        Args:
            uuid (str): The UUID of the Minecraft user.

        Returns:
            list: A list of username history, or an error message if the UUID is invalid.
        """
        print(f"Debug: Requesting URL: {self.MojangAPI_URL}")  # Debugging
        try:
            response = requests.get(self.MojangAPI_URL)
            print(f"Debug: Response Status Code: {response.status_code}")  # Debugging
            if response.status_code == 200:
                name = response.json()
                self.username = name['name']
                username_map[self.uuid] = name['name']
                return name
            elif response.status_code == 404:
                return "Error: UUID not found. Check if the UUID is correct."
            elif response.status_code == 204:
                return "No content found. The UUID might not exist."
            else:
                return f"Error: {response.status_code} - {response.reason}"
        except requests.exceptions.RequestException as e:
            return f"An error occurred: {e}"
        

    def get_minecraft_skins(self):
        print(f"Debug: Requesting URL: {self.MineskinAPI_URL}")  # Debugging
        try:
            # Head of skin
            self.MineskinAPI_URL = f"https://mineskin.eu/helm/{self.username}/100.png"
            response = requests.get(self.MineskinAPI_URL)
            output_file = f"./skins/{self.username}_head.png"


            print(f"Debug: Response Status Code: {response.status_code}")  # Debugging
            if response.status_code == 200:
                with open(output_file, "wb") as file:
                    file.write(response.content)
                print(f"Image successfully saved as {output_file}")

            # Whole of skin
            self.MineskinAPI_URL = f"https://mineskin.eu/skin/{self.username}"
            response = requests.get(self.MineskinAPI_URL)
            output_file = f"./skins/{self.username}.png"

            print(f"Debug: Response Status Code: {response.status_code}")  # Debugging
            if response.status_code == 200:
                with open(output_file, "wb") as file:
                    file.write(response.content)
                print(f"Image successfully saved as {output_file}")



            elif response.status_code == 404:
                return "Error: UUID not found. Check if the UUID is correct."
            elif response.status_code == 204:
                return "No content found. The UUID might not exist."
            else:
                return f"Error: {response.status_code} - {response.reason}"
        except requests.exceptions.RequestException as e:
            return f"An error occurred: {e}"


    def read_playerdata(self):
        self.folder = [file.split(".")[0] for file in self.folder]
        for i in self.folder:
            if i in self.folder:
                self.folder.remove(i)
        return self.folder
    

    def write_playerdata(self):
        output_file = f"./output_data/usernames.json"
        with open(output_file, 'w') as file_handler:
            file_handler.write("{\"stuff\" :[\n")
            
            file_handler.write("\t{\"usermap\" :[{\n")
            count = len(username_map.keys())
            for key in username_map.keys():
                count -=1
                file_handler.write(f'\t\t"{key}": ')
                file_handler.write(f'"{username_map[key]}"')
                if count > 0:
                    file_handler.write(",\n")
                else:
                    file_handler.write("\n")
            file_handler.write("\t}]},\n")
            
            file_handler.write("\t{\"uuids\" :[\n")
            count = len(username_map.keys())
            for key in username_map.keys():
                count -=1
                file_handler.write(f'\t\t"{key}"')
                if count > 0:
                    file_handler.write(",\n")
                else:
                    file_handler.write("\n")
            file_handler.write("\t]},\n")

            file_handler.write("\t{\"usernames\" :[\n")
            count = len(username_map.keys())
            for key in username_map.keys():
                count -=1
                file_handler.write(f'\t\t"{username_map[key]}"')
                if count > 0:
                    file_handler.write(",\n")
                else:
                    file_handler.write("\n")
            file_handler.write("\t]}\n")
            
            file_handler.write("]}")

        print(username_map)
            
    

# Example usage
if __name__ == "__main__":
    uuid = None
    dummy = MojangAPIGrabber(uuid)
    for i in dummy.read_playerdata():
        player = MojangAPIGrabber(i)
        result = player.get_minecraft_usernames()
        print(f"{result['name']}\n")
        player.get_minecraft_skins()
    
    dummy.write_playerdata()
    # print(MojangAPIGrabber.)
    print(MojangAPIGrabber(i).read_playerdata())
    