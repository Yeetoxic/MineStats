import os
import requests
import json

username_map = {}

class MojangAPIGrabber:
    def __init__(self, uuid):
        self.uuid = uuid
        self.username = "notch"  # Default value
        self.folder = self.get_playerdata_folder()
        self.MojangAPI_URL = f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}"
        self.skins_folder = "./skins"
        os.makedirs(self.skins_folder, exist_ok=True)

    def get_playerdata_folder(self):
        """
        Reads the 'playerdata' folder and returns a list of UUIDs from the file names.
        Assumes file names are formatted as <UUID>.dat.
        """
        folder_path = "playerdata" # TEMP DATA
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"Folder '{folder_path}' does not exist.")
        result = []
        for file in os.listdir(folder_path):
            if file.endswith(".dat"):
                result.append(file.split(".")[0])
        return result


    def get_minecraft_usernames(self):
        try:
            response = requests.get(self.MojangAPI_URL)
            if response.status_code == 200:
                data = response.json()
                self.username = data['name']
                username_map[self.uuid] = self.username
                return data
            elif response.status_code == 404:
                return "Error: UUID not found. Check if the UUID is correct."
            elif response.status_code == 204:
                return "No content found. The UUID might not exist."
            else:
                return f"Error: {response.status_code} - {response.reason}"
        except requests.exceptions.RequestException as e:
            return f"An error occurred while fetching usernames: {e}"


    def get_minecraft_skins(self):
        try:
            head_url = f"https://mineskin.eu/helm/{self.username}/100.png"
            skin_url = f"https://mineskin.eu/skin/{self.username}"

            # Download and save head skin
            head_response = requests.get(head_url)
            if head_response.status_code == 200:
                head_file = os.path.join(self.skins_folder, f"{self.username}_head.png")
                with open(head_file, "wb") as file:
                    file.write(head_response.content)
                print(f"Head image successfully saved as {head_file}")
            else:
                print(f"Error fetching head skin: {head_response.status_code} - {head_response.reason}")

            # Download and save full skin
            skin_response = requests.get(skin_url)
            if skin_response.status_code == 200:
                skin_file = os.path.join(self.skins_folder, f"{self.username}.png")
                with open(skin_file, "wb") as file:
                    file.write(skin_response.content)
                print(f"Skin image successfully saved as {skin_file}")
            else:
                print(f"Error fetching full skin: {skin_response.status_code} - {skin_response.reason}")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching skins: {e}")


    def write_playerdata(self):
        output_file = "./output_data/usernames.json"
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        data = {
            "usermap": username_map,
            "uuids": list(username_map.keys()),
            "usernames": list(username_map.values())
        }
        with open(output_file, "w") as file_handler:
            json.dump(data, file_handler, indent=4)
        print(f"Usernames data successfully saved to {output_file}")




# Example usage
if __name__ == "__main__":
    try:
        dummy = MojangAPIGrabber("dummy_uuid")
        for player_uuid in dummy.folder:
            try:
                player = MojangAPIGrabber(player_uuid)
                result = player.get_minecraft_usernames()
                if isinstance(result, dict) and "name" in result:
                    print(f"Username: {result['name']}")
                    player.get_minecraft_skins()
                    print("")
                else:
                    print(result)
            except Exception as e:
                print(f"An error occurred with UUID {player_uuid}: {e}")
        dummy.write_playerdata()
    except Exception as main_e:
        print(f"An error occurred in the main execution: {main_e}")
