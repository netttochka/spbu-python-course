import logging
from typing import List, Optional, Protocol, runtime_checkable, Iterable

from project.game.src.card import Deck
from project.game.src.bot import Bot  # type: ignore  # kept for runtime import

__all__ = ["Game", "GameMeta"]


@runtime_checkable
class BotProtocol(Protocol):  # pragma: no cover
    """Structural typing interface for a bot.

    A minimal subset required by the *Game* engine. Any object that satisfies
    these attributes/methods can participate in the game, which makes the code
    test‑friendly and mypy‑friendly at the same time.
    """

    # Public attrs
    name: str
    balance: int
    current_bet: int
    is_active: bool

    # Complex attrs
    hand: "HandProtocol"  # quoted to avoid a hard dependency

    # Behaviour
    def decide(self) -> bool:  # noqa: D401 – already explicit in name
        """Return *True* if the bot wants another card, *False* otherwise."""


class HandProtocol(Protocol):  # pragma: no cover – same idea as *BotProtocol*
    def calculate_score(self, target: int) -> int:
        ...

    def add_card(self, card: object) -> None:
        ...

    @property
    def cards(self) -> List[object]:
        ...


# ---------------------------------------------------------------------------
# Utility helpers – hide the “ugly” underscore access if a public attribute is
# not provided by the concrete Bot implementation. This keeps the *Game* class
# clean and backward‑compatible with legacy bots that still expose their internals.
# ---------------------------------------------------------------------------


def _safe_get(bot: BotProtocol, public: str) -> object:  # noqa: ANN001 – generic
    """Return *bot.public* if present, otherwise fall back to *bot._public*."""

    if hasattr(bot, public):
        return getattr(bot, public)
    return getattr(bot, f"_{public}")


def _safe_set(bot: BotProtocol, public: str, value: object) -> None:  # noqa: ANN001
    """Set *bot.public* (or its hidden counterpart) to *value*."""

    if hasattr(bot, public):
        setattr(bot, public, value)
    else:
        setattr(bot, f"_{public}", value)


# ---------------------------------------------------------------------------
#  Game engine
# ---------------------------------------------------------------------------


class GameMeta(type):
    """Metaclass that injects *target_score* at class‑creation time."""

    def __new__(  # noqa: D401 – docstring kept from the original for clarity
        cls, name: str, bases: tuple[type, ...], attrs: dict[str, object]
    ) -> "Game":
        attrs.setdefault("target_score", 21)
        return super().__new__(cls, name, bases, attrs)  # type: ignore[misc]


