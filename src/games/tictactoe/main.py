import enum
from typing import List
from pydantic import BaseModel, validator, Field
import click
from subprocess import run


def generate_map(size) -> List[List]:
    return [[0 for _ in range(size)] for _ in range(size)]


class Move(BaseModel):
    player: int
    col: int
    row: int

    def to_coordinate(self) -> str:
        return chr(self.col + ord("A")) + chr(self.row + ord("1"))


class Map(BaseModel):
    game_map: List[List]
    size: int

    def __init__(self, *, size: int) -> None:
        super().__init__(size=size, game_map=generate_map(size))

    def move(self, m: Move):
        if m.col < 0 or m.col > self.size:
            raise ValueError("invalid coordinate: column")
        if m.row < 0 or m.row > self.size:
            raise ValueError("invalid coordinate: row")

        if self.game_map[m.row][m.col] != 0:
            raise ValueError("invalid coordinate: already filled")
        self.game_map[m.row][m.col] = m.player

    def print(self):
        for row in self.game_map:
            for col in row:
                c = "-"
                if col == 1:
                    c = "X"
                if col == 2:
                    c = "O"
                print(c, end=" ")
            print("")
        print("")

    def is_full(self):
        for row in self.game_map:
            for col in row:
                if col == 0:
                    return False
        return True

    def is_win(self) -> bool:
        return (
            self.check_row()
            or self.check_col()
            or self.check_diagonal_left()
            or self.check_diagonal_right()
        )

    def check_row(self) -> bool:
        for i in range(self.size):
            v = self.game_map[i][0]
            if v == 0:
                continue
            count = 1
            for j in range(1, self.size):
                if v != self.game_map[i][j]:
                    break
                count += 1
            if count == self.size:
                return True

    def check_col(self) -> bool:
        for i in range(self.size):
            v = self.game_map[0][i]
            if v == 0:
                continue
            count = 1
            for j in range(1, self.size):
                if v != self.game_map[j][i]:
                    break
                count += 1
            if count == self.size:
                return True

    def check_diagonal_left(self) -> bool:
        v = self.game_map[0][0]
        if v == 0:
            return False
        count = 1
        for i in range(1, self.size):
            if v != self.game_map[i][i]:
                break
            count += 1
        return count == self.size

    def check_diagonal_right(self) -> bool:
        v = self.game_map[0][self.size - 1]
        if v == 0:
            return False
        count = 1
        for i in range(1, self.size):
            if v != self.game_map[i][self.size - 1 - i]:
                break
            count += 1
        return count == self.size


class Data(BaseModel):
    moves: List[Move]
    timeout: int
    game_map: Map


def execute_script(data: Data, path: str, player: int) -> Move:
    moves = [m.player + "," + m.to_coordinate() for m in data.moves]
    args = ["python " + path + " --moves " + ";".join(moves)]

    res = run(args=args, capture_output=True, shell=True, timeout=data.timeout)
    lines = res.stdout.splitlines()
    if len(lines) == 0:
        raise ValueError("invalid coordinate: no result")

    coordinate = lines[0].decode("utf-8")

    if len(coordinate) != 2:
        raise ValueError("invalid coordinate: length must be 2")

    col = ord(coordinate[0]) - ord("A")
    row = ord(coordinate[1]) - ord("1")

    return Move(col=col, row=row, player=player)


SIZE = 3


@click.command()
@click.option("--path_bot1", type=click.Path(exists=True), help="path to bot1 script")
@click.option("--path_bot2", type=click.Path(exists=True), help="path to bot2 script")
@click.option("--timeout", default=500, help="timeout per move, default 500ms")
def main(path_bot1, path_bot2, timeout):
    data = Data(moves=[], timeout=timeout, game_map=Map(size=3))

    paths = [path_bot1, path_bot2]

    while True:
        for i, path in enumerate(paths):
            i = i + 1
            move = execute_script(data, path, i)
            data.game_map.move(move, player=i)
            if data.game_map.is_full():
                print("DRAW")
                break

            if data.game_map.is_win():
                print(f"PLAYER {i} WIN")
                break

            data.moves.append(move)


if __name__ == "__main__":
    main()
