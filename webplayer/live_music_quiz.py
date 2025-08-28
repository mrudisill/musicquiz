#!/usr/bin/env python3
"""
Live Music Quiz - Uses Spotify's Currently Playing API
Creates a quiz based on what you're actually playing on Spotify right now!
"""

import os
import time
import random
from typing import Dict, Optional, List
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from fuzzywuzzy import fuzz

# Load environment variables
load_dotenv()
load_dotenv(dotenv_path="/Users/mollyrudisill/Library/Mobile Documents/com~apple~CloudDocs/Documents/Documents - Molly's MacBook Pro/personal_code/musicrec/.env")


class LiveMusicQuiz:
    """Live Music Quiz using Spotify's Currently Playing API."""
    
    def __init__(self):
        """Initialize the live music quiz with Spotify authentication."""
        self.setup_spotify()
        self.score = 0
        self.total_questions = 0
        self.quiz_history = []
        
    def setup_spotify(self):
        """Set up Spotify authentication with required scopes."""
        scope = "user-read-currently-playing user-read-playback-state user-modify-playback-state user-library-read playlist-read-private"
        
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=os.getenv("SPOTIPY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
            redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
            scope=scope
        ))
        
        print("🎵 Successfully connected to Spotify!")
    
    def get_currently_playing(self) -> Optional[Dict]:
        """Get the currently playing track from Spotify."""
        try:
            current = self.sp.current_playback()
            
            if current is None:
                return None
            
            if not current.get('is_playing', False):
                return None
            
            item = current.get('item')
            if not item or item.get('type') != 'track':
                return None
            
            # Format track data
            track_data = {
                'id': item['id'],
                'title': item['name'],
                'artist': ', '.join([artist['name'] for artist in item['artists']]),
                'album': item['album']['name'],
                'year': item['album']['release_date'][:4] if item['album']['release_date'] else 'Unknown',
                'duration_ms': item['duration_ms'],
                'popularity': item['popularity'],
                'uri': item['uri'],
                'progress_ms': current.get('progress_ms', 0),
                'is_playing': current.get('is_playing', False),
                'device': current.get('device', {}).get('name', 'Unknown Device')
            }
            
            return track_data
            
        except Exception as e:
            print(f"❌ Error getting currently playing track: {e}")
            return None
    
    def get_track_features(self, track_id: str) -> Optional[Dict]:
        """Get audio features for a track."""
        try:
            features = self.sp.audio_features([track_id])[0]
            if features:
                return {
                    'tempo': round(features['tempo']),
                    'energy': round(features['energy'] * 100),
                    'danceability': round(features['danceability'] * 100),
                    'valence': round(features['valence'] * 100),
                    'acousticness': round(features['acousticness'] * 100),
                    'key': features['key'],
                    'mode': 'Major' if features['mode'] == 1 else 'Minor'
                }
        except Exception as e:
            print(f"⚠️  Could not get audio features: {e}")
            return None
    
    def wait_for_new_track(self, timeout: int = 60) -> Optional[Dict]:
        """Wait for a new track to start playing."""
        print(f"⏳ Waiting for you to play a new song (timeout: {timeout}s)...")
        print("🎵 Start playing a song on Spotify now!")
        
        last_track_id = None
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            current = self.get_currently_playing()
            
            if current:
                current_id = current['id']
                
                # Check if this is a new track
                if current_id != last_track_id:
                    # Make sure we haven't used this track recently
                    recent_ids = [track['id'] for track in self.quiz_history[-5:]]
                    if current_id not in recent_ids:
                        print(f"🎵 New track detected!")
                        return current
                
                last_track_id = current_id
            
            time.sleep(2)  # Check every 2 seconds
        
        print("⏰ Timeout reached. No new track detected.")
        return None
    
    def calculate_score(self, user_title: str, user_artist: str, correct_title: str, correct_artist: str) -> tuple:
        """Calculate score based on similarity."""
        title_similarity = fuzz.ratio(user_title.lower().strip(), correct_title.lower().strip())
        artist_similarity = fuzz.ratio(user_artist.lower().strip(), correct_artist.lower().strip())
        
        points = 0
        feedback_parts = []
        
        # Title scoring (max 60 points)
        if title_similarity >= 90:
            points += 60
            feedback_parts.append("🎯 Perfect title!")
        elif title_similarity >= 70:
            points += 40
            feedback_parts.append("👍 Close title!")
        elif title_similarity >= 50:
            points += 20
            feedback_parts.append("🤔 Partial title match")
        else:
            feedback_parts.append("❌ Title incorrect")
        
        # Artist scoring (max 40 points)
        if artist_similarity >= 90:
            points += 40
            feedback_parts.append("🎯 Perfect artist!")
        elif artist_similarity >= 70:
            points += 25
            feedback_parts.append("👍 Close artist!")
        elif artist_similarity >= 50:
            points += 10
            feedback_parts.append("🤔 Partial artist match")
        else:
            feedback_parts.append("❌ Artist incorrect")
        
        feedback = " | ".join(feedback_parts)
        return points, feedback
    
    def show_track_hints(self, track: Dict, features: Optional[Dict] = None):
        """Show hints about the track without revealing title/artist."""
        print(f"\n🔍 TRACK HINTS:")
        print(f"📅 Year: {track['year']}")
        print(f"📀 Album: {track['album']}")
        print(f"🔥 Popularity: {track['popularity']}/100")
        print(f"⏱️  Duration: {track['duration_ms'] // 60000}:{(track['duration_ms'] % 60000) // 1000:02d}")
        print(f"📱 Playing on: {track['device']}")
        
        if features:
            print(f"🎵 Tempo: {features['tempo']} BPM")
            print(f"⚡ Energy: {features['energy']}/100")
            print(f"💃 Danceability: {features['danceability']}/100")
            print(f"😊 Mood (Valence): {features['valence']}/100")
            print(f"🎸 Acoustic: {features['acousticness']}/100")
            print(f"🎼 Key: {features['key']} {features['mode']}")
    
    def play_live_round(self, round_num: int) -> Optional[int]:
        """Play a single live round."""
        print(f"\n{'='*60}")
        print(f"🎵 LIVE ROUND {round_num}")
        print(f"{'='*60}")
        
        # Wait for a new track
        track = self.wait_for_new_track(timeout=120)
        
        if not track:
            print("❌ No track detected. Skipping this round.")
            return None
        
        # Get audio features
        features = self.get_track_features(track['id'])
        
        # Show hints
        self.show_track_hints(track, features)
        
        print(f"\n🎧 Listen to the song that's currently playing...")
        print("🤔 Can you identify this track?")
        
        # Wait a bit for them to listen
        listen_time = int(input("\nHow many seconds do you want to listen? (10-60): ").strip() or "15")
        listen_time = max(10, min(60, listen_time))
        
        print(f"🎵 Listen for {listen_time} seconds...")
        for i in range(listen_time, 0, -1):
            print(f"⏰ {i} seconds remaining...", end='\r')
            time.sleep(1)
        print("\n")
        
        # Get user input
        user_title = input("📝 Song Title: ").strip()
        user_artist = input("🎤 Artist: ").strip()
        
        # Calculate score
        points, feedback = self.calculate_score(
            user_title, user_artist, track['title'], track['artist']
        )
        
        # Show results
        print(f"\n📊 ROUND {round_num} RESULTS:")
        print(f"✅ Correct Answer: '{track['title']}' by {track['artist']}")
        print(f"📝 Your Answer: '{user_title}' by {user_artist}")
        print(f"💯 Score: {points}/100 points")
        print(f"📈 {feedback}")
        
        # Add to history
        self.quiz_history.append(track)
        
        return points
    
    def start_live_quiz(self, num_rounds: int = 3):
        """Start the live music quiz."""
        print("🎵" * 20)
        print("🎤 LIVE MUSIC QUIZ! 🎵")
        print("🎵" * 20)
        print("\nHow it works:")
        print("• Play songs on Spotify (any device)")
        print("• The quiz will detect when you start a new song")
        print("• Listen to the song and guess the title & artist")
        print("• You control the music - pause, skip, replay as needed!")
        print("\n⚠️  Make sure Spotify is open and you're logged in!")
        
        # Check if something is currently playing
        current = self.get_currently_playing()
        if current:
            print(f"🎵 Currently playing: '{current['title']}' by {current['artist']}")
            print("🔄 Start playing a different song to begin the quiz!")
        else:
            print("🔇 No music currently playing. Start playing a song to begin!")
        
        input("\nPress Enter when you're ready to start...")
        
        self.score = 0
        completed_rounds = 0
        
        for round_num in range(1, num_rounds + 1):
            round_score = self.play_live_round(round_num)
            
            if round_score is not None:
                self.score += round_score
                completed_rounds += 1
                
                if round_num < num_rounds:
                    print(f"\n⏳ Current Score: {self.score}/{completed_rounds * 100}")
                    cont = input("Continue to next round? (y/n): ").lower().strip()
                    if cont in ['n', 'no', 'quit', 'exit']:
                        break
            else:
                # Ask if they want to try again
                retry = input("Try this round again? (y/n): ").lower().strip()
                if retry not in ['y', 'yes']:
                    break
        
        # Show final results
        self.show_final_results(completed_rounds)
    
    def show_final_results(self, completed_rounds: int):
        """Display final quiz results."""
        print(f"\n{'='*60}")
        print("🏆 FINAL RESULTS")
        print(f"{'='*60}")
        
        if completed_rounds > 0:
            percentage = (self.score / (completed_rounds * 100)) * 100
            
            print(f"📊 Total Score: {self.score}/{completed_rounds * 100} points")
            print(f"📈 Percentage: {percentage:.1f}%")
            print(f"🎵 Rounds Completed: {completed_rounds}")
            
            # Performance feedback
            if percentage >= 90:
                print("🌟 AMAZING! You know your music! 🎵")
            elif percentage >= 75:
                print("🎉 EXCELLENT! Great music knowledge! 🎶")
            elif percentage >= 60:
                print("👍 GOOD JOB! You're a music fan! 🎧")
            elif percentage >= 40:
                print("🤔 NOT BAD! Keep listening! 📻")
            else:
                print("💪 KEEP DISCOVERING! Music awaits! 🎵")
        else:
            print("😅 No rounds completed, but thanks for trying!")
        
        print(f"\nThanks for playing the Live Music Quiz! 🎉")

def main():
    """Main function to run the live music quiz."""
    try:
        quiz = LiveMusicQuiz()
        
        while True:
            print(f"\n{'🎵' * 15}")
            print("LIVE MUSIC QUIZ")
            print(f"{'🎵' * 15}")
            print("1. 🎯 Quick Live Quiz (3 rounds)")
            print("2. 🎮 Custom Live Quiz (choose number of rounds)")
            print("3. 🚪 Exit")
            
            choice = input("\nSelect an option (1-3): ").strip()
            
            if choice == "1":
                quiz.start_live_quiz(num_rounds=3)
                
            elif choice == "2":
                try:
                    num_rounds = int(input("How many rounds? (1-10): ").strip())
                    num_rounds = max(1, min(10, num_rounds))
                    quiz.start_live_quiz(num_rounds=num_rounds)
                except ValueError:
                    print("❌ Please enter a valid number.")
                    
            elif choice == "3":
                print("🎵 Thanks for playing! Goodbye! 🎵")
                break
                
            else:
                print("❌ Invalid choice. Please select 1-3.")
                
    except KeyboardInterrupt:
        print("\n\n🎵 Quiz interrupted. Goodbye! 🎵")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    main()
