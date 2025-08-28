#!/usr/bin/env python3
"""
Demo version of the Music Quiz - shows how scoring works without requiring Spotify setup.
Perfect for testing the core functionality.
"""

from fuzzywuzzy import fuzz
import random

class DemoMusicQuiz:
    """Demo version of the music quiz for testing without Spotify."""
    
    def __init__(self):
        self.score = 0
        self.total_questions = 0
        
        # Sample tracks for demo
        self.demo_tracks = [
            {
                'title': 'Bohemian Rhapsody',
                'artist': 'Queen',
                'album': 'A Night at the Opera',
                'year': '1975'
            },
            {
                'title': 'Hotel California', 
                'artist': 'Eagles',
                'album': 'Hotel California',
                'year': '1976'
            },
            {
                'title': 'Billie Jean',
                'artist': 'Michael Jackson', 
                'album': 'Thriller',
                'year': '1982'
            },
            {
                'title': 'Sweet Child O\' Mine',
                'artist': 'Guns N\' Roses',
                'album': 'Appetite for Destruction', 
                'year': '1987'
            },
            {
                'title': 'Smells Like Teen Spirit',
                'artist': 'Nirvana',
                'album': 'Nevermind',
                'year': '1991'
            }
        ]
    
    def calculate_score(self, user_title, user_artist, correct_title, correct_artist):
        """Same scoring system as the main quiz."""
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
    
    def play_demo_round(self, track, round_num, total_rounds):
        """Play a demo round without audio."""
        print(f"\n{'='*60}")
        print(f"🎵 DEMO ROUND {round_num}/{total_rounds}")
        print(f"{'='*60}")
        
        # Show track info as hints
        print(f"📅 Year: {track['year']}")
        print(f"📀 Album: {track['album']}")
        
        print(f"\n🎧 Imagine you just heard a preview of this classic song...")
        print("🤔 What song was that?")
        
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
        
        return points
    
    def show_final_results(self):
        """Display final demo results."""
        print(f"\n{'='*60}")
        print("🏆 DEMO RESULTS")
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
        
        print(f"\nDemo complete! 🎉")
        print("To play with real Spotify tracks and audio, set up your .env file and run music_quiz.py")
    
    def start_demo(self, num_questions=3):
        """Start the demo quiz."""
        print("🎵" * 20)
        print("🎤 MUSIC QUIZ DEMO! 🎵")
        print("🎵" * 20)
        print("\nThis is a demo version showing how the quiz works!")
        print("• No audio playback (imagine hearing the songs)")
        print("• Classic rock tracks for easy recognition")
        print("• Same scoring system as the full version")
        print("\nIn the real version, you'll hear actual Spotify previews!")
        
        # Randomly select tracks
        selected_tracks = random.sample(self.demo_tracks, min(num_questions, len(self.demo_tracks)))
        
        self.total_questions = len(selected_tracks)
        self.score = 0
        
        input(f"\nPress Enter to start the {self.total_questions}-question demo...")
        
        # Play each round
        for i, track in enumerate(selected_tracks, 1):
            round_score = self.play_demo_round(track, i, self.total_questions)
            self.score += round_score
            
            if i < self.total_questions:
                print(f"\n⏳ Current Score: {self.score}/{i * 100}")
                input("Press Enter for the next round...")
        
        # Show final results
        self.show_final_results()

def main():
    """Run the demo."""
    demo = DemoMusicQuiz()
    
    while True:
        print(f"\n{'🎵' * 15}")
        print("MUSIC QUIZ DEMO")
        print(f"{'🎵' * 15}")
        print("1. 🎯 Quick Demo (3 questions)")
        print("2. 🎮 Full Demo (5 questions)")
        print("3. 🔍 Test Scoring Examples")
        print("4. 🚪 Exit")
        
        choice = input("\nSelect an option (1-4): ").strip()
        
        if choice == "1":
            demo.start_demo(num_questions=3)
            
        elif choice == "2":
            demo.start_demo(num_questions=5)
            
        elif choice == "3":
            # Show scoring examples
            print(f"\n{'='*50}")
            print("🧪 SCORING SYSTEM EXAMPLES")
            print(f"{'='*50}")
            
            examples = [
                ("Bohemian Rhapsody", "Queen", "Bohemian Rhapsody", "Queen"),
                ("bohemian rhapsody", "queen", "Bohemian Rhapsody", "Queen"),
                ("Bohemian Rhap", "Queen", "Bohemian Rhapsody", "Queen"),
                ("Rhapsody", "Queen", "Bohemian Rhapsody", "Queen"),
                ("Hotel California", "The Eagles", "Hotel California", "Eagles"),
                ("Wrong Song", "Wrong Artist", "Bohemian Rhapsody", "Queen"),
            ]
            
            for user_title, user_artist, correct_title, correct_artist in examples:
                points, feedback = demo.calculate_score(user_title, user_artist, correct_title, correct_artist)
                print(f"\n📝 Guess: '{user_title}' by {user_artist}")
                print(f"✅ Correct: '{correct_title}' by {correct_artist}")
                print(f"💯 Score: {points}/100 - {feedback}")
            
        elif choice == "4":
            print("🎵 Thanks for trying the demo! 🎵")
            break
            
        else:
            print("❌ Invalid choice. Please select 1-4.")

if __name__ == "__main__":
    main()
