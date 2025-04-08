from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pytest
from project.game.src.game import Game
from project.game.src.bot import (
    Bot,
    ConservativeBot,
    AggressiveBot,
    MixedBot,
    IntuitiveBot,
)
from project.game.src.card import Card, Deck


@pytest.fixture
def setup_game():
    bots = [ConservativeBot("Bot1"), AggressiveBot("Bot2"), MixedBot("Bot3")]
    game = Game(bots, max_steps=5)
    return game


def test_initial_state(setup_game):
    game = setup_game
    assert game._current_step == 0
    assert isinstance(game._deck, Deck)


def test_bot_decision(setup_game):
    game = setup_game
    for bot in game._bots:
        bot._hand._add_card(game._deck._draw_card())
        bot._hand._add_card(game._deck._draw_card())
        assert bot.decide() in [True, False]


def test_play_round(setup_game):
    game = setup_game
    game._play_game()
    assert game._current_step > 0


def test_bot_scores(setup_game):
    game = setup_game
    for bot in game._bots:
        bot._hand._add_card(game._deck._draw_card())
        bot._hand._add_card(game._deck._draw_card())

    for bot in game._bots:
        score = bot._hand._calculate_score()
        assert score >= 0


def test_bust_condition(setup_game):
    game = setup_game
    bot = game._bots[0]
    bot._hand._add_card(Card("Hearts", 10))
    bot._hand._add_card(Card("Diamonds", 10))
    bot._hand._add_card(Card("Clubs", 2))

    assert bot._hand._calculate_score() > 21


def test_winner_determination(setup_game):
    game = setup_game
    game._bots[0]._hand._add_card(Card("Hearts", 10))
    game._bots[0]._hand._add_card(Card("Diamonds", 8))
    game._bots[1]._hand._add_card(Card("Clubs", 10))
    game._bots[1]._hand._add_card(Card("Spades", 7))
    game._bots[2]._hand._add_card(Card("Hearts", 10))
    game._bots[2]._hand._add_card(Card("Diamonds", 9))

    winner = game.determine_winner()
    assert winner == game._bots[2]


def test_game_over_condition(setup_game):
    game = setup_game
    game._current_step = game._max_steps
    winner = game.determine_winner()
    assert winner is not None


def test_conservative_bot_decision():
    bot = ConservativeBot("TestBot")
    bot._hand._add_card(Card("Hearts", 10))
    bot._hand._add_card(Card("Diamonds", 5))
    assert bot.decide()

    bot._hand._reset()
    bot._hand._add_card(Card("Hearts", 10))
    bot._hand._add_card(Card("Diamonds", 7))
    assert not bot.decide()


def test_aggressive_bot_decision():
    bot = AggressiveBot("AggressiveBot")
    bot._hand._add_card(Card("Hearts", 10))
    bot._hand._add_card(Card("Spades", 8))
    assert bot.decide()

    bot._hand._add_card(Card("Clubs", 2))
    assert not bot.decide()


def test_mixed_bot_decision():
    bot = MixedBot("MixedBot")
    bot._hand._add_card(Card("Hearts", 3))
    bot._hand._add_card(Card("Diamonds", 5))
    assert bot.decide()

    bot._hand._add_card(Card("Spades", 2))
    assert bot.decide()

    bot._hand._add_card(Card("Clubs", 1))
    assert not bot.decide()


def test_default_target_score():
    game = Game(bots=[], max_steps=5)
    assert game.target_score == 21


def test_custom_target_score():
    game = Game(bots=[], max_steps=5, target_score=15)
    assert game.target_score == 15


def test_game_initialization():
    bots = [ConservativeBot("Bot1"), AggressiveBot("Bot2")]
    game = Game(bots=bots, max_steps=10)
    assert game._bots == bots
    assert game._max_steps == 10


@pytest.fixture
def example_bots():
    return [ConservativeBot("Bot1"), AggressiveBot("Bot2"), MixedBot("Bot3")]


def test_game_target_score_change(example_bots):
    new_target_score = 25
    game = Game(example_bots, max_steps=10, target_score=new_target_score)
    assert game.target_score == new_target_score


def test_game_default_target_score(example_bots):
    game = Game(example_bots, max_steps=10)
    assert game.target_score == 21


def test_bot_strategy_metaclass():
    class BalancedBot(Bot):
        """Bot that uses a balanced strategy."""

        strategy = "balanced"

    balanced_bot = BalancedBot("BalancedBot")
    assert balanced_bot.strategy == "balanced"
    balanced_bot._hand._add_card(Card("Hearts", 5))
    balanced_bot._hand._add_card(Card("Diamonds", 5))
    assert balanced_bot.decide() == (balanced_bot._hand._calculate_score() < 17)


@pytest.mark.parametrize(
    "bot_class, strategy, expected_decision",
    [
        (ConservativeBot, "conservative", lambda score: score < 16),
        (AggressiveBot, "aggressive", lambda score: score < 19),
        (MixedBot, "mixed", lambda score: score % 2 == 0),
    ],
)
def test_bot_decide_methods(bot_class, strategy, expected_decision):
    bot = bot_class("TestBot")
    bot._hand._add_card(Card("Hearts", 5))
    bot._hand._add_card(Card("Diamonds", 5))
    assert bot.strategy == strategy
    assert bot.decide() == expected_decision(bot._hand._calculate_score())


def test_intuitive_bot_decision():
    bot = IntuitiveBot("IntuitiveBot")

    # Ситуация 1: менее 2 карт и счет меньше 15
    bot._hand._add_card(Card("Hearts", 5))
    assert bot.decide()

    # Ситуация 2: 2 карты и счет меньше 17
    bot._hand._add_card(Card("Diamonds", 9))
    assert bot.decide()

    # Ситуация 3: 2 карты и счет равен 17
    bot._hand._add_card(Card("Clubs", 3))  # Счет теперь 17
    assert not bot.decide()

    # Ситуация 4: более 2 карт и счет меньше 21
    bot._hand._add_card(Card("Spades", 2))  # Счет 19
    assert not bot.decide()

    # Ситуация 5: более 2 карт и счет больше 21
    bot._hand._add_card(Card("Diamonds", 5))  # Счет 24 (перебор)
    assert not bot.decide()


def test_bot_bets(setup_game):
    game = setup_game

    # Проверка начальных балансов
    initial_balances = {bot._name: bot._balance for bot in game._bots}

    # Устанавливаем ставки
    for bot in game._bots:
        bet_amount = 100  # Пример ставки
        bot._place_bet(bet_amount)
        assert bot._current_bet == bet_amount  # Проверка, что ставка установлена

    # Предположим, что победил первый бот
    winner = game._bots[0]
    game._distribute_pot(winner)

    # Суммируем ставки проигравших ботов
    total_bet = 200

    # Проверка, что у победителя увеличился баланс на сумму ставок всех проигравших
    assert winner._balance == initial_balances[winner._name] + total_bet

    # Проверка, что у остальных ботов баланс уменьшился на их ставки
    for bot in game._bots[1:]:
        assert bot._balance == initial_balances[bot._name] - 100

    # Сброс ставок
    for bot in game._bots:
        assert bot._current_bet == 0  # Ставки должны быть сброшены
