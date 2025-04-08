from project.game.src.game import Game
from project.game.src.bot import ConservativeBot, AggressiveBot, MixedBot
from typing import Optional


def main(output_file: Optional[str] = None) -> None:
    """
    Initializes and runs a Blackjack game with three different types of bots.

    Args:
        output_file (Optional[str], optional): The file path to which the game output will be saved.
                                               If None, the output will not be saved.
    """

    bots = [
        ConservativeBot("Bot1", 100.0),
        AggressiveBot("Bot2", 200.0),
        MixedBot("Bot3", 100.0),
    ]

    game = Game(bots, max_steps=10, output_file=output_file, target_score=21)
    game._play_game()


if __name__ == "__main__":
    main(output_file="project/game/examples/example_run.txt")
