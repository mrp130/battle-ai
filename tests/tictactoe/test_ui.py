import pytest

from src.games.tictactoe.game import main


def test_ui():
    with pytest.raises(ValueError):
        main("bot1.py", "bot2.py", 500)
