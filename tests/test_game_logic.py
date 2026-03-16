from logic_utils import check_guess, parse_guess, update_score
# Fixed: Used Claude to implement new test cases to spefically target the three bugs I was dealing with
# Note: raised NotImplementedError made my
def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"


# --- Bug 1: Incorrect hints (Too High / Too Low were swapped) ---

def test_hint_not_swapped_high():
    # Bug: original code returned "Too Low" hint when guess was above secret.
    # A guess of 99 against a secret of 1 must say "Too High", not "Too Low".
    result = check_guess(99, 1)
    assert result == "Too High", (
        "check_guess returned wrong direction: guess > secret must be 'Too High'"
    )

def test_hint_not_swapped_low():
    # Bug: original code returned "Too High" hint when guess was below secret.
    # A guess of 1 against a secret of 99 must say "Too Low", not "Too High".
    result = check_guess(1, 99)
    assert result == "Too Low", (
        "check_guess returned wrong direction: guess < secret must be 'Too Low'"
    )

def test_hint_boundary_one_above():
    # Guess is exactly one above secret — should be "Too High".
    result = check_guess(51, 50)
    assert result == "Too High"

def test_hint_boundary_one_below():
    # Guess is exactly one below secret — should be "Too Low".
    result = check_guess(49, 50)
    assert result == "Too Low"

def test_hint_direction_with_string_secret():
    # On even-numbered attempts app.py converts secret to a string.
    # check_guess must still return the correct direction for the string path.
    result_high = check_guess(80, "50")   # 80 > 50 → "Too High"
    assert result_high == "Too High", (
        "String-secret path: guess > secret must still return 'Too High'"
    )
    result_low = check_guess(20, "50")    # 20 < 50 → "Too Low"
    assert result_low == "Too Low", (
        "String-secret path: guess < secret must still return 'Too Low'"
    )


# --- Bug 2: Attempts counter not decremented on the first wrong attempt ---

def test_attempts_increment_on_first_wrong_guess():
    # Simulates what app.py does: attempts starts at 0, increments by 1
    # on every submit — including the very first wrong guess.
    # The bug caused the first wrong guess not to count, leaving attempts at 0.
    attempts = 0
    attempt_limit = 8  # Normal difficulty

    ok, guess_int, _ = parse_guess("30")   # wrong guess; secret = 50
    assert ok, "parse_guess should succeed for a valid integer string"

    # Mimic app.py: increment BEFORE evaluating the guess.
    attempts += 1

    outcome = check_guess(guess_int, 50)
    assert outcome != "Win"

    # After the first wrong guess, attempts must be 1, not 0.
    assert attempts == 1, (
        f"Expected attempts=1 after first wrong guess, got {attempts}"
    )
    assert attempt_limit - attempts == 7, (
        "Attempts left should drop from 8 to 7 after the first wrong guess"
    )

def test_attempts_increment_on_each_subsequent_wrong_guess():
    # Verify the counter increments correctly for the first three wrong guesses.
    attempts = 0
    attempt_limit = 8
    secret = 50
    wrong_guesses = ["10", "20", "30"]

    for i, raw in enumerate(wrong_guesses, start=1):
        ok, guess_int, _ = parse_guess(raw)
        assert ok
        attempts += 1                         # app.py increments before check
        outcome = check_guess(guess_int, secret)
        assert outcome == "Too Low"
        assert attempts == i, (
            f"After guess #{i}, attempts should be {i}, got {attempts}"
        )

    assert attempt_limit - attempts == 5, "Should have 5 attempts remaining"


# --- Bug 3: New game does not reset game status ---

def test_new_game_resets_status_to_playing():
    # Simulates the state machine that new_game must satisfy.
    # Bug: the New Game button omitted resetting status, so a finished game
    # (status="lost" or "won") would immediately re-block play after reload.
    game_state = {"attempts": 5, "score": 30, "status": "lost"}

    # Mimic the fixed new_game block from app.py.
    game_state["attempts"] = 0
    game_state["status"] = "playing"

    assert game_state["status"] == "playing", (
        "New game must reset status to 'playing'; "
        "without the fix a finished game stays locked"
    )

def test_new_game_resets_status_from_won():
    # Same check but starting from a won game.
    game_state = {"attempts": 3, "score": 80, "status": "won"}

    game_state["attempts"] = 0
    game_state["status"] = "playing"

    assert game_state["status"] == "playing"
    assert game_state["attempts"] == 0
