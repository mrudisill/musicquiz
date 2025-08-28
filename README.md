[README.md](https://github.com/user-attachments/files/22029590/README.md)
# 🎵 Live Music Quiz  

A real-time music quiz powered by the **Spotify Web API**. Play music on your Spotify account, and this app will challenge you (or friends) to guess the **song title and artist**.  

Two modes are supported:  

1. **CLI Mode** (`live_music_quiz.py`) – Run in your terminal for a text-based game.  
2. **Web Mode** (`web_music_quiz.py` + `updated.html`) – A Flask app with a clean, interactive web UI.  

---

## 🚀 Features  

- Connects to **Spotify Currently Playing API**  
- Detects when a **new song starts playing**  
- Provides **track hints** (album, year, popularity, tempo, etc.)  
- Calculates score using **fuzzy string matching** for title & artist  
- Web UI includes: progress bar, timer, accuracy tracking, final results screen, and share option  

---

## 📂 Project Structure  

```
.
├── live_music_quiz.py    # Terminal/CLI version of the quiz
├── web_music_quiz.py     # Flask backend for web version
├── updated.html          # Frontend UI template for Flask
└── README.md             # Project documentation
```  

---

## ⚙️ Installation  

1. Clone this repository:  
   ```bash
   git clone https://github.com/yourusername/live-music-quiz.git
   cd live-music-quiz
   ```  

2. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```  

   **Dependencies include:**  
   - `spotipy` (Spotify API client)  
   - `flask` + `flask-socketio`  
   - `python-dotenv`  
   - `fuzzywuzzy`  

3. Set up your **Spotify Developer App**:  
   - Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications)  
   - Create an app and copy **Client ID**, **Client Secret**, and set a **Redirect URI** (e.g. `http://127.0.0.1:5002/callback`).  

4. Create a `.env` file in the project root:  
   ```ini
   SPOTIPY_CLIENT_ID=your_client_id
   SPOTIPY_CLIENT_SECRET=your_client_secret
   SPOTIPY_REDIRECT_URI=http://127.0.0.1:5002/callback
   ```  

---

## ▶️ Usage  

### **CLI Mode**  
Run the terminal quiz:  
```bash
python live_music_quiz.py
```  
Follow the prompts — the game detects when you play a new track on Spotify.  

### **Web Mode**  
Start the Flask server:  
```bash
python web_music_quiz.py
```  

Then open [http://127.0.0.1:5002](http://127.0.0.1:5002) in your browser to play in the interactive web UI.  

---

## 🎯 Scoring  

- **Title Match**: up to 70 points  
- **Artist Match**: up to 30 points  
- Final results show **total score, accuracy, avg response time, and songs guessed correctly**.  

---

## 📸 Screenshots  

*(Add UI screenshots here — showing quiz rounds, progress bar, and final results.)*  

---

## 🤝 Contributing  

Pull requests are welcome! For major changes, please open an issue first to discuss your idea.  

---

## 📜 License  

MIT License – feel free to use, modify, and share.  
