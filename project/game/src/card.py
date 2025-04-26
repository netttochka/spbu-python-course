# project/game/src/card.py
"""
Card & Deck primitives for the blackjack-like game engine.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import ClassVar, List, Optional, Sequence


# ---------------------------------------------------------------------------#
#  Card
# ---------------------------------------------------------------------------#


@dataclass(slots=True, frozen=True)
class Card:
    """
    Immutable playing card.

    * rank* — 1 … 13  (Ace=1, Jack=11, Queen=12, King=13)
    * suit* — one of ``"Hearts" | "Diamonds" | "Clubs" | "Spades"``

    ``value`` свойство автоматически приравнивает все картинки к 10,
    что соответствует правилам блэкджека.
    """

    suit: str
    rank: int

    # Face-card map для красивого вывода
    _RANK_NAMES: ClassVar[dict[int, str]] = {
        1: "Ace",
        11: "Jack",
        12: "Queen",
        13: "King",
    }

    @property
    def value(self) -> int:  # noqa: D401 – already explicit
        """Numeric value used when подсчитывается очки руки."""
        return min(self.rank, 10)

    # ------------------------------------------------------------------ dunder

    def __str__(self) -> str:  # print(card) → 'Ace of Hearts'
        name = self._RANK_NAMES.get(self.rank, str(self.rank))
        return f"{name} of {self.suit}"

    def __repr__(self) -> str:  # repr(card) → 'Card("Hearts", 1)'
        return f"{type(self).__name__}({self.suit!r}, {self.rank})"


# ---------------------------------------------------------------------------#
#  Deck
# ---------------------------------------------------------------------------#


class Deck:
    """
    Standard 52-card deck.  Поддерживает::

        deck = Deck()          # авто-тасуется
        card = deck.draw()     # достать карту (или None, если колода пуста)
        len(deck)              # сколько карт осталось
    """

    suits: ClassVar[Sequence[str]] = ("Hearts", "Diamonds", "Clubs", "Spades")
    ranks: ClassVar[Sequence[int]] = range(1, 14)  # 1…13

    # ------------------------------------------------------------------ init

    def __init__(self, *, rng: Optional[random.Random] = None) -> None:
        """
        Создаёт полную колоду и перемешивает её.
        *rng* — опциональный генератор случайных чисел (удобно для тестов).
        """
        self._cards: List[Card] = [
            Card(suit, rank) for suit in self.suits for rank in self.ranks
        ]
        (rng or random).shuffle(self._cards)

    # ------------------------------------------------------------------ API

    def draw(self) -> Optional[Card]:
        """Возвращает верхнюю карту или ``None``, если колода пуста."""
        return self._cards.pop() if self._cards else None

    # alias для обратной совместимости с старым кодом/игровым движком
    _draw_card = draw

    # ------------------------------------------------------------------ helpers & dunder

    def shuffle(self, *, rng: Optional[random.Random] = None) -> None:
        """Перетасовать оставшиеся карты."""
        (rng or random).shuffle(self._cards)

    def __len__(self) -> int:  # len(deck)
        return len(self._cards)

    def __bool__(self) -> bool:  # bool(deck) → есть ли ещё карты
        return bool(self._cards)

    def __iter__(self):
        """Итерация по оставшимся картам без вынимания."""
        return iter(self._cards.copy())
