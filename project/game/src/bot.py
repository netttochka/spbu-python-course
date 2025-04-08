from typing import List
from project.game.src.card import Card


class Hand:
    """Class representing a hand of cards for a bot or player."""

    def __init__(self) -> None:
        """Initializes an empty hand."""
        self._cards: List[Card] = []

    def _add_card(self, card: Card) -> None:
        """Adds a card to the hand."""
        self._cards.append(card)

    def _calculate_score(self, target_score: int = 21) -> int:
        """Calculates the score based on the cards in the hand."""
        score = sum(card._value for card in self._cards)
        aces = sum(1 for card in self._cards if card._rank == 1)
        while score <= target_score - 10 and aces:
            score += 10
            aces -= 1
        return score

    def _reset(self) -> None:
        """Clears the hand of all cards."""
        self._cards = []


class Bet:
    """Class representing a bet in the game."""

    def __init__(self, amount: float) -> None:
        """Initializes a bet with a given amount."""
        self._amount = amount


class BotMeta(type):
    """Metaclass for creating bots with different strategies."""

    def __new__(cls, name: str, bases: tuple, attrs: dict) -> type:
        strategy = attrs.get("strategy", None)

        if strategy == "conservative":
            attrs["decide"] = (
                lambda self, target_score=21: self._hand._calculate_score(target_score)
                < target_score - 5
            )
        elif strategy == "aggressive":
            attrs["decide"] = (
                lambda self, target_score=21: self._hand._calculate_score(target_score)
                < target_score - 2
            )
        elif strategy == "mixed":
            attrs["decide"] = (
                lambda self, target_score=21: self._hand._calculate_score(target_score)
                % 2
                == 0
            )
        elif strategy == "balanced":
            attrs["decide"] = (
                lambda self, target_score=21: self._hand._calculate_score(target_score)
                < target_score - 4
            )

        return super().__new__(cls, name, bases, attrs)


class Bot(metaclass=BotMeta):
    """Base class for bots in the game."""

    def __init__(self, name: str, bet_amount: float = 0.0) -> None:
        self._name = name
        self._balance = 1000
        self._hand = Hand()
        self._is_active = True
        self._current_bet = 0.0
        self._bet = Bet(bet_amount)
        self._place_bet(bet_amount)

    def _place_bet(self, amount: float) -> None:
        """Устанавливает ставку для бота."""
        if amount <= self._balance:  # Проверка, что у бота достаточно средств
            self._current_bet = amount
        else:
            raise ValueError("Insufficient balance to place the bet.")

    def _reset_hand(self) -> None:
        """Resets the bot's hand by clearing all cards."""
        self._hand._reset()


class ConservativeBot(Bot):
    """Bot that uses a conservative strategy."""

    strategy = "conservative"


class AggressiveBot(Bot):
    """Bot that uses an aggressive strategy."""

    strategy = "aggressive"


class MixedBot(Bot):
    """Bot that uses a mixed strategy."""

    strategy = "mixed"


class BalancedBot(Bot):
    """Bot that uses a balanced strategy."""

    strategy = "balanced"


class IntuitiveBot(Bot):
    """Bot that uses an intuitive strategy."""

    strategy = "intuitive"

    def decide(self, target_score: int = 21) -> bool:
        """Intuitive strategy decision making."""
        score = self._hand._calculate_score(target_score)
        total_cards = len(self._hand._cards)

        # Интуитивная стратегия: если у бота меньше 2 карт и его счет меньше 15, он будет брать карту
        if total_cards < 2 and score < 15:
            return True

        # Если у бота 2 карты и его счет меньше 17, он будет брать карту
        if total_cards == 2 and score < 17:
            return True

        # В противном случае, бот останется
        return False
