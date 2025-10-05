# 🏀 WNBA Playoffs Streaming Analytics

## Overview

This project simulates live streaming of WNBA playoff game events and dynamically visualizes team scores and game momentum. Using Python, JSON, and Matplotlib animations, you can see cumulative scores and momentum in near real-time as if following a live game broadcast.

---

## Features

Streams WNBA game events from a JSON file (wnba_playoffs_live.json) simulating live data.

Tracks team scores and player points dynamically.

  Displays two real-time graphs:

    Team Scores: cumulative points per team.

    Momentum: score difference between the two teams.

Top scorer annotations for each team.



## Setup Instructions

  Clone the repository

    git clone https://github.com/mindy0cruz/WNBA-Stream-W6.git

      cd WNBA-Stream-W6


  Create a virtual environment: 
      python -m venv .venv
      
      Activate the virtual environment
        .venv\Scripts\Activate.ps1
    
    Install dependencies
        pip install -r requirements.txt


## Running the Project

Start the Producer

  Simulates streaming of game events:

    python producers/game_producer.py

Start the Consumer

  Visualizes team scores and momentum in real-time:

    python consumers/game_consumer.py


## JSON Event Format

Each game event in wnba_playoffs_live.json has the structure:

      {
    "timestamp": "2025-10-04 19:00:00",
    "game": "Mercury vs Aces",
    "team": "Aces",
    "player": "A’ja Wilson",
    "points_scored": 2,
    "message": "A’ja Wilson hits a jumper to start the game!"
      }




