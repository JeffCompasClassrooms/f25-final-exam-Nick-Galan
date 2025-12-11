import pytest
import string
from brute import Brute


def describe_brute():

    @pytest.fixture
    def cracker():
        return Brute("TDD")

    def describe_bruteOnce():

        def true_when_attempt_matches_target(cracker):
            # returns True when guess matches
            assert cracker.bruteOnce("TDD") is True

        def false_when_attempt_does_not_match_target(cracker):
            # returns False when guess is wrong
            assert cracker.bruteOnce("wrong") is False

        def case_sensitive(cracker):
            # matching is case-sensitive
            assert cracker.bruteOnce("tdd") is False

        def handles_empty_secret_string():
            # empty string only matches empty
            empty_cracker = Brute("")
            assert empty_cracker.bruteOnce("") is True
            assert empty_cracker.bruteOnce("a") is False

    def describe_bruteMany():

        @pytest.fixture
        def mock_cracker(mocker):
            # stub guesses for deterministic behavior
            mock_brute = Brute("TDD")
            mocker.patch.object(mock_brute, "randomGuess", side_effect=["TDD", "wrong"])
            return mock_brute

        def it_returns_time_to_crack_when_successful(mock_cracker):
            # returns time > 0 on success
            time_taken = mock_cracker.bruteMany(limit=10)
            assert time_taken > 0

        def it_returns_negative_one_when_unsuccessful(mocker):
            # returns -1 when never cracked
            mock_brute = Brute("TDD")
            mocker.patch.object(mock_brute, "randomGuess", return_value="wrong")
            result = mock_brute.bruteMany(limit=10)
            assert result == -1

        def it_verifies_bruteOnce_is_called_with_generated_guess(mock_cracker, mocker):
            # ensures bruteOnce is called with the guessed string
            mock_brute_once = mocker.patch.object(mock_cracker, "bruteOnce", return_value=True)
            mock_cracker.randomGuess.return_value = "TDD"
            mock_cracker.bruteMany(limit=1)
            mock_brute_once.assert_called_with("TDD")

        def it_calls_hash_and_randomGuess_for_each_attempt_until_failure(mocker):
            # loops correctly through attempts until limit reached
            brute = Brute("TDD")

            def stub_hash(s):
                return brute.target + "x"

            hash_stub = mocker.patch.object(brute, "hash", side_effect=stub_hash)
            guess_mock = mocker.patch.object(brute, "randomGuess", return_value="anything")

            result = brute.bruteMany(limit=4)

            assert result == -1
            assert hash_stub.call_count == 4
            assert guess_mock.call_count == 4

    def describe_randomGuess():

        def it_generates_a_string_within_the_expected_length_range(cracker):
            # length between 1 and 8
            guess = cracker.randomGuess()
            assert 1 <= len(guess) <= 8

        def it_generates_strings_with_valid_characters(cracker):
            # only letters and digits
            guess = cracker.randomGuess()
            valid_chars = string.ascii_letters + string.digits
            assert all(c in valid_chars for c in guess)
