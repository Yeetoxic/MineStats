from flask import Flask, render_template
import json
import os
from PlayerGrabber import PlayerGrabber
from MinecraftStatsHandler import MinecraftStatsHandler
import threading
import time

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DATA_FILE_PATH = os.path.join(BASE_DIR, 'output_data', 'usernames.json')

# Create a threading event to signal when to stop
stop_event = threading.Event()

def run_initial_processing():
    global stop_event
    """
    Runs PlayerGrabber and MinecraftStatsHandler to process data when the app starts.
    """
    print("Starting initial data processing...")

    # Process player data using PlayerGrabber
    input_folder = "../world/playerdata"
    output_folder = "./output_data/playerdata"
    os.makedirs(output_folder, exist_ok=True)
    while not stop_event.is_set():
        try:
            for file in os.listdir(input_folder):
                if file.endswith(".dat"):
                    input_file = os.path.join(input_folder, file)
                    output_file = os.path.join(output_folder, f"{file.split('.')[0]}.json")
                    grabber = PlayerGrabber(input_file, output_file)
                    grabber.process_data()

            # Process stats and advancements using MinecraftStatsHandler
            try:
                dummy = MinecraftStatsHandler("dummy_uuid")
                for player_uuid in dummy.folder:
                    try:
                        player = MinecraftStatsHandler(player_uuid)
                        result = player.get_minecraft_usernames()
                        if isinstance(result, dict) and "name" in result:
                            print(f"Username: {result['name']}")
                            player.get_minecraft_skins()

                            # Generate advancement report
                            player.generate_achievement_report()

                            # Convert stats to simplified JSON
                            player.convert_stats_to_simplified_json()
                            print("")
                        else:
                            print(result)
                    except Exception as e:
                        print(f"An error occurred with UUID {player_uuid}: {e}")
                dummy.write_playerdata()
            except Exception as main_e:
                print(f"An error occurred in the main execution: {main_e}")
            # Sleep between cycles if no stop event is set
            if not stop_event.is_set():
                time.sleep(5)
        except Exception as e:
            print(f"An error occurred during data processing: {e}")
            break  # In case of an unexpected error, exit the loop gracefully
    print("Initial data processing complete.")


# Load data from JSON
def load_data():
    with open(DATA_FILE_PATH, 'r') as f:
        data = json.load(f)
    
    # Convert the "usermap" dictionary into a list of player dictionaries
    players = [{"uuid": uuid, "username": username} for uuid, username in data["usermap"].items()]
    
    return players

def load_advancements(player_uuid):
    advancements_file_path = os.path.join(BASE_DIR, 'output_data/advancements_reports', f'advancements_report_{player_uuid}.json')
    try:
        with open(advancements_file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None


@app.route('/')
def index():
    players = load_data()
    return render_template('index.html', players=players)

@app.route('/player/<uuid>')
def player_page(uuid):
    players = load_data()
    player = next((p for p in players if p["uuid"] == uuid), None)
    if not player:
        return "Player not found", 404
    advancements = load_advancements(uuid)
    return render_template('player.html', player=player, advancements=advancements)

@app.route('/player/<uuid>/advancements')
def player_advancements(uuid):
    players = load_data()
    player = next((p for p in players if p["uuid"] == uuid), None)
    if not player:
        return "Player not found", 404
    
    # Load the advancements for the player
    advancements = load_advancements(uuid)
    
    return render_template('advancements.html', player=player, advancements=advancements)


if __name__ == "__main__":
    # Run initial data processing
    processing_thread = threading.Thread(target=run_initial_processing)
    processing_thread.start()
    # Start the Flask app
    try:
        # Run the Flask app on the main thread
        print("Flask app starting...")
        app.run(debug=True, host='0.0.0.0')
    except KeyboardInterrupt:
        pass
        # Handle ^C (Ctrl+C) gracefully
    print("Received KeyboardInterrupt, stopping Flask app.")
    stop_event.set()  # Set the event to signal the thread to stop
    # Ensure the background thread finishes before the program exits
    processing_thread.join()
    print("Background processing complete, shutting down.")
