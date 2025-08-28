-#!/usr/bin/env python3
"""
Music Quiz Application
A fun quiz game that plays Spotify preview tracks and challenges users to guess the song title and artist.
"""

import os
import random
import time
import threading
import webbrowser
from typing import List, Dict, Tuple, Optional
import requests
from io import BytesIO

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import pygame
from fuzzywuzzy import fuzz

# Load environment variables
load_dotenv()
load_dotenv(dotenv_path="/Users/mollyrudisill/Library/Mobile Documents/com~apple~CloudDocs/Documents/Documents - Molly's MacBook Pro/personal_code/musicrec/.env")


class MusicQuiz:
    """Main Music Quiz class that handles Spotify integration, audio playback, and scoring."""
    
    def __init__(self):
        """Initialize the music quiz with Spotify authentication and pygame for audio."""
        self.setup_spotify()
        self.setup_audio()
        self.score = 0
        self.total_questions = 0
        self.current_tracks = []
        
    def setup_spotify(self):
        """Set up Spotify authentication with required scopes."""
        scope = "user-top-read playlist-read-private user-library-read"
        
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=os.getenv("SPOTIPY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
            redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
            scope=scope
        ))
        
        print("🎵 Successfully connected to Spotify!")
        
    def setup_audio(self):
        """Initialize pygame mixer for audio playback."""
        try:
            pygame.mixer.init()
            print("🔊 Audio system initialized!")
        except pygame.error as e:
            print(f"❌ Could not initialize audio: {e}")
            self.audio_enabled = False
        else:
            self.audio_enabled = True
    
    def get_quiz_tracks(self, source: str = "top", limit: int = 10) -> List[Dict]:
        """
        Fetch tracks for the quiz from various Spotify sources.
        
        Args:
            source: Source of tracks ('top', 'playlist', 'search')
            limit: Number of tracks to fetch
            
        Returns:
            List of track dictionaries with metadata and preview URLs
        """
        tracks = []
        
        if source == "top":
            # Get user's top tracks
            results = self.sp.current_user_top_tracks(limit=limit*2, time_range='medium_term')
            for item in results['items']:
                if item.get('preview_url'):  # Only include tracks with preview URLs
                    tracks.append(self._format_track_data(item))
                    if len(tracks) >= limit:
                        break
                        
        elif source == "search":
            # Search for popular tracks from various genres and popular artists
            genres = ['pop', 'rock', 'hip-hop', 'indie', 'electronic', 'jazz', 'country', 'r&b']
            popular_artists = ['Taylor Swift', 'Ed Sheeran', 'The Weeknd', 'Ariana Grande', 'Drake', 'Billie Eilish']
            
            search_limit = max(5, limit)  # Search more to find tracks with previews
            
            # Try genres first
            for genre in random.sample(genres, min(2, len(genres))):
                if len(tracks) >= limit:
                    break
                try:
                    results = self.sp.search(
                        q=f'genre:{genre}', 
                        type='track', 
                        limit=search_limit,
                        market='US'
                    )
                    for item in results['tracks']['items']:
                        if item.get('preview_url') and len(tracks) < limit:
                            tracks.append(self._format_track_data(item))
                except Exception as e:
                    print(f"Genre search failed for {genre}: {e}")
            
            # If we still need more tracks, try popular artists
            if len(tracks) < limit:
                for artist in random.sample(popular_artists, min(2, len(popular_artists))):
                    if len(tracks) >= limit:
                        break
                    try:
                        results = self.sp.search(
                            q=f'artist:{artist}', 
                            type='track', 
                            limit=search_limit,
                            market='US'
                        )
                        for item in results['tracks']['items']:
                            if item.get('preview_url') and len(tracks) < limit:
                                tracks.append(self._format_track_data(item))
                    except Exception as e:
                        print(f"Artist search failed for {artist}: {e}")
            
            # If still not enough, try a general popular search
            if len(tracks) < limit:
                try:
                    results = self.sp.search(
                        q='year:2020-2024', 
                        type='track', 
                        limit=search_limit*2,
                        market='US'
                    )
                    for item in results['tracks']['items']:
                        if item.get('preview_url') and len(tracks) < limit:
                            tracks.append(self._format_track_data(item))
                except Exception as e:
                    print(f"General search failed: {e}")
        
        # Shuffle tracks for random order
        random.shuffle(tracks)
        return tracks[:limit]
    
    def _format_track_data(self, track_item: Dict) -> Dict:
        """Format Spotify track data for quiz use."""
        return {
            'id': track_item['id'],
            'title': track_item['name'],
            'artist': ', '.join([artist['name'] for artist in track_item['artists']]),
            'album': track_item['album']['name'],
            'preview_url': track_item['preview_url'],
            'popularity': track_item['popularity'],
            'duration': track_item['duration_ms'] // 1000,
            'year': track_item['album']['release_date'][:4] if track_item['album']['release_date'] else 'Unknown'
        }
    
    def download_and_play_preview(self, preview_url: str, duration: int = 15) -> None:
        """
        Download and play a preview audio clip.
        
        Args:
            preview_url: Spotify preview URL
            duration: How long to play the clip (seconds)
        """
        if not self.audio_enabled or not preview_url:
            print("⚠️  Audio not available for this track")
            return
            
        try:
            print("🎵 Downloading audio preview...")
            response = requests.get(preview_url, timeout=10)
            response.raise_for_status()
            
            # Load audio data into pygame
            audio_data = BytesIO(response.content)
            pygame.mixer.music.load(audio_data)
            
            print(f"▶️  Playing preview for {duration} seconds...")
            pygame.mixer.music.play()
            
            # Play for specified duration
            time.sleep(duration)
            pygame.mixer.music.stop()
            
        except requests.RequestException as e:
            print(f"❌ Error downloading audio: {e}")
        except pygame.error as e:
            print(f"❌ Error playing audio: {e}")
    
    def calculate_score(self, user_title: str, user_artist: str, correct_title: str, correct_artist: str) -> Tuple[int, str]:
        """
        Calculate score based on how close the user's answer is to the correct answer.
        
        Args:
            user_title: User's guess for song title
            user_artist: User's guess for artist
            correct_title: Correct song title
            correct_artist: Correct artist name
            
        Returns:
            Tuple of (points_earned, feedback_message)
        """
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
    
    def play_quiz_round(self, track: Dict, round_num: int, total_rounds: int) -> int:
        """
        Play a single round of the quiz.
        
        Args:
            track: Track dictionary with metadata
            round_num: Current round number
            total_rounds: Total number of rounds
            
        Returns:
            Points earned in this round
        """
        print(f"\n{'='*60}")
        print(f"🎵 ROUND {round_num}/{total_rounds}")
        print(f"{'='*60}")
        
        # Show some track metadata as hints
        print(f"📅 Year: {track['year']}")
        print(f"📀 Album: {track['album']}")
        print(f"🔥 Popularity: {track['popularity']}/100")
        
        print(f"\n🎧 Get ready to listen to a {15}-second preview...")
        input("Press Enter when ready to play the song...")
        
        # Play the preview
        self.download_and_play_preview(track['preview_url'], 15)
        
        print("\n🤔 What song was that?")
        
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
        
        # Offer to replay the song
        replay = input("\n🔄 Want to hear it again? (y/n): ").lower().strip()
        if replay in ['y', 'yes']:
            self.download_and_play_preview(track['preview_url'], 20)
        
        return points
    
    def show_final_results(self):
        """Display final quiz results and performance summary."""
        print(f"\n{'='*60}")
        print("🏆 FINAL RESULTS")
        print(f"{'='*60}")
        
        percentage = (self.score / (self.total_questions * 100)) * 100 if self.total_questions > 0 else 0
        
        print(f"📊 Total Score: {self.score}/{self.total_questions * 100} points")
        print(f"📈 Percentage: {percentage:.1f}%")
        
        # Performance feedback
        if percentage >= 90:
            print("🌟 AMAZING! You're a music master! 🎵")
        elif percentage >= 75:
            print("🎉 EXCELLENT! Great music knowledge! 🎶")
        elif percentage >= 60:
            print("👍 GOOD JOB! You know your music! 🎧")
        elif percentage >= 40:
            print("🤔 NOT BAD! Keep listening to more music! 📻")
        else:
            print("💪 KEEP PRACTICING! Music discovery awaits! 🎵")
        
        print(f"\nThanks for playing the Music Quiz! 🎉")
    
    def start_quiz(self, num_questions: int = 5, source: str = "top"):
        """
        Start the main quiz game loop.
        
        Args:
            num_questions: Number of questions to ask
            source: Source for quiz tracks ('top', 'search')
        """
        print("🎵" * 20)
        print("🎤 WELCOME TO THE MUSIC QUIZ! 🎵")
        print("🎵" * 20)
        print("\nInstructions:")
        print("• Listen to each song preview carefully")
        print("• Type the song title and artist name")
        print("• You get points based on how close your answer is!")
        print("• Perfect matches get 100 points per song")
        print("\nFetching quiz tracks...")
        
        # Get tracks for the quiz
        try:
            tracks = self.get_quiz_tracks(source=source, limit=num_questions)
            if not tracks:
                print("❌ No tracks with previews found. Try a different source.")
                return
                
            if len(tracks) < num_questions:
                print(f"⚠️  Only found {len(tracks)} tracks with previews.")
                num_questions = len(tracks)
                
        except Exception as e:
            print(f"❌ Error fetching tracks: {e}")
            return
        
        self.total_questions = num_questions
        self.score = 0
        
        print(f"\n🎯 Starting quiz with {num_questions} questions!")
        input("Press Enter to begin...")
        
        # Play each round
        for i, track in enumerate(tracks[:num_questions], 1):
            round_score = self.play_quiz_round(track, i, num_questions)
            self.score += round_score
            
            if i < num_questions:
                print(f"\n⏳ Current Score: {self.score}/{i * 100}")
                input("Press Enter for the next round...")
        
        # Show final results
        self.show_final_results()


