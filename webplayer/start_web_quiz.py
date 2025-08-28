#!/usr/bin/env python3
"""
Launcher script for the Web Music Quiz
"""

import webbrowser
import time
import threading
from web_music_quiz import app, socketio

def open_browser():
    """Open the web browser after a short delay."""
    time.sleep(2)
    webbrowser.open('http://localhost:5003')

if __name__ == '__main__':
    print("🎵" * 20)
    print("🎤 STARTING WEB MUSIC QUIZ")
    print("🎵" * 20)
    print("\n📱 The quiz will open in your web browser!")
    print("🔗 URL: http://localhost:5003")
    print("\n🎵 Instructions:")
    print("1. Start playing music on Spotify")
    print("2. Click 'Check Current Track' in the web app")
    print("3. Click 'Start Quiz Round' to begin!")
    print("4. Listen and guess the song title and artist")
    print("\n⚠️  Make sure Spotify is open and playing music!")
    print("🚪 Press Ctrl+C to stop the server")
    print("\n" + "="*50)
    
    # Start browser in a separate thread
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Start the web server
    try:
        socketio.run(app, debug=False, host='127.0.0.1', port=5003)
    except KeyboardInterrupt:
        print("\n\n🎵 Quiz server stopped! Goodbye! 🎵")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        print("Make sure port 5002 is available and try again.")
