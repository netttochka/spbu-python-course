from project.game.src.card import Deck
from project.game.src.bot import Bot
from typing import List, Optional


class GameMeta(type):
    """
    Metaclass for the Game class to set default attributes.
    """

    def __new__(cls, name: str, bases: tuple, attrs: dict) -> type:
        """
        Creates a new Game class with default attributes.

        Args:
            cls (type): The metaclass itself.
            name (str): The name of the new class.
            bases (tuple): The base classes.
            attrs (dict): The class attributes.

        Returns:
            type: The newly created class.
        """
        attrs["target_score"] = attrs.get("target_score", 21)  # Set default value
        return super().__new__(cls, name, bases, attrs)


class Game(metaclass=GameMeta):
    """
    Represents a game that involves a deck of cards and bots.

    Attributes:
        deck (Deck): The deck of cards used in the game.
        bots (List[Bot]): The list of bots participating in the game.
        max_steps (int): The maximum number of rounds to play.
        current_step (int): The current round number.
        output_file (Optional[str]): The file to log game output.
        target_score (int): The target score to reach to win the game.
    """

    target_score: int

    def __init__(
        self,
        bots: List,
        max_steps: int = 10,
        output_file: Optional[str] = None,
        target_score: Optional[int] = None,
    ) -> None:
        """
        Initializes a Game instance.

        Args:
            bots (List[Bot]): A list of bots participating in the game.
            max_steps (int, optional): Maximum number of rounds to play. Defaults to 10.
            output_file (Optional[str], optional): File to log output. Defaults to None.
            target_score (Optional[int], optional): The target score to win. Defaults to the class default.
        """
        self._deck = Deck()
        self._bots = bots
        self._max_steps = max_steps
        self._current_step = 0
        self._output_file = output_file
        self.target_score = (
            target_score if target_score is not None else self.target_score
        )

    def _log(self, message: str) -> None:
        """
        Logs a message to the output file and prints it.

        Args:
            message (str): The message to log.
        """
        if self._output_file:
            with open(self._output_file, "a") as f:
                f.write(message + "\n")
        print(message)

    def _show_initial_state(self) -> None:
        """
        Logs the initial balance and current bet of each bot at the start of the game.
        """
        self._log("\n--- Initial Game State ---")
        for bot in self._bots:
            self._log(
                f"{bot._name}: Initial Balance = {bot._balance}, Initial Bet = {bot._current_bet}"
            )

    def _show_final_state(
        self, winner: Optional[Bot] = None, total_winnings: Optional[int] = None
    ) -> None:
        """
        Logs the final balance of each bot at the end of the game. If there is a winner, logs their winnings.

        Args:
            winner (Optional[Bot]): The winning bot, if any.
            total_winnings (Optional[int]): The total amount won by the winner.
        """
        self._log("\n--- Final Game State ---")
        for bot in self._bots:
            self._log(f"{bot._name}: Final Balance = {bot._balance}")

        if winner and total_winnings is not None:
            self._log(
                f"{winner._name} wins and receives {total_winnings} as total winnings."
            )

    def _show_state(self) -> None:
        """
        Displays the current state of the game, including scores and hands of all bots.
        """
        state = "\nCurrent game state:\n"
        for bot in self._bots:
            hand_cards = ", ".join(str(card) for card in bot._hand._cards)
            state += f"{bot._name} ({bot.__class__.__name__}) score: {bot._hand._calculate_score(self.target_score)} | Hand: [{hand_cards}]\n"
        self._log(state)

    def _play_round(self) -> None:
        """
        Plays a single round of the game, allowing each active bot to draw cards or stay.
        """
        self._log(f"\n--- Round {self._current_step + 1} ---")
        for bot in self._bots:
            if bot._is_active:  # Only active bots can take actions
                if bot._hand._calculate_score(self.target_score) < self.target_score:
                    if bot.decide():
                        card = self._deck._draw_card()
                        if card:
                            bot._hand._add_card(card)
                            self._log(f"{bot._name} draws {card}")
                        else:
                            self._log("Deck is empty!")
                    else:
                        self._log(
                            f"{bot._name} stays with score {bot._hand._calculate_score(self.target_score)}"
                        )
                else:
                    bot._is_active = False  # Bot is deactivated if score exceeds target
                    self._log(
                        f"{bot._name} stays with score {bot._hand._calculate_score(self.target_score)} (bust)"
                    )
        self._show_state()

    def determine_winner(self) -> Optional[Bot]:
        """
        Determines the winner of the game based on the scores of the bots.

        Returns:
            Optional[Bot]: The winning bot, or None if no winner is found.
        """
        valid_bots = [
            bot
            for bot in self._bots
            if bot._hand._calculate_score(self.target_score) <= self.target_score
        ]
        if not valid_bots:
            self._log("All bots bust. No winner.")
            return None

        # Winning condition: if one of the bots reaches the target score
        winner = next(
            (
                bot
                for bot in valid_bots
                if bot._hand._calculate_score(self.target_score) == self.target_score
            ),
            None,
        )

        # If no winner with the target score, choose the one with the highest score
        if not winner:
            winner = max(
                valid_bots,
                key=lambda bot: bot._hand._calculate_score(self.target_score),
            )

        return winner

    def _distribute_pot(self, winner: Bot) -> None:
        """
        Distributes the total bets to the winner.

        Args:
            winner (Bot): The winning bot.
        """
        total_bet = sum(
            bot._current_bet for bot in self._bots if bot != winner
        )  # Сумма ставок всех проигравших
        winner._balance += (
            total_bet  # Увеличение баланса победителя на сумму ставок остальных
        )

        # Уменьшаем баланс проигравших на их ставки
        for bot in self._bots:
            if bot != winner:
                bot._balance -= bot._current_bet

        # Сброс всех ставок
        for bot in self._bots:
            bot._current_bet = 0

    def _play_game(self) -> None:
        """Plays the game for the maximum number of steps or until a winner is found."""
        if self._output_file:
            open(
                self._output_file, "w"
            ).close()  # Clear the file before starting the game

        # Show initial balances and bets
        self._show_initial_state()

        while self._current_step < self._max_steps:
            self._play_round()
            self._current_step += 1

            # Check for active bots after each round
            active_bots = [bot for bot in self._bots if bot._is_active]

            # Check if there is only one active bot left
            if len(active_bots) == 1:
                winner = active_bots[0]
                self._log(f"Game over: {winner._name} wins as the last remaining bot!")
                self._distribute_pot(winner)
                self._show_final_state(winner=winner)
                return  # End the game

            # Check for a winner (reaching target score)
            if any(
                bot._hand._calculate_score(self.target_score) == self.target_score
                for bot in active_bots
            ):
                winner = next(
                    bot
                    for bot in active_bots
                    if bot._hand._calculate_score(self.target_score)
                    == self.target_score
                )
                self._log(
                    f"Game over: {winner._name} wins with {self.target_score} points!"
                )
                self._distribute_pot(winner)
                self._show_final_state(winner=winner)
                return  # End the game

        # Determine the winner after all rounds are over
        winner = self.determine_winner()
        if winner:
            self._log(
                f"Game over: {winner._name} wins with a score of {winner._hand._calculate_score(self.target_score)}!"
            )
            self._distribute_pot(winner)
        else:
            self._log("Game ended due to max steps without a winner.")

        # Show final state regardless of the outcome
        self._show_final_state(winner=winner)
