import random
import json
import sys

# Import hard mode dynamically
try:
    from hard_mode_script import hard_mode  # Assumes your hard mode game is in "hard_mode_script.py"
except ImportError:
    print("Hard mode script not found! Ensure 'hard_mode_script.py' is in the same directory.")
    sys.exit(1)

# High score file
HIGH_SCORE_FILE = "highscores_easy.json"

def load_high_scores():
    """Loads the top 3 high scores from a file."""
    try:
        with open(HIGH_SCORE_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_high_score(name, score):
    """Saves the top 3 high scores to a file."""
    scores = load_high_scores()
    scores.append({"name": name, "score": score})
    scores = sorted(scores, key=lambda x: x["score"])[:3]
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

def main():
    player_name = input("Enter your name: ").strip()
    
    while True:
        try:
            dif = int(input("Select difficulty (1 for easy, 2 for medium, 3 for hard): "))
            if dif in [1, 2, 3]:
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
        except ValueError:
            print("Invalid input! Please enter a number.")
    
    if dif == 3:
        print("\nLoading Hard Mode... Good Luck!")
        hard_mode()  # Calls hard mode function from imported script
        return
    
    num = random.randint(1, 100)
    print("(DEBUG: The number is", num, ")")  # Remove this for final version
    score = 200 if dif == 1 else 100
    guess_count = 0
    
    while score > 0:
        guess = input("Take a guess! (between 1 and 100) or type 'stop' to quit: ").lower()
        if guess == "stop":
            print("Game Over!")
            break
        elif guess == "cheesewheel":
            print("You win Egg-avier! 0 points!")
            break
        else:
            try:
                guess = int(guess)
            except ValueError:
                print("Please enter a valid number or 'stop' to quit.")
                continue
        
        guess_count += 1
        
        if guess == num:
            print(f"Congratulations, {player_name}! You won!")
            print("Your score is:", score)
            save_high_score(player_name, guess_count)
            display_high_scores()
            break
        else:
            print("Pssss, guess higher" if num > guess else "Pssss, guess lower")
            score -= 20
            
            if score <= 0:
                x = input("Game Over! Do you wish to restart? y/n: ")
                if x.lower() == "y":
                    main()
                else:
                    break
            else:
                print("Wrong guess! Current score is:", score)
                if dif == 1:
                    awn = input("Want a mega hint? Type 'yes please!' or 'no thank you': ")
                    if awn.lower() == "yes please!":
                        print("The number is between", num - 5, "and", num + 7)
                    elif awn.lower() == "no thank you":
                        print("Okay, good luck!")

if __name__ == "__main__":
    main()
