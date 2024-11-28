from flask import Flask, render_template, jsonify
import json
import os

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DATA_FILE_PATH = os.path.join(BASE_DIR, 'output_data', 'usernames.json')

# Load data from JSON
def load_data():
    with open(DATA_FILE_PATH, 'r') as f:
        data = json.load(f)
    
    # Convert the "usermap" dictionary into a list of player dictionaries
    players = [{"uuid": uuid, "username": username} for uuid, username in data["usermap"].items()]
    
    return players


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
    return render_template('player.html', player=player)

if __name__ == "__main__":
    app.run(debug=True)
