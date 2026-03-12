from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score


def test_get_range_for_difficulty():
    assert get_range_for_difficulty("Easy") == (1, 20)
    assert get_range_for_difficulty("Normal") == (1, 50)
    assert get_range_for_difficulty("Hard") == (1, 1000)


def test_parse_guess_negative_validation():
    ok, value, err = parse_guess("-1")
    assert ok is False
    assert value is None
    assert "positive" in err.lower()


def test_parse_guess_zero_validation():
    ok, value, err = parse_guess("0")
    assert ok is False
    assert value is None
    assert "positive" in err.lower()


def test_parse_guess_rejects_decimal():
    ok, value, err = parse_guess("7.9")
    assert ok is False
    assert value is None
    assert "whole number" in err.lower()


def test_check_guess_directions():
    assert check_guess(9, 5) == ("Too High", "Go LOWER!")
    assert check_guess(1, 5) == ("Too Low", "Go HIGHER!")
    assert check_guess(5, 5) == ("Win", "Correct!")


def test_update_score_win_floor_and_penalty():
    assert update_score(0, "Win", 0) == 90
    assert update_score(0, "Win", 99) == 10
    assert update_score(20, "Too High", 2) == 15
    assert update_score(20, "Too Low", 2) == 15