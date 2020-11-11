import random
from typing import List, Tuple, Optional

from cards import ALL_BASE_CARDS
from structures import Piece, Pos, Card, Player

Board = List[List[Piece]]


def init_game() -> Tuple[Board, List[Card], List[Card], Card]:
    board: Board = [[Piece(False, Player.NONE) for _ in range(5)] for _ in range(5)]

    for x, y in [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]:
        board[y][x].colour = Player.BLUE
    board[0][2].is_master = True

    for x, y in [(0, 4), (1, 4), (2, 4), (3, 4), (4, 4)]:
        board[y][x].colour = Player.RED
    board[4][2].is_master = True

    random_cards = random.sample(ALL_BASE_CARDS, 5)
    blue_cards = random_cards[:2]
    red_cards = random_cards[2:4]
    side_card = random_cards[4]

    return board, blue_cards, red_cards, side_card


def print_board(b: Board) -> None:
    ret: str = ""
    for y in range(5):
        for x in range(5):
            if b[y][x].colour == Player.NONE:
                ret += "•"
            else:
                if b[y][x].colour == 0:
                    ret += "B" if b[y][x].is_master else "b"
                else:
                    ret += "R" if b[y][x].is_master else "r"
            ret += " "
        ret += f" {chr(y + 65)}\n"
    ret += "1 2 3 4 5"
    print(ret)


def print_game(b: Board, blue_cards: List[Card], red_cards: List[Card], side_card: Card) -> None:
    print_board(b)
    print(f"Blue: {' '.join(i.name for i in blue_cards)}")
    print(f"Red: {' '.join(i.name for i in red_cards)}")
    print(f"Side: {side_card.name}")


def clone_board(board: Board) -> Board:
    new_board: Board = []
    for y in board:
        new_board.append([])
        for x in y:
            new_board[-1].append(Piece(x.is_master, x.colour))

    return new_board


def generate_moves_for_piece(piece_pos: Pos, cards: List[Card], b: Board) -> List[Tuple[Pos, Card]]:
    piece: Piece = b[piece_pos.y][piece_pos.x]
    moves: List[Tuple[Pos, Card]] = []
    # Each element in moves is a tuple.
    # The tuple contains the position that the move would lead to and the card used for that move.

    for card in cards:
        for move in card.moves:
            # Account for card rotation on both sides
            # On blue side, negative X goes right
            # On red side, negative Y goes up
            x = (-move.x if piece.colour == Player.BLUE else move.x) + piece_pos.x
            y = (-move.y if piece.colour == Player.RED else move.y) + piece_pos.y
            if 0 > x or x > 4 or 0 > y or y > 4:
                continue
            if b[y][x].colour != Player.NONE and b[y][x].colour == piece.colour:
                continue

            moves.append((Pos(x, y), card))

    return moves


def apply_move(piece_pos: Pos,
               move_pos: Pos, move_card: Card,
               cards: List[Card], b: Board) -> Optional[Board]:
    generated_moves = generate_moves_for_piece(piece_pos, cards, b)
    if (move_pos, move_card) not in generated_moves:
        return None
    cloned: Board = clone_board(b)
    cloned[move_pos.y][move_pos.x].colour = cloned[piece_pos.y][piece_pos.x].colour
    cloned[move_pos.y][move_pos.x].is_master = cloned[piece_pos.y][piece_pos.x].is_master
    cloned[piece_pos.y][piece_pos.x].colour = Player.NONE
    return cloned


def check_win_condition(b: Board) -> Player:
    blue_master_exists = False
    red_master_exists = False
    for row in b:
        for piece in row:
            if piece.is_master and piece.colour == Player.BLUE:
                blue_master_exists = True
            if piece.is_master and piece.colour == Player.RED:
                red_master_exists = True
    if not blue_master_exists:
        return Player.RED
    if not red_master_exists:
        return Player.BLUE

    if b[0][2].is_master and b[0][2].colour == Player.RED:
        return Player.RED
    if b[4][2].is_master and b[4][2].colour == Player.BLUE:
        return Player.BLUE

    return Player.NONE
