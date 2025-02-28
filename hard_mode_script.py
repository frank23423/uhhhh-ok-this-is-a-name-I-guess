import random
import time
import threading
import json
from inputimeout import inputimeout, TimeoutOccurred
import sys

# High score file
HIGH_SCORE_FILE = "highscores.json"

# Global configuration
DEFAULT_GUESS_TIME = 10  # Initial allowed seconds per guess
MIN_GUESS_TIME = 3       # Minimum allowed time
guess_count = 0          # Total number of guesses
chase_failures = 0       # Number of failed chase challenges (affects timer)

def load_high_scores():
    """Loads the top 3 high scores from a file."""
    try:
        with open(HIGH_SCORE_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []  # Return an empty list if no scores exist

def save_high_score(name, score):
    """Saves the top 3 high scores to a file."""
    scores = load_high_scores()
    scores.append({"name": name, "score": score})
    scores = sorted(scores, key=lambda x: x["score"])[:3]  # Keep only the top 3
    with open(HIGH_SCORE_FILE, "w") as f:
        json.dump(scores, f, indent=4)

def display_high_scores():
    """Displays the top 3 high scores."""
    scores = load_high_scores()
    print("\n🏆 High Scores 🏆")
    if not scores:
        print("No high scores yet!")
    else:
        for i, entry in enumerate(scores, 1):
            print(f"{i}. {entry['name']} - {entry['score']} guesses")

def countdown_timer(duration, stop_event):
    """Prints a countdown separately while waiting for user input."""
    remaining = duration
    while remaining > 0 and not stop_event.is_set():
        sys.stdout.write(f"\r\033[KTime left: {remaining} seconds\n")
        sys.stdout.flush()
        time.sleep(1)
        remaining -= 1
    sys.stdout.write("\r\033[K")

def get_input_with_timer(prompt, timeout):
    """Displays a countdown while waiting for user input."""
    stop_event = threading.Event()
    timer_thread = threading.Thread(target=countdown_timer, args=(timeout, stop_event))
    timer_thread.daemon = True
    timer_thread.start()
    try:
        user_input = inputimeout(prompt=f"\n{prompt}", timeout=timeout)
    except TimeoutOccurred:
        user_input = None
    stop_event.set()
    timer_thread.join()
    print()
    return user_input

def chase_sequence():
    """Handles the chase sequence. Player must type a code correctly within 5 seconds."""
    challenge_str = ''.join(random.choices("0123456789", k=4))
    allowed_time = 5
    max_attempts = 2
    print("\n--- CHASE SEQUENCE INITIATED! ---")
    print(f"The number is almost caught! To secure it, type this code: {challenge_str}")

    attempts = 0
    while attempts < max_attempts:
        try:
            entry = inputimeout(prompt="Enter the code: ", timeout=allowed_time)
        except TimeoutOccurred:
            entry = None

        if entry == challenge_str:
            print("You nailed the chase sequence and caught the number!")
            return True
        else:
            attempts += 1
            print("Incorrect code or too slow!")
            if attempts < max_attempts:
                print("Quick, try again!")
    return False

def hard_mode():
    global guess_count, chase_failures, DEFAULT_GUESS_TIME
    
    player_name = input("Enter your name: ").strip()

    target_num = random.randint(1, 500)
    print("THE NUMBER HAS ESCAPED!")
    time.sleep(1)
    print("GO FIND IT!...") 
    time.sleep(2)

    guess_count = 0
    chase_failures = 0

    while True:
        current_time = DEFAULT_GUESS_TIME - (guess_count // 5) - chase_failures
        if current_time < MIN_GUESS_TIME:
            current_time = MIN_GUESS_TIME

        print(f"\nYou have {current_time} seconds for your next guess.")
        user_input = get_input_with_timer("Enter your guess (1-500): ", current_time)

        if user_input is None:
            print("Time's up for that guess!")
            guess_count += 1
            continue

        try:
            guess = int(user_input)
        except ValueError:
            print("Invalid input! Please enter a valid number.")
            guess_count += 1
            continue

        guess_count += 1

        if abs(guess - target_num) <= 5:
            print("You're extremely close!")
            if chase_sequence():
                print(f"Congratulations, {player_name}! You won in {guess_count} guesses!")
                save_high_score(player_name, guess_count)
                display_high_scores()
                break
            else:
                print("You failed the chase sequence!")
                chase_failures += 1
                if chase_failures >= 2:
                    print("You've failed twice in the chase. The number has moved!")
                    target_num = random.randint(1, 500)
                    chase_failures = 0
                continue

        elif abs(guess - target_num) <= 10:
            print("You're close, but not quite there. Try again!")
        elif guess < target_num:
            print("Too low! Broaden your search area.")
        else:
            print("Too high! Try a lower range.")

if __name__ == "__main__":
    hard_mode()
