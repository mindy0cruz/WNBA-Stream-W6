import os
import json
from collections import deque, defaultdict
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ----------------------------
# Load environment variables
# ----------------------------
load_dotenv()
DATA_DIR = os.getenv("BASE_DATA_DIR", "data")
LIVE_DATA_FILE = os.getenv("LIVE_DATA_FILE_NAME", "wnba_playoffs_live.json")
VIS_TITLE = os.getenv("VISUALIZATION_TITLE", "WNBA Playoffs: Live Game Score & Momentum")
MESSAGE_INTERVAL = float(os.getenv("MESSAGE_INTERVAL_SECONDS", 3))

data_file_path = os.path.join(DATA_DIR, LIVE_DATA_FILE)

# ----------------------------
# Load events with validation
# ----------------------------
def load_game_events(file_path):
    if not os.path.exists(file_path):
        print(f"[ERROR] JSON file not found: {file_path}")
        return []

    try:
        with open(file_path, "r") as f:
            events = json.load(f)
        valid_events = []
        for e in events:
            if "team" in e and "player" in e and "points_scored" in e:
                valid_events.append(e)
            else:
                print(f"[WARNING] Skipping invalid event: {e}")
        print(f"[INFO] Loaded {len(valid_events)} valid events from {file_path}")
        return valid_events
    except json.JSONDecodeError:
        print(f"[ERROR] Failed to parse JSON from {file_path}")
        return []

# ----------------------------
# Setup plotting (side-by-side)
# ----------------------------
fig, (ax_score, ax_momentum) = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle(VIS_TITLE, fontsize=16, fontweight="bold")

# Make space at the bottom for explanation text
plt.subplots_adjust(bottom=0.15)
plt.tight_layout(pad=4)

# Bottom caption explaining scale differences
fig.text(
    0.5, 0.05,
    "Note: The left graph shows absolute team scores (always positive, cumulative). "
    "The right graph shows score *difference* (momentum), centered around zero — "
    "so scales will differ.",
    ha="center", va="top", fontsize=9, color="dimgray"
)

team_scores = defaultdict(list)
player_scores = defaultdict(lambda: defaultdict(int))
teams = []
event_queue = deque()
momentum = []

# ----------------------------
# Update function
# ----------------------------
def update(frame):
    if not event_queue:
        return

    event = event_queue.popleft()
    print(f"[DEBUG] Processing event: {event}")

    team = event.get("team")
    player = event.get("player")
    points = event.get("points_scored", 0)

    if not team or points is None:
        print("[WARNING] Invalid event, skipping")
        return

    if team not in teams:
        teams.append(team)

    # Update team score
    prev_score = team_scores[team][-1] if team_scores[team] else 0
    team_scores[team].append(prev_score + points)

    # Update player score
    player_scores[team][player] += points

    # Ensure all teams have equal-length score arrays
    for t in teams:
        if len(team_scores[t]) < len(team_scores[teams[0]]):
            team_scores[t].append(team_scores[t][-1] if team_scores[t] else 0)

    # ----------------------------
    # Plot cumulative scores (Left)
    # ----------------------------
    ax_score.clear()
    ax_score.set_title("Team Scores")
    ax_score.set_xlabel("Play")
    ax_score.set_ylabel("Score")
    ax_score.grid(True, linestyle="--", alpha=0.6)

    for t in teams:
        ax_score.plot(range(len(team_scores[t])), team_scores[t], label=t, linewidth=2)
    ax_score.legend(loc="upper left")

    # Y-axis scaling in multiples of 10
    max_score = max([score[-1] for score in team_scores.values()] + [10])
    y_max = ((max_score // 10) + 1) * 10
    ax_score.set_ylim(0, y_max)
    ax_score.set_yticks(range(0, y_max + 1, 10))

    # Top player annotations
    y_offset = 0.05
    for t in teams:
        if player_scores[t]:
            top_player = max(player_scores[t], key=player_scores[t].get)
            top_points = player_scores[t][top_player]
            ax_score.text(
                0.95, 0.9 - y_offset,
                f"{t} top scorer: {top_player} ({top_points})",
                transform=ax_score.transAxes,
                horizontalalignment='right',
                fontsize=9
            )
            y_offset += 0.05

    # ----------------------------
    # Plot momentum (Right)
    # ----------------------------
    ax_momentum.clear()

    # Dynamic label explaining the scale
    ax_momentum.text(
        0.5, 1.02,
        "",
        transform=ax_momentum.transAxes,
        ha="center",
        va="bottom",
        fontsize=8,
        color="gray"
    )

    if len(teams) == 2:
        t1, t2 = teams
        diff = team_scores[t1][-1] - team_scores[t2][-1]
        momentum.append(diff)

        ax_momentum.set_title(f"Momentum: {t1} - {t2}")
        ax_momentum.set_xlabel("Play")
        ax_momentum.set_ylabel("Score Difference")
        ax_momentum.grid(True, linestyle="--", alpha=0.6)

        # Y-axis scaling in multiples of 10
        if momentum:
            max_diff = max(abs(m) for m in momentum)
            y_max_mom = ((max_diff // 10) + 1) * 10
            ax_momentum.set_ylim(-y_max_mom, y_max_mom)
            ax_momentum.set_yticks(range(-y_max_mom, y_max_mom + 1, 10))

        ax_momentum.plot(range(len(momentum)), momentum, color="crimson", linewidth=2)
        ax_momentum.axhline(0, color="gray", linestyle="--", alpha=0.7)
    else:
        ax_momentum.set_title("Momentum: Waiting for 2 Teams")
        ax_momentum.set_xlabel("Event Number")
        ax_momentum.set_ylabel("Score Difference")
        ax_momentum.grid(True, linestyle="--", alpha=0.6)

# ----------------------------
# Main
# ----------------------------
def main():
    print("[INFO] Starting WNBA Consumer (all momentum changes visible)...")
    events = load_game_events(data_file_path)
    if not events:
        print("[INFO] No events to visualize. Exiting.")
        return

    for event in events:
        event_queue.append(event)

    ani = FuncAnimation(fig, update, interval=MESSAGE_INTERVAL * 1000, cache_frame_data=False)
    plt.show()

if __name__ == "__main__":
    main()
