# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable.

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] **Game purpose:** A Streamlit number guessing game where players pick a difficulty (Easy, Normal, Hard), then try to guess a secret number within a limited number of attempts while receiving directional hints.
- [x] **Bugs found:** (1) The secret number changed on every click because it was not stored in session state. (2) The hint logic was reversed — "Too High" told the player to go higher instead of lower. (3) On even attempts, the secret was cast to a string causing type mismatch comparisons. (4) Hard difficulty had a smaller range than Normal, and attempt limits were inconsistent. (5) Negative numbers were accepted as valid guesses.
- [x] **Fixes applied:** Wrapped the secret number in `st.session_state` so it persists across reruns. Corrected the hint messages so "Too High" says "Go LOWER" and "Too Low" says "Go HIGHER". Removed the `str()` type cast on even attempts. Rebalanced difficulty ranges (Easy: 1-20, Normal: 1-50, Hard: 1-1000) and attempt limits (Easy: 8, Normal: 6, Hard: 5). Added negative/zero input rejection in `parse_guess`. Refactored all game logic from `app.py` into `logic_utils.py` and added 15 pytest tests.

## 📸 Demo

<!-- TODO: Replace with a screenshot of the fixed, winning game -->
- [ ] [Insert a screenshot of your fixed, winning game here]

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, insert a screenshot of your Enhanced Game UI here]
