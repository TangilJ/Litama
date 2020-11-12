from typing import List

from cards import ALL_BASE_CARDS
from game import Board
from structures import Player, Piece, Pos, Card


def board_to_str(b: Board) -> str:
    s = ""
    for row in b:
        for piece in row:
            if piece.color == Player.BLUE:
                s += "2" if piece.is_master else "1"
            elif piece.color == Player.RED:
                s += "4" if piece.is_master else "3"
            else:
                s += "0"
    return s


def str_to_board(s: str) -> Board:
    board: Board = [[Piece(False, Player.NONE) for _ in range(5)] for _ in range(5)]
    for i, n in enumerate(s):
        if n == "0":
            continue
        x = i % 5
        y = i // 5
        if n == "1" or n == "2":
            board[y][x].color = Player.BLUE
        if n == "3" or n == "4":
            board[y][x].color = Player.RED
        if n == "2" or n == "4":
            board[y][x].is_master = True
    return board


def notation_to_pos(s: str) -> Pos:
    return Pos(4 - (ord(s[0]) - 97), int(s[1]) - 1)


def get_card_from_name(name: str) -> Card:
    return next(filter(lambda x: x.name == name, ALL_BASE_CARDS))


def get_cards_from_names(names: List[str]) -> List[Card]:
    cards: List[Card] = []
    for name in names:
        cards.append(get_card_from_name(name))
    return cards
