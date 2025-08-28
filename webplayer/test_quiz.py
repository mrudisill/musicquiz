#!/usr/bin/env python3
"""
Quick test script for the Music Quiz application.
Tests core functionality without requiring full quiz gameplay.
"""

import os
from webplayer.music_quiz import MusicQuiz
from fuzzywuzzy import fuzz

def test_scoring_system():
    """Test the scoring algorithm with various examples."""
    print("🧪 Testing Scoring System...")
    
    quiz = MusicQuiz()
    
    test_cases = [
        # (user_title, user_artist, correct_title, correct_artist, expected_min_score)
        ("Bohemian Rhapsody", "Queen", "Bohemian Rhapsody", "Queen", 90),  # Perfect match
        ("bohemian rhapsody", "queen", "Bohemian Rhapsody", "Queen", 90),  # Case insensitive
        ("Bohemian Rhap", "Queen", "Bohemian Rhapsody", "Queen", 60),     # Partial title
        ("Bohemian Rhapsody", "The Queen", "Bohemian Rhapsody", "Queen", 70),  # Partial artist
        ("Shape of You", "Ed Sheeran", "Bohemian Rhapsody", "Queen", 0),  # Completely wrong
        ("Rhapsody", "Queen", "Bohemian Rhapsody", "Queen", 40),          # Partial title match
    ]
    
    for user_title, user_artist, correct_title, correct_artist, expected_min in test_cases:
        score, feedback = quiz.calculate_score(user_title, user_artist, correct_title, correct_artist)
        status = "✅" if score >= expected_min else "❌"
        print(f"{status} '{user_title}' by {user_artist} → {score}/100 points")
        print(f"   Expected: ≥{expected_min}, Got: {score} - {feedback}")
    
    print("\n✅ Scoring system test completed!")

def test_spotify_connection():
    """Test Spotify API connection."""
    print("\n🔌 Testing Spotify Connection...")
    
    try:
        quiz = MusicQuiz()
        
        # Try to get a small number of tracks
        tracks = quiz.get_quiz_tracks(source="search", limit=2)
        
        if tracks:
            print(f"✅ Successfully fetched {len(tracks)} tracks")
            for i, track in enumerate(tracks, 1):
                print(f"   {i}. '{track['title']}' by {track['artist']}")
                print(f"      Preview: {'✅' if track['preview_url'] else '❌'}")
        else:
            print("⚠️  No tracks found - this might be normal if no tracks have previews")
            
    except Exception as e:
        print(f"❌ Spotify connection failed: {e}")
        print("Make sure your .env file is set up correctly!")

def test_audio_system():
    """Test audio initialization."""
    print("\n🔊 Testing Audio System...")
    
    try:
        import pygame
        pygame.mixer.init()
        print("✅ Audio system initialized successfully!")
        
        # Test basic audio functionality
        print("🎵 Audio system ready for playback")
        pygame.mixer.quit()
        
    except Exception as e:
        print(f"⚠️  Audio system issue: {e}")
        print("The quiz will still work but without audio previews")

def test_dependencies():
    """Test that all required dependencies are available."""
    print("\n📦 Testing Dependencies...")
    
    required_modules = [
        'spotipy',
        'pygame', 
        'fuzzywuzzy',
        'requests',
        'dotenv'
    ]
    
    missing = []
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module} - Missing!")
            missing.append(module)
    
    if missing:
        print(f"\n⚠️  Missing dependencies: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
    else:
        print("\n✅ All dependencies available!")

def main():
    """Run all tests."""
    print("🎵" * 20)
    print("🧪 MUSIC QUIZ TEST SUITE")
    print("🎵" * 20)
    
    # Run tests
    test_dependencies()
    test_scoring_system()
    test_audio_system()
    test_spotify_connection()
    
    print(f"\n{'='*40}")
    print("🎉 Test Suite Complete!")
    print("If all tests passed, you're ready to run the quiz!")
    print("Run: python music_quiz.py")
    print(f"{'='*40}")

if __name__ == "__main__":
    main()
