from flask import Flask, request, jsonify
from utils.streaming_data_parser import parse_skipped_tracks
from utils.spotify_api_helper import remove_tracks_from_spotify

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Spotify Cleanup API!"

@app.route('/recommendations', methods=['GET', 'POST'])
def recommendations():
    if request.method == 'POST':
        # Handle the POST request logic here
        return "Handling POST request for recommendations"
    else:
        # Handle the GET request (for testing or displaying simple message)
        return "Recommendations endpoint is ready for POST requests"

@app.route('/remove_tracks', methods=['POST'])
def remove_tracks():
    tracks_to_remove = request.json.get('tracks')
    remove_tracks_from_spotify(tracks_to_remove)
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask

app = Flask(__name__)