class Game(metaclass=GameMeta):
    """Black‑jack‑like card game for several autonomous bots.

    The public *play()* method drives the whole life‑cycle. Detailed state is
    surfaced through a standard *logging.Logger* which can be redirected to a
    file via *output_file* or controlled globally by the application.
    """

    # ---------------------------------------------------------------------
    # Construction helpers
    # ---------------------------------------------------------------------

    def __init__(
        self,
        bots: List[BotProtocol],
        max_steps: int = 10,
        output_file: Optional[str] = None,
        target_score: Optional[int] = None,
    ) -> None:
        if max_steps <= 0:
            raise ValueError("max_steps must be a positive integer > 0")

        self._deck: Deck = Deck()
        self._bots: List[BotProtocol] = bots
        self._max_steps: int = max_steps
        self._current_step: int = 0

        # Score can be customised per‑instance but always falls back to the
        # default injected by *GameMeta*.
        self.target_score: int = target_score or type(self).target_score  # type: ignore[attr-defined]

        # -----------------------------------------------------------------
        # Logging configuration – per‑instance logger so different games can
        # be isolated if needed.
        # -----------------------------------------------------------------
        self._logger = logging.getLogger(f"{__name__}.{id(self):x}")
        self._logger.setLevel(logging.INFO)
        handler: logging.Handler
        if output_file:
            handler = logging.FileHandler(output_file, mode="w", encoding="utf‑8")
        else:
            handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(message)s"))
        self._logger.addHandler(handler)
        # Keep a reference so that we can close the file when the game ends.
        self._handler = handler

    # ---------------------------------------------------------------------
    # Logging helpers
    # ---------------------------------------------------------------------

    def _log(self, message: str) -> None:  # noqa: D401 – thin wrapper
        self._logger.info(message)

    # ---------------------------------------------------------------------
    # Public API
    # ---------------------------------------------------------------------

    def play(self) -> None:
        """Run the main game loop and block until the game ends."""
        try:
            for _ in self._rounds():
                pass  # *self._rounds()* already does the heavy lifting.
        finally:
            # Always flush/close the handler so that the log file (if any) is
            # written even in case of exceptions.
            self._handler.close()
            self._logger.removeHandler(self._handler)

    # ---------------------------------------------------------------------
    # Internal core – everything below here is considered an implementation
    # detail and may change without notice.
    # ---------------------------------------------------------------------

    def _rounds(self) -> Iterable[None]:
        """Generator encapsulating the game flow round by round."""

        self._show_initial_state()
        while self._current_step < self._max_steps:
            self._play_round()
            self._current_step += 1

            # ----- Termination checks -----
            active_bots = [b for b in self._bots if _safe_get(b, "is_active")]

            # A. Only one bot left alive
            if len(active_bots) == 1:
                winner = active_bots[0]
                self._conclude(winner, reason="last remaining bot")
                yield  # so callers can still iterate even if we finish early
                return

            # B. Someone hit the exact target
            perfect = next(
                (
                    b
                    for b in active_bots
                    if b.hand.calculate_score(self.target_score) == self.target_score
                ),
                None,
            )
            if perfect:
                self._conclude(perfect, reason=f"reached {self.target_score} points")
                yield
                return

            yield  # Round finished, but the game continues.

        # ----- Max rounds exhausted – use score heuristics to decide -----
        self._log("Max number of rounds reached – determining winner by score …")
        winner = self._determine_winner()
        self._conclude(winner)

    # ------------------------------------------------------------------
    # Round helpers
    # ------------------------------------------------------------------

    def _play_round(self) -> None:
        self._log(f"\n— Round {self._current_step + 1} —")
        for bot in self._bots:
            # Skip inactive players early
            if not _safe_get(bot, "is_active"):
                continue

            score = bot.hand.calculate_score(self.target_score)

            if score >= self.target_score:
                # Bust or exact target – the bot cannot act this round
                _safe_set(bot, "is_active", False)
                tag = "(bust)" if score > self.target_score else "(stay)"
                self._log(f"{bot.name} stays with score {score} {tag}")
                continue

            if bot.decide():
                card = self._deck._draw_card()  # noqa: SLF001 – minimal change
                if card is None:
                    self._log("Deck is empty!")
                    break  # Cannot draw further – end round early.
                bot.hand.add_card(card)
                self._log(f"{bot.name} draws {card}")
            else:
                self._log(f"{bot.name} stays with score {score}")

        self._show_state()

    # ------------------------------------------------------------------
    # State inspection helpers
    # ------------------------------------------------------------------

    def _show_initial_state(self) -> None:
        self._log("\n— Initial Game State —")
        for bot in self._bots:
            self._log(
                f"{bot.name}: Initial Balance = {bot.balance}, Initial Bet = {bot.current_bet}"
            )

    def _show_final_state(self, winner: Optional[BotProtocol]) -> None:
        self._log("\n— Final Game State —")
        for bot in self._bots:
            self._log(f"{bot.name}: Final Balance = {bot.balance}")
        if winner is not None:
            self._log(f"Winner: {winner.name} (Balance ⇒ {winner.balance})")

    def _show_state(self) -> None:
        state = "\nCurrent game state:"  # Single string for one log entry
        for bot in self._bots:
            hand_cards = ", ".join(map(str, bot.hand.cards))
            score = bot.hand.calculate_score(self.target_score)
            state += f"\n{bot.name} ({bot.__class__.__name__}) score: {score} | Hand: [{hand_cards}]"
        self._log(state)

    # ------------------------------------------------------------------
    # Winner logic
    # ------------------------------------------------------------------

    def _determine_winner(self) -> Optional[BotProtocol]:
        valid = [
            b
            for b in self._bots
            if b.hand.calculate_score(self.target_score) <= self.target_score
        ]
        if not valid:
            self._log("All bots bust. No winner.")
            return None
        perfect = next(
            (
                b
                for b in valid
                if b.hand.calculate_score(self.target_score) == self.target_score
            ),
            None,
        )
        if perfect:
            return perfect
        return max(valid, key=lambda b: b.hand.calculate_score(self.target_score))

    # ------------------------------------------------------------------
    # Pot handling
    # ------------------------------------------------------------------

    def _distribute_pot(self, winner: BotProtocol) -> int:
        total_bet = sum(b.current_bet for b in self._bots if b is not winner)
        _safe_set(winner, "balance", winner.balance + total_bet)
        for bot in self._bots:
            if bot is not winner:
                _safe_set(bot, "balance", bot.balance - bot.current_bet)
            _safe_set(bot, "current_bet", 0)
        return total_bet

    def _conclude(
        self, winner: Optional[BotProtocol], *, reason: str | None = None
    ) -> None:
        if winner is None:
            self._show_final_state(winner=None)
            self._log("Game ended with no winner.")
            return
        total_winnings = self._distribute_pot(winner)
        pretty_reason = f" – {reason}" if reason else ""
        self._log(f"Game over: {winner.name} wins{pretty_reason}!")
        self._show_final_state(winner)
