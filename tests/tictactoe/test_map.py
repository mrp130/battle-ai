from src.games.tictactoe.main import Map, Move


def test_win_diagonal_left():
    m = Map(size=3)
    m.move(Move(col=1, row=1, player=1))
    assert m.is_win() is False
    m.move(Move(col=2, row=2, player=1))
    assert m.is_win() is False
    m.move(Move(col=0, row=0, player=1))
    assert m.is_win() is True


def test_win_diagonal_right():
    m = Map(size=3)
    m.move(Move(col=2, row=0, player=1))
    assert m.is_win() is False
    m.move(Move(col=1, row=1, player=1))
    assert m.is_win() is False
    m.move(Move(col=0, row=2, player=1))
    assert m.is_win() is True


def test_win_col():
    m = Map(size=3)
    m.move(Move(col=1, row=0, player=1))
    assert m.is_win() is False
    m.move(Move(col=1, row=1, player=1))
    assert m.is_win() is False
    m.move(Move(col=1, row=2, player=1))
    assert m.is_win() is True


def test_win_row():
    m = Map(size=3)
    m.move(Move(col=1, row=1, player=1))
    assert m.is_win() is False
    m.move(Move(col=2, row=1, player=1))
    assert m.is_win() is False
    m.move(Move(col=0, row=1, player=1))
    assert m.is_win() is True
