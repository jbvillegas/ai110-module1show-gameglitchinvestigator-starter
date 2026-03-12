import pytest
from logic_utils import parse_guess, check_guess, update_score

# Basic parse_guess tests
def test_parse_valid_integer():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None

def test_parse_empty_string():
    ok, value, err = parse_guess("")
    assert ok is False
    assert err is not None

def test_parse_non_numeric():
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert err is not None

def test_parse_decimal():
    """Decimal input should be rejected (whole numbers only)."""
    ok, value, err = parse_guess("3.7")
    assert ok is False
    assert err is not None

def test_parse_negative():
    ok, value, err = parse_guess("-5")
    assert ok is False
    assert err is not None

# check_guess tests — returns (outcome, message) tuple
def test_check_guess_correct():
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"

def test_check_guess_too_high():
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"

def test_check_guess_too_low():
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"

# update_score tests — signature: update_score(current_score, outcome, attempt_number)
def test_update_score_increases():
    new_score = update_score(10, outcome="Win", attempt_number=1)
    assert new_score > 10

def test_update_score_decreases_on_wrong():
    new_score = update_score(10, outcome="Too High", attempt_number=1)
    assert new_score < 10