from dataclasses import dataclass
from enum import Enum, auto

from typing import List, Tuple


class Player(Enum):
    BLUE = "blue"
    RED = "red"
    NONE = "none"


class GameState(Enum):
    WAITING_FOR_PLAYER = "waiting for player"
    IN_PROGRESS = "in progress"
    ENDED = "ended"


@dataclass
class Piece:
    is_master: bool
    colour: Player


@dataclass(eq=True, frozen=True)
class Pos:
    x: int
    y: int


@dataclass(eq=True, frozen=True)
class Card:
    name: str
    colour: Player
    moves: List[Pos]
    # moves = Positions the piece can move to using the card.
    # The piece is at (0, 0) and positions are relative to it.
