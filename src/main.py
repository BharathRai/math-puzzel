from puzzle_generator import generate_puzzle
from tracker import PerformanceTracker
from adaptive_engine import adjust_difficulty

def main():
    print("--- Math Adventures ---")
    name = input("Enter your name: ")
    difficulty = "Easy" # Start at Easy [cite: 17]
    tracker = PerformanceTracker()
    
    print(f"Welcome {name}! Starting at {difficulty} level.")
    print("Type 'exit' to quit.")

    while True:
        # 1. Generate Puzzle
        problem, correct_answer = generate_puzzle(difficulty)
        print(f"\nLevel: {difficulty}")
        print(f"Solve: {problem}")

        # 2. Track Input & Time
        tracker.start_timer()
        user_input = input("Answer: ")

        if user_input.lower() == 'exit':
            break

        try:
            val = int(user_input)
            is_correct = (val == correct_answer)
        except ValueError:
            is_correct = False

        if is_correct:
            print("Correct!")
        else:
            print(f"Wrong. The answer was {correct_answer}")

        # 3. Log Performance
        last_record = tracker.log_attempt(difficulty, is_correct)

        # 4. Adapt Difficulty
        difficulty = adjust_difficulty(difficulty, last_record)
    
    # 5. Summary
    print("\n--- Session Summary ---")
    stats = tracker.get_summary()
    print(stats)

if __name__ == "__main__":
    main()