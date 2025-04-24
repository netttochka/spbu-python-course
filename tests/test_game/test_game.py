"""
End‑to‑end and unit tests for the blackjack engine.

These tests target the *refactored* versions of ``game.py``, ``bot.py`` and
``card.py``.  They exercise core behaviour – initialisation, per‑round logic,
strategy decisions and pot distribution – without relying on the internal
implementation details that changed during the rewrite.
"""

from __future__ import annotations

from pathlib import Path
import sys
from typing import List, Type

import pytest

# Ensure the project root is on *sys.path* when the tests are executed in‑place
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ---------------------------------------------------------------------------
# Local imports (after path tweak so that the work‑in‑progress modules resolve)
# ---------------------------------------------------------------------------

from project.game.src.game import Game  # noqa: E402 – path hack above
from project.game.src.bot import (
    Bot,
    ConservativeBot,
    AggressiveBot,
    MixedBot,
    IntuitiveBot,
)
from project.game.src.card import Card, Deck  # noqa: E402

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def example_game() -> Game:
    """Provide a small game instance with three bots for quick tests."""

    bots = [ConservativeBot("Bot1"), AggressiveBot("Bot2"), MixedBot("Bot3")]
    return Game(bots=bots, max_steps=5)


# ---------------------------------------------------------------------------
# Basic construction
# ---------------------------------------------------------------------------


def test_initial_state(example_game: Game) -> None:
    """Game starts at round 0 with a non‑empty deck."""

    assert example_game._current_step == 0  # internal counter should be zero
    assert isinstance(example_game._deck, Deck)
    assert len(example_game._deck) == 52


# ---------------------------------------------------------------------------
# Bot decisions & strategy lambdas
# ---------------------------------------------------------------------------


def test_bot_decision(example_game: Game) -> None:
    """Each bot returns a boolean from ``decide()`` under normal conditions."""

    for bot in example_game._bots:
        bot._hand._add_card(example_game._deck._draw_card())  # legacy alias still OK
        bot._hand._add_card(example_game._deck._draw_card())
        assert bot.decide() in (True, False)


# ---------------------------------------------------------------------------
# Game loop integration
# ---------------------------------------------------------------------------


def test_play_game_advances_rounds(example_game: Game) -> None:
    """Running :py:meth:`Game.play` must advance the internal step counter."""

    example_game.play()
    assert example_game._current_step > 0


# ---------------------------------------------------------------------------
# Hand score logic
# ---------------------------------------------------------------------------


def test_hand_scoring(example_game: Game) -> None:
    """Score should always be non‑negative after adding cards."""

    for bot in example_game._bots:
        bot._hand._add_card(example_game._deck._draw_card())
        bot._hand._add_card(example_game._deck._draw_card())
        assert bot._hand._calculate_score() >= 0


def test_bust_condition() -> None:
    """Three high‑value cards should result in a bust (>21)."""

    hand_bot = ConservativeBot("Buster")
    hand_bot._hand._add_card(Card("Hearts", 10))
    hand_bot._hand._add_card(Card("Diamonds", 10))
    hand_bot._hand._add_card(Card("Clubs", 2))
    assert hand_bot._hand._calculate_score() > 21


# ---------------------------------------------------------------------------
# Strategy‑specific behaviour
# ---------------------------------------------------------------------------


def test_conservative_bot_decision() -> None:
    bot = ConservativeBot("ConBot")
    bot._hand._add_card(Card("Hearts", 10))
    bot._hand._add_card(Card("Diamonds", 5))
    assert bot.decide()  # score 15 → hit

    bot._hand._reset()
    bot._hand._add_card(Card("Hearts", 10))
    bot._hand._add_card(Card("Diamonds", 7))
    assert not bot.decide()  # score 17 → stay


def test_aggressive_bot_decision() -> None:
    bot = AggressiveBot("Aggro")
    bot._hand._add_card(Card("Hearts", 10))
    bot._hand._add_card(Card("Spades", 8))  # 18
    assert bot.decide()

    bot._hand._add_card(Card("Clubs", 2))  # 20
    assert not bot.decide()


