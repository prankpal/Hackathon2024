import json
import uuid
from flask import Flask, request, redirect, session, url_for, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from utils.streaming_data_parser import analyze_streaming_data
from utils.spotify_api_helper import create_spotify_instance, analyze_user_playlists
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import requests

# Load environment variables
load_dotenv()

# Set up Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

app.secret_key = os.getenv('FLASK_SECRET_KEY')
app.config['SESSION_COOKIE_NAME'] = 'spotify-login-session'

# Spotify OAuth setup
sp_oauth = SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="user-library-read user-library-modify playlist-read-private playlist-modify-public playlist-modify-private"
)

def exchange_code_for_token(code):
    token_url = "https://accounts.spotify.com/api/token"
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'response_type': 'code',
        'redirect_uri': os.getenv("SPOTIPY_REDIRECT_URI"),
        'client_id': os.getenv("SPOTIPY_CLIENT_ID"),
        'client_secret': os.getenv("SPOTIPY_CLIENT_SECRET"),
        'state': str(uuid.uuid4()),
        'show_dialog': 'true'
    }
    
    response = requests.post(token_url, data=data)
    token_info = response.json()
    return token_info


@app.route('/login')
def login():
    print("Login route accessed")
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if code:
        try:
            token_info = exchange_code_for_token(code)
            session['token_info'] = token_info
            print("Successfully authenticated!" + str(token_info))
            return redirect('http://localhost:3000/playlists')
        except Exception as e:
            print(f"Error obtaining token: {str(e)}")
            return "An error occurred during authentication", 500
    return "Missing authorization code", 400



@app.route('/playlists', methods=['GET'])
def playlists():
    print("Playlists route accessed")
    token_info = session.get('token_info', None)
    if not token_info:
        return redirect(url_for('login'))

    sp = create_spotify_instance(token_info)
    user_playlists = sp.current_user_playlists(limit=20)
    
    playlists_data = [
        {
            'id': playlist['id'],
            'name': playlist['name'],
            'track_count': playlist['tracks']['total']
        }
        for playlist in user_playlists['items']
    ]
    
    return jsonify(playlists_data)


@app.route('/profile')
def profile():
    # Retrieve the token information from the session
    token_info = session.get('token_info', None)
    if not token_info:
        return redirect(url_for('login'))

    # Use the token to access the Spotify API
    sp = spotipy.Spotify(auth=token_info['access_token'])
    user_profile = sp.current_user()
    return jsonify(user_profile)

@app.route('/analyze', methods=['POST'])
def analyze():
    # Ensure the user is authenticated
    token_info = session.get('token_info', None)
    if not token_info:
        return redirect(url_for('login'))

    # Get the uploaded JSON streaming file
    json_file = request.files.get('streaming_data')

    if not json_file:
        return jsonify({"error": "No file provided"}), 400

    try:
        # Load and analyze the JSON file
        streaming_data = json.load(json_file)

        # Analyze streaming data to identify skipped tracks
        skipped_tracks = analyze_streaming_data(streaming_data)

        # Create Spotify instance with user's token
        sp = create_spotify_instance(token_info)

        # Analyze user's playlists for the skipped tracks
        playlist_analysis = analyze_user_playlists(sp, skipped_tracks)

        return jsonify({
            "skipped_tracks": skipped_tracks,
            "playlist_analysis": playlist_analysis
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5001)

