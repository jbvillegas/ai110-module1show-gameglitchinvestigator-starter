# FIXME: Original app.py had all logic inline with UI code, making it untestable.
# FIX: Refactored all core game logic into logic_utils.py using Claude Haiku 4.5
# so functions can be unit tested independently with pytest.


def get_range_for_difficulty(difficulty: str) -> tuple[int, int]:
    """Return (low, high) inclusive range for a given difficulty."""
    # FIX: Original had Hard at 1-50, easier than Normal's 1-100 — counterintuitive.
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 50
    if difficulty == "Hard":
        return 1, 1000
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    raw = str(raw).strip()
    if raw == "":
        return False, None, "Enter a guess."

    # FIX: Do not silently truncate decimals (e.g., "7.9" -> 7).
    if "." in raw:
        return False, None, "Please enter a whole number."

    try:
        value = int(raw)
    except ValueError:
        return False, None, "That is not a number."

    # FIX: Reject negative numbers and zero — game range always starts at 1.
    if value < 1:
        return False, None, "Please enter a positive number (1 or above)."

    return True, value, None


def check_guess(guess: int, secret: int):
    """
    Compare guess to secret and return (outcome, message).

    outcome: "Win", "Too High", or "Too Low"
    """
    if guess == secret:
        return "Win", "Correct!"

    # FIXME: Original starter code had hints BACKWARDS.
    # FIX: Too High => Go LOWER, Too Low => Go HIGHER.
    if guess > secret:
        return "Too High", "Go LOWER!"
    return "Too Low", "Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int) -> int:
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        return current_score + max(points, 10)

    # FIX: Penalize incorrect guesses consistently.
    if outcome in ("Too High", "Too Low"):
        return current_score - 5

    return current_score