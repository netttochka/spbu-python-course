"""Bot implementations and the *Hand* helper used by the game engine."""

from __future__ import annotations

from typing import List

from project.game.src.card import Card

# ---------------------------------------------------------------------------
# Hand
# ---------------------------------------------------------------------------


class Hand:
    """A mutable collection of :class:`Card` objects held by a player."""

    __slots__ = ("_cards",)

    def __init__(self) -> None:
        self._cards: List[Card] = []

    # ------------------------------------------------------------------ API

    @property
    def cards(self) -> List[Card]:
        """Return a **copy** of the internal card list."""
        return self._cards.copy()

    def add_card(self, card: Card) -> None:
        """Append *card* to the hand."""
        self._cards.append(card)

    # Backwards‑compatibility alias (old code called ``_add_card``)
    _add_card = add_card

    def calculate_score(self, target_score: int = 21) -> int:
        """Return the blackjack‑style score for this hand.

        Aces are initially counted as ``1`` but can be promoted to ``11`` if
        this does **not** cause the total to exceed *target_score*.
        """

        score = sum(c.value for c in self._cards)
        aces = sum(1 for c in self._cards if c.rank == 1)

        while aces and score <= target_score - 10:
            score += 10  # upgrade Ace → 11
            aces -= 1
        return score

    _calculate_score = calculate_score  # legacy alias

    def reset(self) -> None:
        """Remove **all** cards from the hand."""
        self._cards.clear()

    _reset = reset  # legacy alias


# ---------------------------------------------------------------------------
# Bet
# ---------------------------------------------------------------------------


class Bet:
    """Simple value object that stores a wager amount."""

    __slots__ = ("amount",)

    def __init__(self, amount: float) -> None:
        if amount < 0:
            raise ValueError("Bet amount must be non‑negative")
        self.amount = amount


# ---------------------------------------------------------------------------
# Bot & strategies
# ---------------------------------------------------------------------------


class BotMeta(type):
    """Metaclass that injects a :pymeth:`Bot.decide` method based on *strategy*."""

    def __new__(cls, name: str, bases: tuple[type, ...], attrs: dict):  # type: ignore[override]
        strategy = attrs.get("strategy")

        def _build(delta: int):
            return (
                lambda self, target_score=21: self.hand.calculate_score(target_score)
                < target_score - delta
            )

        if strategy == "conservative":
            attrs["decide"] = _build(5)  # hit while < 16
        elif strategy == "aggressive":
            attrs["decide"] = _build(2)  # hit while < 19
        elif strategy == "mixed":
            attrs["decide"] = (
                lambda self, target_score=21: self.hand.calculate_score(target_score)
                % 2
                == 0
            )
        elif strategy == "balanced":
            attrs["decide"] = _build(4)  # hit while < 17
        # Custom subclasses may define their own decide().

        return super().__new__(cls, name, bases, attrs)


class Bot(metaclass=BotMeta):
    """Base class for autonomous players compatible with :class:`Game`."""

    # Public attributes expected by :pyclass:`Game.BotProtocol`
    name: str
    balance: int
    current_bet: float
    is_active: bool
    hand: Hand

    def __init__(self, name: str, bet_amount: float = 0.0) -> None:
        self.name = name
        self.balance = 1000
        self.hand = Hand()
        self.is_active = True
        self.current_bet = 0.0

        # Legacy underscored aliases to avoid breaking older code paths
        self._name = self.name
        self._balance = self.balance
        self._hand = self.hand
        self._is_active = self.is_active
        self._current_bet = self.current_bet

        self._bet = Bet(bet_amount)
        self.place_bet(bet_amount)

    # ------------------------------------------------------------------ banking

    def place_bet(self, amount: float) -> None:
        """Reserve *amount* from the player's balance for the current round."""
        if amount < 0:
            raise ValueError("Bet amount must be non‑negative")
        if amount > self.balance:
            raise ValueError("Insufficient balance to place the bet")

        self.current_bet = amount
        self._current_bet = amount  # keep alias in sync

    _place_bet = place_bet  # legacy alias

    # ------------------------------------------------------------------ helpers

    def reset_hand(self) -> None:
        """Clear the current hand and reactivate the player."""
        self.hand.reset()
        self.is_active = True
        self._is_active = True

    _reset_hand = reset_hand

    # ------------------------------------------------------------------ gameplay

    def decide(
        self, target_score: int = 21
    ) -> bool:  # noqa: D401 – override in subclasses or metaclass
        """Default behaviour: take a card while score < 17."""
        return self.hand.calculate_score(target_score) < 17


# ---------------------------------------------------------------------------
# Ready‑made strategy subclasses
# ---------------------------------------------------------------------------


class ConservativeBot(Bot):
    """Bot that plays very cautiously."""

    strategy = "conservative"


class AggressiveBot(Bot):
    """Bot that keeps hitting until the score is high."""

    strategy = "aggressive"


class MixedBot(Bot):
    """Bot that bases its decision on score parity."""

    strategy = "mixed"


class BalancedBot(Bot):
    """Bot with a middle‑ground risk profile."""

    strategy = "balanced"


class IntuitiveBot(Bot):
    """Bot that tries to mimic a simple human‑like intuition."""

    strategy = "intuitive"

    def decide(self, target_score: int = 21) -> bool:  # type: ignore[override]
        score = self.hand.calculate_score(target_score)
        total_cards = len(self.hand.cards)

        # If holding < 2 cards and score < 15 → hit
        if total_cards < 2 and score < 15:
            return True
        # If exactly 2 cards and score < 17 → hit
        if total_cards == 2 and score < 17:
            return True
        return False
