import random
from typing import Optional, List


class Card:
    """
    Represents a playing card with a suit and rank.

    Attributes:
        suit (str): The suit of the card (e.g., Hearts, Diamonds).
        rank (int): The rank of the card (1-13, where 1 is Ace, 11 is Jack, 12 is Queen, 13 is King).
        value (int): The value of the card for the game, where ranks higher than 10 are valued at 10.
    """

    def __init__(self, suit: str, rank: int) -> None:
        """
        Initializes a Card instance.

        Args:
            suit (str): The suit of the card.
            rank (int): The rank of the card.
        """
        self._suit = suit
        self._rank = rank
        self._value = min(rank, 10)  # Cards with rank > 10 are valued as 10

    def __repr__(self) -> str:
        """
        Returns a string representation of the Card.

        Returns:
            str: A string in the format "<rank> of <suit>".
        """
        return f"{self._rank} of {self._suit}"


class Deck:
    """
    Represents a deck of playing cards.

    Attributes:
        suits (List[str]): The list of suits in the deck.
        ranks (List[int]): The list of ranks in the deck.
        cards (List[Card]): The list of Card instances in the deck.
    """

    suits: List[str] = ["Hearts", "Diamonds", "Clubs", "Spades"]
    ranks: List[int] = list(
        range(1, 14)
    )  # Aces (1), numbers (2-10), and face cards (11-13)

    def __init__(self) -> None:
        """
        Initializes a Deck instance, creates a full deck of cards, and shuffles them.
        """
        self._cards: List[Card] = [
            Card(suit, rank) for suit in Deck.suits for rank in Deck.ranks
        ]
        random.shuffle(self._cards)

    def _draw_card(self) -> Optional[Card]:
        """
        Draws a card from the deck.

        Returns:
            Optional[Card]: The drawn Card, or None if the deck is empty.
        """
        return self._cards.pop() if self._cards else None
