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
        self.skins_folder = "./static/skins"
        os.makedirs(self.skins_folder, exist_ok=True)


    def get_playerdata_folder(self):
        """
        Reads the 'playerdata' folder and returns a list of UUIDs from the file names.
        Assumes file names are formatted as <UUID>.dat.
        """
        # Correct path based on the new file system
        folder_path = "../world/playerdata"
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
                head_file = os.path.join(self.skins_folder, f"{self.uuid}_head.png")
                with open(head_file, "wb") as file:
                    file.write(head_response.content)
                print(f"Head image successfully saved as {head_file}")
            else:
                print(f"Error fetching head skin: {head_response.status_code} - {head_response.reason}")

            # Download and save full skin
            skin_response = requests.get(skin_url)
            if skin_response.status_code == 200:
                skin_file = os.path.join(self.skins_folder, f"{self.uuid}.png")
                with open(skin_file, "wb") as file:
                    file.write(head_response.content)
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
    

    def generate_achievement_report(self):
        """
        Generate a JSON file for the current UUID that lists all advancements with completed and incomplete criteria,
        using the external advancement_criteria.json for multi-part advancements.
        Filters out advancements with the recipe tag and separates non-Minecraft advancements.
        """
        advancements_path = f"../world/advancements/{self.uuid}.json"
        missing_criteria_path = "./static/advancement_criteria.json"
        output_path = f"./output_data/advancements_report_{self.uuid}.json"

        if not os.path.exists(advancements_path):
            print(f"Advancements file for UUID {self.uuid} does not exist.")
            return

        if not os.path.exists(missing_criteria_path):
            print(f"Advancement criteria file '{missing_criteria_path}' does not exist.")
            return

        try:
            with open(advancements_path, "r") as file:
                advancements_data = json.load(file)

            with open(missing_criteria_path, "r") as file:
                missing_criteria_data = json.load(file)

            multi_part_advancements = missing_criteria_data.get("multi_part_advancements", {})

            report = {"minecraft_advancements": {}, "non_minecraft_advancements": {}}
            for advancement, details in advancements_data.items():
                if not isinstance(details, dict):
                    print(f"Skipping invalid data for advancement {advancement}: {details}")
                    continue  # Skip non-dictionary entries

                # Skip advancements with the "recipe" tag
                if "recipe" in advancement:
                    print(f"Skipping recipe advancement: {advancement}")
                    continue

                completed_criteria = list(details.get("criteria", {}).keys())

                if advancement in multi_part_advancements:
                    total_criteria = multi_part_advancements[advancement]["criteria"]
                else:
                    total_criteria = completed_criteria

                missing_criteria = []
                for criterion in total_criteria:
                    if criterion not in completed_criteria:
                        missing_criteria.append(criterion)

                advancement_data = {
                    "description": multi_part_advancements.get(advancement, {}).get("description", "No description available"),
                    "completed_criteria": completed_criteria,
                    "missing_criteria": missing_criteria,
                    "completed": details.get("done", False),
                }

                # Categorize advancements
                if advancement.startswith("minecraft:"):
                    report["minecraft_advancements"][advancement] = advancement_data
                else:
                    report["non_minecraft_advancements"][advancement] = advancement_data

            # Write the report to an output JSON file
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "w") as json_file:
                json.dump(report, json_file, indent=4)

            print(f"Advancement report successfully saved to {output_path}")
        except Exception as e:
            print(f"An error occurred while processing advancements for UUID {self.uuid}: {e}")



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

                    # Generate advancement report
                    player.generate_achievement_report()
                    print("")
                else:
                    print(result)
            except Exception as e:
                print(f"An error occurred with UUID {player_uuid}: {e}")
        dummy.write_playerdata()
    except Exception as main_e:
        print(f"An error occurred in the main execution: {main_e}")
