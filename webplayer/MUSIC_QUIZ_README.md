# 🎵 Music Quiz Application

A fun interactive music quiz that integrates with Spotify to play song previews and challenge users to guess the song title and artist!

## ✨ Features

- 🎧 **Audio Previews**: Plays 15-30 second previews from Spotify
- 🎯 **Smart Scoring**: Uses fuzzy matching to score partial correct answers
- 🎮 **Multiple Quiz Modes**: 
  - Quick Quiz (your top tracks)
  - Custom Quiz (choose length and source)
  - Discovery Quiz (various genres)
- 📊 **Real-time Scoring**: Get immediate feedback on your answers
- 🎵 **Multiple Sources**: Quiz from your top tracks or discover new music

## 🚀 Quick Start

### 1. Setup Spotify App
1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new app
3. Add `http://localhost:8080/callback` as a redirect URI
4. Note your Client ID and Client Secret

### 2. Environment Setup
Create a `.env` file with your Spotify credentials:
```
SPOTIPY_CLIENT_ID=your_client_id_here
SPOTIPY_CLIENT_SECRET=your_client_secret_here
SPOTIPY_REDIRECT_URI=http://localhost:8080/callback
```

### 3. Install Dependencies
```bash
# Run the setup script to check everything
python setup_quiz.py

# Or install manually
pip install -r requirements.txt
```

### 4. Start the Quiz!
```bash
python music_quiz.py
```

## 🎮 How to Play

1. **Choose Quiz Type**: Select from quick quiz, custom quiz, or discovery mode
2. **Listen**: Each round plays a 15-second preview of a song
3. **Guess**: Type in the song title and artist name
4. **Score**: Get points based on how accurate your guess is:
   - Perfect title match: 60 points
   - Perfect artist match: 40 points
   - Partial matches get partial points!
5. **Results**: See your final score and performance feedback

## 📊 Scoring System

The quiz uses intelligent fuzzy matching to score your answers:

- **Title Scoring** (max 60 points):
  - 90%+ similarity: 60 points ✨
  - 70-89% similarity: 40 points 👍
  - 50-69% similarity: 20 points 🤔
  - Below 50%: 0 points ❌

- **Artist Scoring** (max 40 points):
  - 90%+ similarity: 40 points ✨
  - 70-89% similarity: 25 points 👍
  - 50-69% similarity: 10 points 🤔
  - Below 50%: 0 points ❌

## 🎵 Quiz Sources

- **Your Top Tracks**: Based on your Spotify listening history
- **Discovery Mode**: Curated tracks from various genres (pop, rock, hip-hop, indie, etc.)
- **Custom**: Choose the number of questions (1-20)

## 🛠️ Technical Details

### Dependencies
- `spotipy`: Spotify Web API integration
- `pygame`: Audio playback
- `fuzzywuzzy`: Intelligent answer matching
- `requests`: HTTP requests for audio previews
- `python-dotenv`: Environment variable management

### Audio System
- Downloads 30-second Spotify previews
- Plays 15-second clips by default
- Gracefully handles tracks without previews
- Cross-platform audio support via pygame

### API Integration
- Uses Spotify Web API for track metadata
- Requires user authentication for personalized quizzes
- Handles API rate limits and errors gracefully

## 🔧 Troubleshooting

### Common Issues

**No audio playing:**
- Check that pygame is installed: `pip install pygame`
- Ensure your system has audio drivers
- Try running `python setup_quiz.py` to test audio

**Spotify authentication errors:**
- Verify your `.env` file has correct credentials
- Check that redirect URI matches exactly: `http://localhost:8080/callback`
- Ensure your Spotify app is set to "Development" mode

**No tracks with previews:**
- Try "Discovery Mode" instead of "Your Top Tracks"
- Some tracks don't have preview URLs available
- The app will automatically filter for tracks with previews

**Installation issues:**
- Make sure you have Python 3.7+
- Try: `pip install --upgrade pip` then `pip install -r requirements.txt`
- On macOS: You might need to install pygame dependencies

### Audio Setup (macOS specific)
If you encounter audio issues on macOS:
```bash
# Install pygame dependencies
brew install sdl2 sdl2_image sdl2_mixer sdl2_ttf
pip install pygame
```

## 🎯 Performance Tips

- **Internet Connection**: Stable connection needed for audio streaming
- **Spotify Premium**: Not required, but recommended for better experience
- **Audio Quality**: Depends on Spotify's preview quality (128kbps)

## 🔮 Future Enhancements

Potential features for future versions:
- 🏆 Leaderboards and score tracking
- 🎨 Web interface with better UI
- 🎪 Multiplayer support
- 🎭 Themed quizzes (decades, genres, artists)
- 📱 Mobile app version
- 🔄 Playlist creation from quiz songs

## 📄 License

This project is for educational and personal use. Spotify content usage follows Spotify's Terms of Service.

## 🙏 Acknowledgments

- Spotify Web API for music data and previews
- pygame community for audio playback capabilities
- fuzzywuzzy for intelligent text matching

---

Have fun testing your music knowledge! 🎵🎉
