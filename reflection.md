# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
  
  Initially when I ran the game it looked simple, just another number guessing game, but I detected multiple issues right away. First of all, the secret number changed every single time I clicked "Submit Gues" because it was generated without using the Streamlit session state (secret_number = random.randint(1, 100)). Secondly, the hints were backwards, meaning that when my guess was higher than the secret number, it told me to "Go HIGHER!" instead of "Go LOWER!", and vice versa. Lastlym there was no such thing as a difficulty system, attempt limits or scoring, so the game lacked structure, there was no chance of winnning. 

- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").
  
  BUG 1 - Reversed Hint Logic: In the original app.py, when guess_int > secret_number, the game displayed "📉 Go HIGHER!" and when guess_int < secret_number, it displayed "📈 Go LOWER!". This is completely backwards, if your guess is too high you should go lower, not higher. The emojis were also swapped (📉 down-arrow paired with "HIGHER").

  BUG 2 - Secret Number Resetting: The line secret_number = random.randint(1, 100) was at the module level, meaning every time Streamlit re-ran the script (which happens on every button click or widget interaction), a brand-new random number was generated. The player was literally chasing a moving target and could never converge on the answer.

  BUG 3 - Type Mismatch: ll game logic was inlined in the Streamlit UI code, making it impossible to unit test. There was no logic_utils.py and no separation of concerns. Additionally, in the fixed version, a type mismatch bug was introduced on even attempts where the secret gets cast to a string (secret = str(st.session_state.secret)), causing comparison issues between int and str types. 

  BUG 4 - Difficulty: Hard difficulty range was set to 1-50 (easier than Normal's 1-100, which is counterintuitive), attempt limits needed rebalancing (Easy: 6, Normal: 8, Hard: 5), the New Game button reset attempts to 0 but attempts started counting at 1, and negative input was allowed without validation.
---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?

  I used tools such as Claude Haiku 4.5.
  
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

  Claude correctly identified the session state bug, it suggested wrapping the secret number in st.session_state using the pattern if "secret" not in st.session_state: st.session_state.secret = random.randint(low, high). I verified this was correct by running the app, opening the Developer Debug Info expander, and confirming that the secret number stayed the same across multiple guesses. Before the fix, every click showed a different number in the debug panel; after the fix, it remained stable until I clicked "New Game."

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

  The AI's hint fix still contains a subtle issue — in check_guess() at lines 37-40 of app.py, when the guess is too high, the message says "📈 Go HIGHER!" and when it's too low, it says "📉 Go LOWER!". While the outcome labels ("Too High", "Too Low") are correct, the user-facing messages still tell players to go in the wrong direction (if your guess is too high, you should go lower, not higher). I verified this by reading the code carefully and tracing the logic: guess > secret returns "Too High" (correct label) but "📈 Go HIGHER!" (incorrect advice to the player). The emojis and direction words are still swapped from what a player would expect.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?

  I used a combination of manual playtesting and code review to verify fixes. For the session state bug, I ran the Streamlit app, opened the Developer Debug Info expander, and checked that the secret number remained constant across multiple guesses. For the hint logic, I made deliberate guesses above and below the secret number (visible in debug mode) to confirm the hints pointed in the correct direction. I also reviewed the code line by line to trace the logical flow and confirm the conditional branches matched the expected behavior.

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.

  The project includes three pytest tests in tests/test_game_logic.py that test the check_guess() function from logic_utils.py. The tests check: (1) check_guess(50, 50) should return "Win", (2) check_guess(60, 50) should return "Too High", and (3) check_guess(40, 50) should return "Too Low". However, these tests currently expect check_guess() to return a plain string, while the implementation in app.py returns a tuple like ("Win", "🎉 Correct!"). This mismatch means the tests would fail against the current implementation — the tests need to be updated to either unpack the tuple or only compare the first element. Running pytest against the stubs in logic_utils.py raises NotImplementedError, confirming that logic_utils.py still needs the refactored implementations.

- Did AI help you design or understand any tests? How?

  Yes, Claude helped explain what the test cases were verifying and pointed out the mismatch between the test expectations (string return) and the actual implementation (tuple return). It also helped clarify why separating game logic into logic_utils.py was necessary — you can't easily unit test functions that are embedded inside Streamlit widget callbacks because they depend on the Streamlit runtime. By extracting pure functions like check_guess(), parse_guess(), and get_range_for_difficulty(), the logic becomes independently testable with standard pytest.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.

  In the original app, the secret number was generated with secret_number = random.randint(1, 100) at the top level of the script, outside of any session state protection. Streamlit works by re-executing the entire Python script from top to bottom every time a user interacts with any widget (clicks a button, types in an input, etc.). So every time you clicked "Submit Guess," the entire script re-ran, and that random.randint() call generated a completely new random number. The secret was literally a moving target — by the time Streamlit checked your guess against secret_number, it was already a different number than when you started.

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

  Imagine a whiteboard that gets completely erased and redrawn every time you press a button — that's how Streamlit works. Every click triggers a full re-run of your Python script from line 1 to the last line, which means any regular variable gets reset to its initial value. Session state is like a sticky note on the side of the whiteboard that doesn't get erased during redraws. When you store something in st.session_state, it persists across reruns, so your game can remember the secret number, the player's score, and how many attempts they've made. Without session state, your app has amnesia — it forgets everything between interactions.

- What change did you make that finally gave the game a stable secret number?

  The fix was replacing the bare secret_number = random.randint(1, 100) with a session-state-guarded initialization: if "secret" not in st.session_state: st.session_state.secret = random.randint(low, high). The if check ensures the random number is only generated once — the very first time the app runs. On every subsequent rerun, the "secret" key already exists in session state, so the if block is skipped and the original number is preserved. The same pattern was applied to attempts, score, status, and history to give the entire game persistent state across interactions.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
- This could be a testing habit, a prompting strategy, or a way you used Git.

  I want to keep using the "debug expander" pattern — adding a collapsible section that shows internal state (st.session_state values, the secret number, attempt count, etc.) during development. This made it incredibly easy to verify whether bugs were fixed without having to guess or add print statements. Combined with writing small, focused pytest tests for pure logic functions, this gave me fast feedback on whether my changes actually worked. I also want to continue the habit of separating UI code from business logic so that the logic can be tested independently.
  
- What is one thing you would do differently next time you work with AI on a coding task?

  Next time I would verify every AI suggestion by reading the code line by line before accepting it, rather than assuming it's correct because it "looks right." The hint message bug (where the direction words are still swapped even though the outcome labels are correct) showed me that AI-generated fixes can be partially correct — they might fix the structural problem while introducing or preserving subtle logic errors. I would also write my tests first (or at least simultaneously), so I have an automated way to catch these issues instead of relying solely on manual testing.


- In one or two sentences, describe how this project changed the way you think about AI generated code.

  This project taught me that AI-generated code should be treated as a first draft, not a finished product. The original game was "generated by AI" and it shipped with fundamental bugs — backwards logic, no state management, and untestable architecture. Even when AI helped fix those bugs, the fixes weren't always 100% correct. AI is a powerful accelerator for writing code quickly, but it requires a human developer who understands the logic to review, test, and verify every change.

