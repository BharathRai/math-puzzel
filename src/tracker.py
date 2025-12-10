import time

class PerformanceTracker:
    def __init__(self):
        self.history = []
        self.start_time = 0

    def start_timer(self):
        self.start_time = time.time()

    def log_attempt(self, difficulty, is_correct):
        duration = time.time() - self.start_time
        record = {
            "difficulty": difficulty,
            "correct": is_correct,
            "time_taken": round(duration, 2)
        }
        self.history.append(record)
        return record

    def get_summary(self):
        total = len(self.history)
        if total == 0:
            return {
                "total_attempts": 0,
                "accuracy": "0.0%",
                "avg_time": "0.00s",
                "streak": 0
            }
        
        correct_count = sum(1 for r in self.history if r['correct'])
        avg_time = sum(r['time_taken'] for r in self.history) / total
        
        # Calculate Current Streak
        streak = 0
        for r in reversed(self.history):
            if r['correct']:
                streak += 1
            else:
                break

        return {
            "total_attempts": total,
            "accuracy": f"{(correct_count/total)*100:.1f}%",
            "avg_time": f"{avg_time:.2f}s",
            "streak": streak
        }