def main():
    """Main function to run the music quiz application."""
    try:
        quiz = MusicQuiz()
        
        while True:
            print(f"\n{'🎵' * 15}")
            print("MUSIC QUIZ OPTIONS")
            print(f"{'🎵' * 15}")
            print("1. 🎯 Quick Quiz (5 questions from your top tracks)")
            print("2. 🎮 Custom Quiz (choose length and source)")
            print("3. 🔍 Discovery Quiz (5 questions from various genres)")
            print("4. 🚪 Exit")
            
            choice = input("\nSelect an option (1-4): ").strip()
            
            if choice == "1":
                quiz.start_quiz(num_questions=5, source="top")
                
            elif choice == "2":
                try:
                    num_q = int(input("How many questions? (1-20): ").strip())
                    num_q = max(1, min(20, num_q))  # Clamp between 1-20
                    
                    print("\nTrack sources:")
                    print("1. Your top tracks")
                    print("2. Discovery (various genres)")
                    source_choice = input("Choose source (1-2): ").strip()
                    
                    source = "top" if source_choice == "1" else "search"
                    quiz.start_quiz(num_questions=num_q, source=source)
                    
                except ValueError:
                    print("❌ Please enter a valid number.")
                    
            elif choice == "3":
                quiz.start_quiz(num_questions=5, source="search")
                
            elif choice == "4":
                print("🎵 Thanks for playing! Goodbye! 🎵")
                break
                
            else:
                print("❌ Invalid choice. Please select 1-4.")
                
    except KeyboardInterrupt:
        print("\n\n🎵 Quiz interrupted. Goodbye! 🎵")
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        print("Make sure your Spotify credentials are set up correctly in your .env file.")


if __name__ == "__main__":
    main()
