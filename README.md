# 🏀 WNBA Playoffs Streaming Analytics

This project simulates live streaming data from **WNBA Playoff games** and processes it in real-time to generate insights about **team scores, player performance, and game momentum**.  

A Python **producer** streams simulated play-by-play events (from a JSON file), while a **consumer** processes them, updates game stats, and creates **dynamic visualizations** with Matplotlib.  

---

## 📌 Project Overview

- **Producer**  
  - Reads from a JSON file of simulated WNBA playoff events.  
  - Streams events one by one to mimic a live game.  

- **Consumer**  
  - Listens for events and processes them in real time.  
  - Tracks:  
    - Team scores  
    - Player scoring totals  
    - Momentum runs (scoring streaks)  
  - Generates a **live animated chart** showing the evolving score and momentum.  

- **Visualization**  
  - Animated **line chart** of team scores over time.  
  - Captions highlighting scoring runs and momentum shifts.  

---

## 🛠️ Project Structure

wnba-playoffs-streaming/
│── data/ # Data storage
│ └── wnba_playoffs_live.json # Simulated game events
│
│── producers/
│ └── game_producer.py # Streams live events
│
│── consumers/
│ ├── game_consumer.py # Processes messages & updates stats
│ └── visualizer.py # Handles Matplotlib animation
│
│── utils/
│ ├── utils_config.py # Config handling
│ ├── utils_logger.py # Logging
│ └── utils_helpers.py # Helper functions
│
│── .env # Environment variables (not committed)
│── .env.example # Example env file (safe to commit)
│── requirements.txt # Dependencies
│── README.md # Project documentation


---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/mindy0cruz/WNBA-Stream-W6
cd WNBA-Stream-W6



