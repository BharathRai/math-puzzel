import numpy as np
from sklearn.tree import DecisionTreeClassifier

class MLAdaptiveEngine:
    def __init__(self):
        self.model = DecisionTreeClassifier()
        self.levels = ["Easy", "Medium", "Hard"]
        self.level_map = {"Easy": 0, "Medium": 1, "Hard": 2}
        
        # Train the model immediately on initialization
        self.train_initial_model()

    def train_initial_model(self):
        """
        Since we have no real user data yet, we train the model on 
        synthetic data representing ideal logic.
        Features: [current_level_idx, is_correct (0/1), time_taken]
        Labels:   0=Decrease, 1=Stay, 2=Increase
        """
        # Synthetic Training Data
        # Format: [Level, Correct?, Time]
        X_train = [
            # Case: Correct & Fast -> Increase (Label 2)
            [0, 1, 2.0], [1, 1, 3.5], [0, 1, 1.5],
            
            # Case: Correct but Slow -> Stay (Label 1)
            [0, 1, 12.0], [1, 1, 15.0], [2, 1, 20.0],
            
            # Case: Incorrect -> Decrease (Label 0)
            [1, 0, 5.0], [2, 0, 8.0], [1, 0, 2.0], [2, 0, 15.0],
            
            # Case: Easy & Incorrect -> Stay (Can't go lower) (Label 1)
            [0, 0, 5.0]
        ]
        
        # Labels: 0=Down, 1=Same, 2=Up
        y_train = [
            2, 2, 2,  # Fast/Correct
            1, 1, 1,  # Slow/Correct
            0, 0, 0, 0, # Wrong
            1         # Wrong at Easy
        ]

        self.model.fit(X_train, y_train)

    def predict_next_difficulty(self, current_difficulty, last_performance):
        """
        Predicts next level based on user performance.
        """
        # Prepare input features
        lvl_idx = self.level_map[current_difficulty]
        correct_numeric = 1 if last_performance['correct'] else 0
        time_val = last_performance['time_taken']

        # Predict action (0, 1, or 2)
        prediction = self.model.predict([[lvl_idx, correct_numeric, time_val]])[0]

        # Apply logic to bound the levels (cannot go below Easy or above Hard)
        next_idx = lvl_idx
        
        if prediction == 2:   # Increase
            next_idx = min(lvl_idx + 1, 2)
        elif prediction == 0: # Decrease
            next_idx = max(lvl_idx - 1, 0)
        # prediction == 1 is Stay, so next_idx doesn't change

        return self.levels[next_idx]

# Expose a simple function for main.py to use
engine = MLAdaptiveEngine()

def adjust_difficulty(current_difficulty, last_performance):
    return engine.predict_next_difficulty(current_difficulty, last_performance)