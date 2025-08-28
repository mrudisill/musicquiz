#!/usr/bin/env python3
"""
Web Music Quiz - Flask web interface for the live music quiz
"""

import os
import time
import json
from typing import Dict, Optional
from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from fuzzywuzzy import fuzz
import secrets

# Load environment variables
load_dotenv()
load_dotenv(dotenv_path="/Users/mollyrudisill/Library/Mobile Documents/com~apple~CloudDocs/Documents/Documents - Molly's MacBook Pro/personal_code/musicrec/.env")

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
socketio = SocketIO(app, cors_allowed_origins="*")

class WebMusicQuiz:
    """Web version of the music quiz."""
    
    def __init__(self):
        self.sp = None
        self.setup_spotify()
        
    def setup_spotify(self):
        """Set up Spotify authentication."""
        scope = "user-read-currently-playing user-read-playback-state user-library-read user-modify-playback-state"
        
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=os.getenv("SPOTIPY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
            redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
            scope=scope,
            cache_path=".spotify_cache",
            open_browser=True,
            show_dialog=False
        ))
    
    def get_currently_playing(self) -> Optional[Dict]:
        """Get the currently playing track."""
        try:
            current = self.sp.current_playback()
            
            if not current or not current.get('is_playing', False):
                return None
            
            item = current.get('item')
            if not item or item.get('type') != 'track':
                return None
            
            return {
                'id': item['id'],
                'title': item['name'],
                'artist': ', '.join([artist['name'] for artist in item['artists']]),
                'album': item['album']['name'],
                'year': item['album']['release_date'][:4] if item['album']['release_date'] else 'Unknown',
                'duration_ms': item['duration_ms'],
                'popularity': item['popularity'],
                'progress_ms': current.get('progress_ms', 0),
                'device': current.get('device', {}).get('name', 'Unknown Device'),
                'image_url': item['album']['images'][0]['url'] if item['album']['images'] else None
            }
        except Exception as e:
            print(f"Error getting currently playing: {e}")
            return None
    
    def skip_to_next_track(self) -> bool:
        """Skip to the next track in the user's current playback."""
        try:
            self.sp.next_track()
            # Wait a moment for Spotify to process the skip
            time.sleep(1.5)
            return True
        except Exception as e:
            print(f"Error skipping track: {e}")
            return False
    
    def calculate_score(self, user_title: str, user_artist: str, correct_title: str, correct_artist: str, response_time: float = None):
        """Calculate quiz score (title + artist = 100 points, no speed bonus)."""
        title_similarity = fuzz.ratio(user_title.lower().strip(), correct_title.lower().strip())
        artist_similarity = fuzz.ratio(user_artist.lower().strip(), correct_artist.lower().strip())
    
        title_points = 0
        artist_points = 0

        # Title scoring (max 70 points)
        if title_similarity >= 90:
            title_points = 70
        elif title_similarity >= 70:
            title_points = 50
        elif title_similarity >= 50:
            title_points = 30

    # Artist scoring (max 30 points)
        if artist_similarity >= 90:
            artist_points = 30
        elif artist_similarity >= 70:
            artist_points = 20
        elif artist_similarity >= 50:
            artist_points = 10

        return {
            'total_points': title_points + artist_points,
            'title_points': title_points,
            'artist_points': artist_points,
            'response_time': response_time,
            'time_message': "",  # keep empty now
            'title_similarity': title_similarity,
            'artist_similarity': artist_similarity
    }
# Initialize quiz instance
quiz = WebMusicQuiz()

@app.route('/')
def index():
    """Main quiz page."""
    return render_template('updated.html')

@app.route('/api/current-track')
def get_current_track():
    """API endpoint to get currently playing track."""
    track = quiz.get_currently_playing()
    if track:
        return jsonify({
            'success': True,
            'track': track
        })
    else:
        return jsonify({
            'success': False,
            'message': 'No track currently playing'
        })

@app.route('/api/skip-track', methods=['POST'])
def skip_track():
    """API endpoint to skip to next track."""
    success = quiz.skip_to_next_track()
    if success:
        # Get the new track after skipping
        track = quiz.get_currently_playing()
        if track:
            return jsonify({
                'success': True,
                'message': 'Skipped to next track',
                'track': track
            })
        else:
            return jsonify({
                'success': True,
                'message': 'Skipped track, but no new track detected yet'
            })
    else:
        return jsonify({
            'success': False,
            'message': 'Failed to skip track. Make sure Spotify is playing music.'
        })

@app.route('/api/submit-guess', methods=['POST'])
def submit_guess():
    """API endpoint to submit a guess."""
    data = request.json
    user_title = data.get('title', '').strip()
    user_artist = data.get('artist', '').strip()
    correct_title = data.get('correct_title', '')
    correct_artist = data.get('correct_artist', '')
    response_time = data.get('response_time', None)  # Time in seconds
    
    if not user_title or not user_artist:
        return jsonify({
            'success': False,
            'message': 'Please provide both title and artist'
        })
    
    score = quiz.calculate_score(user_title, user_artist, correct_title, correct_artist, response_time)
    
    return jsonify({
        'success': True,
        'score': score,
        'user_answer': {
            'title': user_title,
            'artist': user_artist
        },
        'correct_answer': {
            'title': correct_title,
            'artist': correct_artist
        }
    })

@socketio.on('connect')
def handle_connect():
    """Handle client connection."""
    print('Client connected')
    emit('connected', {'data': 'Connected to quiz server'})

@socketio.on('start_monitoring')
def handle_start_monitoring():
    """Start monitoring for track changes."""
    print('Starting track monitoring')
    # This would typically start a background task to monitor track changes
    emit('monitoring_started', {'message': 'Track monitoring started'})

if __name__ == '__main__':
    socketio.run(app, debug=True, host='127.0.0.1', port=5002)
