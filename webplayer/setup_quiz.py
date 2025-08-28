#!/usr/bin/env python3
"""
Setup script for the Music Quiz application.
Helps check dependencies and Spotify credentials.
"""

import os
import sys
import subprocess
from dotenv import load_dotenv

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7+ is required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def install_dependencies():
    """Install required dependencies."""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def check_spotify_credentials():
    """Check if Spotify credentials are configured."""
    print("\n🔐 Checking Spotify credentials...")
    
    # Load environment variables
    load_dotenv()
    load_dotenv(dotenv_path="/Users/mollyrudisill/Library/Mobile Documents/com~apple~CloudDocs/Documents/Documents - Molly's MacBook Pro/personal_code/musicrec/.env")
    
    client_id = os.getenv("SPOTIPY_CLIENT_ID")
    client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
    redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")
    
    missing = []
    if not client_id:
        missing.append("SPOTIPY_CLIENT_ID")
    if not client_secret:
        missing.append("SPOTIPY_CLIENT_SECRET")
    if not redirect_uri:
        missing.append("SPOTIPY_REDIRECT_URI")
    
    if missing:
        print(f"❌ Missing Spotify credentials: {', '.join(missing)}")
        print("\n📝 To set up Spotify credentials:")
        print("1. Go to https://developer.spotify.com/dashboard")
        print("2. Create a new app")
        print("3. Add 'http://localhost:8080/callback' as a redirect URI")
        print("4. Create a .env file with:")
        print("   SPOTIPY_CLIENT_ID=your_client_id")
        print("   SPOTIPY_CLIENT_SECRET=your_client_secret")
        print("   SPOTIPY_REDIRECT_URI=http://localhost:8080/callback")
        return False
    
    print("✅ Spotify credentials found!")
    return True

def test_audio_system():
    """Test if audio system works."""
    print("\n🔊 Testing audio system...")
    try:
        import pygame
        pygame.mixer.init()
        pygame.mixer.quit()
        print("✅ Audio system works!")
        return True
    except Exception as e:
        print(f"⚠️  Audio system may have issues: {e}")
        print("The quiz will still work but without audio previews.")
        return False

def main():
    """Run setup checks."""
    print("🎵" * 20)
    print("🎤 MUSIC QUIZ SETUP")
    print("🎵" * 20)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", install_dependencies),
        ("Spotify Credentials", check_spotify_credentials),
        ("Audio System", test_audio_system)
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n🔍 Checking {name}...")
        result = check_func()
        results.append((name, result))
    
    print(f"\n{'='*40}")
    print("📊 SETUP SUMMARY")
    print(f"{'='*40}")
    
    all_good = True
    for name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {name}")
        if not result and name in ["Python Version", "Dependencies", "Spotify Credentials"]:
            all_good = False
    
    if all_good:
        print(f"\n🎉 Setup complete! Run 'python music_quiz.py' to start the quiz!")
    else:
        print(f"\n⚠️  Please fix the issues above before running the quiz.")

if __name__ == "__main__":
    main()
