from flask import Flask, request, redirect, session, url_for, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from utils.streaming_data_parser import analyze_streaming_data
from utils.spotify_api_helper import create_spotify_instance, analyze_user_playlists
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

# Load environment variables
load_dotenv()

# Set up Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:3000"]}})

app.secret_key = os.getenv('FLASK_SECRET_KEY')
app.config['SESSION_COOKIE_NAME'] = 'spotify-login-session'

# Spotify OAuth setup
sp_oauth = SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="user-library-read user-library-modify playlist-read-private playlist-modify-public playlist-modify-private"
)

@app.route('/login')
def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info
    return redirect("http://localhost:3000/")  # Redirect to the frontend

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

    # Get the uploaded JSON streaming files
    json_files = request.files.getlist('streaming_data')

    if not json_files:
        return jsonify({"error": "No files provided"}), 400

    try:
        # Analyze streaming data to identify skipped tracks
        skipped_tracks = analyze_streaming_data(json_files=json_files)
        
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
    app.run(debug=True)

