"""Core gameplay logic and state handling."""

from dataclasses import dataclass, field
import sys

import pygame

import button
from constants import MAX_HINTS
from direction import compress_get_bearing, get_direction
from distance import haversine
from game_ui import draw_game_ui, draw_win_popup
from resources import (
    CLOCK,
    COUNTRY_BY_LOWER,
    COUNTRY_NAMES_LOWER,
    SCREEN,
    get_font,
    random_country,
)


@dataclass
class GameState:
    """Mutable game state used by the play loop and UI."""
    input_text: str = ""
    guess_history: list[tuple[str, int, str]] = field(default_factory=list)
    hint_text: str = ""
    message: str = "Guess country"
    current_bearing: float | None = None
    display_angle: float = 0.0
    count: int = 0
    hint_count: int = 0
    game_won: bool = False
    target_country: dict | None = None


def _reset_state(state: GameState):
    """Initialize a fresh game state and choose a new target country."""
    state.input_text = ""
    state.guess_history.clear()
    state.hint_text = ""
    state.message = "Guess country"
    state.current_bearing = None
    state.display_angle = 0.0
    state.count = 0
    state.hint_count = 0
    state.game_won = False
    state.target_country = random_country()
    print(f"Answer: {state.target_country['country']}")


def _get_suggestions(prefix: str):
    """Return country name suggestions for the current input prefix."""
    lowered = prefix.lower()
    return [name for name, lower_name in COUNTRY_NAMES_LOWER if lower_name.startswith(lowered)]


def _handle_guess(state: GameState):
    """Validate and score the current guess, updating history and hints."""
    state.count += 1
    guess = COUNTRY_BY_LOWER.get(state.input_text.lower())
    if guess is None:
        state.message = "Country not found"
        return

    if guess["country"].lower() == state.target_country["country"].lower():
        state.message = f"Correct! {state.target_country['country']}"
        state.game_won = True
        return

    lat1, lon1 = guess["lat"], guess["lon"]
    lat2, lon2 = state.target_country["lat"], state.target_country["lon"]

    distance = round(haversine(lat1, lon1, lat2, lon2))
    bearing = compress_get_bearing(lat1, lon1, lat2, lon2)
    direction = get_direction(bearing)

    state.guess_history.append((guess["country"], distance, direction))
    state.current_bearing = bearing


def _handle_hint(state: GameState):
    """Advance the hint counter and set the current hint text."""
    if state.hint_count < MAX_HINTS:
        if state.hint_count == 0:
            state.hint_text = f"{state.target_country['hemisphere']} Hemisphere"
        elif state.hint_count == 1:
            state.hint_text = f"Continent : {state.target_country['continent']}"
        elif state.hint_count == 2:
            state.hint_text = f"Starts with : {state.target_country['country'][0]}"
        state.hint_count += 1
    else:
        state.hint_text = "No more hints"


def play():
    """Run the main game loop until the player exits to the menu."""
    state = GameState()
    _reset_state(state)

    hint_button = button.Button(
        image=None,
        pos=(120, 650),
        text_input="HINT",
        font=get_font(35),
        base_color=(255, 255, 255),
        hovering_color=(255, 80, 80),
    )
    back_button = button.Button(
        image=None,
        pos=(1200, 40),
        text_input="BACK",
        font=get_font(35),
        base_color=(255, 255, 255),
        hovering_color=(255, 0, 0),
    )
    win_again_button = button.Button(
        image=None,
        pos=(560, 420),
        text_input="Play Again",
        font=get_font(32),
        base_color=(255, 255, 255),
        hovering_color=(255, 80, 80),
    )
    win_exit_button = button.Button(
        image=None,
        pos=(720, 420),
        text_input="Exit",
        font=get_font(32),
        base_color=(255, 255, 255),
        hovering_color=(255, 0, 0),
    )

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if state.game_won:
                # Lock input to win popup actions.
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if win_again_button.checkForInput(mouse_pos):
                        _reset_state(state)
                    elif win_exit_button.checkForInput(mouse_pos):
                        return
                continue

            if event.type == pygame.KEYDOWN:
                # Text input for the guess box.
                if event.key == pygame.K_RETURN:
                    _handle_guess(state)
                    state.input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    state.input_text = state.input_text[:-1]
                else:
                    state.input_text += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                # UI button clicks.
                if hint_button.checkForInput(mouse_pos):
                    _handle_hint(state)
                if back_button.checkForInput(mouse_pos):
                    return

        # Autocomplete suggestions based on current input.
        suggestions = _get_suggestions(state.input_text)

        # Render the full game UI and update compass animation state.
        state.display_angle = draw_game_ui(
            state,
            suggestions,
            hint_button,
            back_button,
            mouse_pos,
        )

        if state.game_won:
            # Overlay the win popup on top of the game UI.
            draw_win_popup(mouse_pos, win_again_button, win_exit_button)

        pygame.display.flip()
        CLOCK.tick(60)
