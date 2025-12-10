# Math Adaptive Prototype

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://bharathrai-math-puzzel-srcapp-w64rqa.streamlit.app/)

**Live Demo:** [https://bharathrai-math-puzzel-srcapp-w64rqa.streamlit.app/](https://bharathrai-math-puzzel-srcapp-w64rqa.streamlit.app/)

This project is a prototype for an adaptive math learning system. It generates puzzles, tracks user progress, and adapts the difficulty based on performance.

## Structure

- `src/app.py`: Streamlit web application (Frontend).
- `src/main.py`: Command-line entry point (Legacy).
- `src/puzzle_generator.py`: Generates math puzzles.
- `src/tracker.py`: Tracks user performance.
- `src/adaptive_engine.py`: Adjusts difficulty based on user stats (Rule-based or ML).

## Usage

1. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the Streamlit app:
   ```bash
   streamlit run src/app.py
   ```