def test_mixed_bot_decision() -> None:
    bot = MixedBot("Mixer")
    bot._hand._add_card(Card("Hearts", 3))
    bot._hand._add_card(Card("Diamonds", 5))  # 8 even
    assert bot.decide()

    bot._hand._add_card(Card("Spades", 2))  # 10 even
    assert bot.decide()

    bot._hand._add_card(Card("Clubs", 1))  # 11 odd
    assert not bot.decide()


# ---------------------------------------------------------------------------
# Target score handling
# ---------------------------------------------------------------------------


def test_default_target_score() -> None:
    assert Game(bots=[], max_steps=1).target_score == 21


def test_custom_target_score() -> None:
    assert Game(bots=[], max_steps=1, target_score=15).target_score == 15


# ---------------------------------------------------------------------------
# Game initialisation basics
# ---------------------------------------------------------------------------


def test_game_initialisation() -> None:
    bots: List[Bot] = [ConservativeBot("B1"), AggressiveBot("B2")]
    game = Game(bots=bots, max_steps=10)
    assert game._bots == bots
    assert game._max_steps == 10


# ---------------------------------------------------------------------------
# Fixture for multiple tests below
# ---------------------------------------------------------------------------


@pytest.fixture
def populated_bots() -> List[Bot]:
    return [ConservativeBot("C1"), AggressiveBot("A1"), MixedBot("M1")]


# ---------------------------------------------------------------------------
# Dynamic target score
# ---------------------------------------------------------------------------


def test_game_target_score_change(populated_bots: List[Bot]):
    new_target = 25
    game = Game(populated_bots, max_steps=10, target_score=new_target)
    assert game.target_score == new_target


def test_game_default_target_score(populated_bots: List[Bot]):
    assert Game(populated_bots, max_steps=10).target_score == 21


# ---------------------------------------------------------------------------
# Metaclass‑generated strategy logic
# ---------------------------------------------------------------------------


def test_balanced_bot_strategy():
    class BalancedBot(Bot):
        strategy = "balanced"

    bal_bot = BalancedBot("Bal")
    bal_bot._hand._add_card(Card("Hearts", 5))
    bal_bot._hand._add_card(Card("Diamonds", 5))
    expected = bal_bot._hand._calculate_score() < 17
    assert bal_bot.decide() is expected


@pytest.mark.parametrize(
    "bot_cls, strategy, predicate",
    [
        (ConservativeBot, "conservative", lambda s: s < 16),
        (AggressiveBot, "aggressive", lambda s: s < 19),
        (MixedBot, "mixed", lambda s: s % 2 == 0),
    ],
)
def test_bot_decide_methods(bot_cls: Type[Bot], strategy: str, predicate):
    bot = bot_cls("Test")
    bot._hand._add_card(Card("Hearts", 5))
    bot._hand._add_card(Card("Diamonds", 5))
    assert bot.strategy == strategy
    assert bot.decide() is predicate(bot._hand._calculate_score())


# ---------------------------------------------------------------------------
# IntuitiveBot bespoke logic
# ---------------------------------------------------------------------------


def test_intuitive_bot_decision():
    bot = IntuitiveBot("IBot")

    # Case 1 – fewer than two cards & score < 15 → hit
    bot._hand._add_card(Card("Hearts", 5))
    assert bot.decide()

    # Case 2 – exactly two cards & score < 17 → hit
    bot._hand._add_card(Card("Diamonds", 9))
    assert bot.decide()

    # Case 3 – two cards & score == 17 → stay
    bot._hand._add_card(Card("Clubs", 3))  # now 17
    assert not bot.decide()

    # Case 4 – >2 cards & score < 21 → stay
    bot._hand._add_card(Card("Spades", 2))  # 19
    assert not bot.decide()

    # Case 5 – bust (>21) → stay
    bot._hand._add_card(Card("Diamonds", 5))  # 24
    assert not bot.decide()
