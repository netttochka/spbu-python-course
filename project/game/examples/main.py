"""
Entry-point for a quick Blackjack simulation with three AI bots.

The script relies on the **refactored** modules (`game.py`, `bot.py`) we
introduced earlier.  Run it directly or import `run_demo()` from your own code.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from project.game.src.game import Game
from project.game.src.bot import ConservativeBot, AggressiveBot, MixedBot


def run_demo(output_file: Optional[str] = None) -> None:
    """
    Initialise three strategy bots and play a full game.

    Parameters
    ----------
    output_file:
        Path to a log file.  If *None*, all output is sent to `stdout`
        via the internal ``logging`` machinery.
    """
    bots = [
        ConservativeBot("Bot-Conservative", bet_amount=100.0),
        AggressiveBot("Bot-Aggressive", bet_amount=200.0),
        MixedBot("Bot-Mixed", bet_amount=100.0),
    ]

    # You can tweak *max_steps* or *target_score* as needed.
    game = Game(bots=bots, max_steps=10, output_file=output_file, target_score=21)
    game.play()  # public API replaces the old _play_game()


if __name__ == "__main__":
    # Logs will be stored under `examples/` next to the script.
    log_path = Path(__file__).with_suffix(".log")
    run_demo(output_file=str(log_path))
    print(f"Game finished – log written to: {log_path}")
