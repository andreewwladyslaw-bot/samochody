import curses
import random

from constants import (
    GAME_TITLE,
    MIN_TERMINAL_WIDTH,
    MIN_TERMINAL_HEIGHT,
    ROAD_WIDTH,
    ROAD_HEIGHT,
    LANE_COUNT,
    PLAYER_CAR,
    ENEMY_CARS,
    FRAME_DELAY_MS,
    ENEMY_SPAWN_FRAMES,
    MAX_ENEMIES,
    MIN_ENEMY_GAP,
    CRASH_SPRITE,
    CRASH_DELAY_MS,
    DISTANCE_PER_LEVEL,
    MAX_LEVEL,
    SPEED_STEP_MS,
    MIN_FRAME_DELAY_MS,
    SPEED_UP_MESSAGE_FRAMES,
    PLAYER_NAME,
    DECORATION_SPRITES,
    DECORATION_SPAWN_FRAMES,
    MAX_DECORATIONS,
    COUNTDOWN_DELAY_MS,
    START_DELAY_MS,
)

from storage import (
    load_highscores,
    save_highscore,
    get_best_score,
)


def is_exit_key(key):
    """Sprawdza, czy naciśnięto Q albo Esc."""
    return key in (
        ord("q"),
        ord("Q"),
        27,  # Esc
    )


def get_sprite_lines(sprite):
    """Zwraca sprite jako kolekcję wierszy."""
    if isinstance(sprite, str):
        return (sprite,)

    return sprite


def get_sprite_width(sprite):
    """Zwraca szerokość najszerszego wiersza sprite'a."""
    lines = get_sprite_lines(sprite)

    return max(len(line) for line in lines)


def get_sprite_height(sprite):
    """Zwraca wysokość sprite'a."""
    return len(get_sprite_lines(sprite))


def draw_sprite(
    screen,
    y,
    x,
    sprite,
    min_y=0,
    max_y=None,
):
    """Rysuje jedno- lub wielowierszowy sprite."""
    terminal_height, terminal_width = screen.getmaxyx()

    if max_y is None:
        max_y = terminal_height

    for row_offset, line in enumerate(
        get_sprite_lines(sprite)
    ):
        screen_y = y + row_offset

        # Wiersz poza wyznaczonym obszarem
        if not min_y <= screen_y < max_y:
            continue

        # Wiersz poza terminalem
        if not 0 <= screen_y < terminal_height:
            continue

        draw_x = x
        visible_line = line

        # Obcięcie części sprite'a wychodzącej z lewej strony
        if draw_x < 0:
            visible_line = visible_line[-draw_x:]
            draw_x = 0

        if draw_x >= terminal_width:
            continue

        available_width = terminal_width - draw_x - 1

        if available_width <= 0:
            continue

        try:
            screen.addnstr(
                screen_y,
                draw_x,
                visible_line,
                available_width,
            )
        except curses.error:
            # Ochrona przed błędem rysowania na krawędzi terminala
            pass

def show_countdown(screen):
    """Pokazuje odliczanie przed rozpoczęciem gry."""
    height, _ = screen.getmaxyx()
    center_y = height // 2

    for number in ("3", "2", "1"):
        screen.erase()

        add_centered(
            screen,
            center_y - 2,
            GAME_TITLE,
        )

        add_centered(
            screen,
            center_y,
            number,
        )

        screen.refresh()
        curses.napms(COUNTDOWN_DELAY_MS)

    screen.erase()

    add_centered(
        screen,
        center_y - 2,
        GAME_TITLE,
    )

    add_centered(
        screen,
        center_y,
        "START!",
    )

    screen.refresh()
    curses.napms(START_DELAY_MS)
def add_centered(screen, y, text):
    """Wyświetla tekst na środku wskazanego wiersza."""
    height, width = screen.getmaxyx()

    if not 0 <= y < height:
        return

    x = max(0, (width - len(text)) // 2)
    available_width = width - x - 1

    if available_width <= 0:
        return

    try:
        screen.addnstr(
            y,
            x,
            text,
            available_width,
        )
    except curses.error:
        pass


def draw_road(screen, start_y, start_x, line_offset):
    """Rysuje drogę oraz animowane linie między pasami."""
    lane_width = ROAD_WIDTH // LANE_COUNT

    for row in range(ROAD_HEIGHT):
        y = start_y + row

        # Granice drogi
        screen.addstr(y, start_x, "│")
        screen.addstr(y, start_x + ROAD_WIDTH, "│")

        # Linie oddzielające trzy pasy
        first_line_x = start_x + lane_width
        second_line_x = start_x + lane_width * 2

        # Animowana linia przerywana
        if (row + line_offset) % 2 == 0:
            screen.addstr(y, first_line_x, "┆")
            screen.addstr(y, second_line_x, "┆")


def get_lane_x(road_x, lane, sprite):
    """Oblicza pozycję X na środku wybranego pasa."""
    lane_width = ROAD_WIDTH // LANE_COUNT
    sprite_width = get_sprite_width(sprite)

    return (
        road_x
        + lane * lane_width
        + lane_width // 2
        - sprite_width // 2
    )


def get_player_y():
    """Zwraca górny wiersz samochodu gracza na drodze."""
    player_height = get_sprite_height(PLAYER_CAR)

    return ROAD_HEIGHT - player_height - 1


def draw_player(screen, road_y, road_x, player_lane):
    """Rysuje samochód gracza."""
    player_y = road_y + get_player_y()

    player_x = get_lane_x(
        road_x,
        player_lane,
        PLAYER_CAR,
    )

    draw_sprite(
        screen,
        player_y,
        player_x,
        PLAYER_CAR,
        min_y=road_y,
        max_y=road_y + ROAD_HEIGHT,
    )


def create_enemy():
    """Tworzy przeszkodę na losowym pasie."""
    return {
        "lane": random.randint(0, LANE_COUNT - 1),
        "y": 0,
        "sprite": random.choice(ENEMY_CARS),
        "passed_player": False,
    }


def can_spawn_enemy(enemies):
    """Sprawdza, czy jest miejsce na nową przeszkodę."""
    maximum_enemy_height = max(
        get_sprite_height(sprite)
        for sprite in ENEMY_CARS
    )

    required_position = (
        maximum_enemy_height
        + MIN_ENEMY_GAP
    )

    for enemy in enemies:
        if enemy["y"] < required_position:
            return False

    return True


def draw_enemies(screen, road_y, road_x, enemies):
    """Rysuje wszystkie samochody-przeszkody."""
    for enemy in enemies:
        enemy_x = get_lane_x(
            road_x,
            enemy["lane"],
            enemy["sprite"],
        )

        enemy_screen_y = road_y + enemy["y"]

        draw_sprite(
            screen,
            enemy_screen_y,
            enemy_x,
            enemy["sprite"],
            min_y=road_y,
            max_y=road_y + ROAD_HEIGHT,
        )


def create_decoration():
    """Tworzy dekorację po lewej lub prawej stronie drogi."""
    return {
        "side": random.choice(("left", "right")),
        "y": 0,
        "sprite": random.choice(DECORATION_SPRITES),
        "distance": random.randint(2, 5),
    }


def draw_decorations(
    screen,
    road_y,
    road_x,
    decorations,
):
    """Rysuje dekoracje przy drodze."""
    terminal_height, terminal_width = screen.getmaxyx()

    for decoration in decorations:
        decoration_y = road_y + decoration["y"]

        if decoration["side"] == "left":
            decoration_x = (
                road_x
                - decoration["distance"]
            )
        else:
            decoration_x = (
                road_x
                + ROAD_WIDTH
                + decoration["distance"]
            )

        if (
            0 <= decoration_y < terminal_height
            and 0 <= decoration_x < terminal_width
        ):
            try:
                screen.addstr(
                    decoration_y,
                    decoration_x,
                    decoration["sprite"],
                )
            except curses.error:
                pass


def check_collision(player_lane, enemies):
    """Sprawdza kolizję pojazdów na podstawie ich zakresów."""
    player_top = get_player_y()

    player_bottom = (
        player_top
        + get_sprite_height(PLAYER_CAR)
        - 1
    )

    for enemy in enemies:
        enemy_top = enemy["y"]

        enemy_bottom = (
            enemy_top
            + get_sprite_height(enemy["sprite"])
            - 1
        )

        same_lane = (
            enemy["lane"] == player_lane
        )

        vertical_overlap = (
            enemy_top <= player_bottom
            and enemy_bottom >= player_top
        )

        if same_lane and vertical_overlap:
            return True

    return False


def get_frame_delay(level):
    """Oblicza opóźnienie klatki dla danego poziomu."""
    delay = (
        FRAME_DELAY_MS
        - (level - 1) * SPEED_STEP_MS
    )

    return max(
        MIN_FRAME_DELAY_MS,
        delay,
    )


def show_crash(
    screen,
    road_y,
    road_x,
    player_lane,
    enemies,
    decorations,
    line_offset,
):
    """Pokazuje krótki efekt zderzenia."""
    screen.erase()

    draw_road(
        screen,
        road_y,
        road_x,
        line_offset,
    )

    draw_decorations(
        screen,
        road_y,
        road_x,
        decorations,
    )

    draw_enemies(
        screen,
        road_y,
        road_x,
        enemies,
    )

    crash_y = road_y + get_player_y()

    crash_x = get_lane_x(
        road_x,
        player_lane,
        CRASH_SPRITE,
    )

    draw_sprite(
        screen,
        crash_y,
        crash_x,
        CRASH_SPRITE,
        min_y=road_y,
        max_y=road_y + ROAD_HEIGHT,
    )

    screen.refresh()
    curses.napms(CRASH_DELAY_MS)


def show_game_over(
    screen,
    score,
    distance,
    best_score,
    highscores,
):
    """
    Pokazuje ekran końcowy.

    Zwraca:
    restart – gdy gracz naciśnie R,
    quit – gdy gracz naciśnie Q albo Esc.
    """
    screen.timeout(-1)
    screen.erase()

    height, width = screen.getmaxyx()

    start_y = max(
        1,
        height // 2 - 7,
    )

    add_centered(
        screen,
        start_y,
        "GAME OVER",
    )

    add_centered(
        screen,
        start_y + 2,
        f"SCORE: {score}",
    )

    add_centered(
        screen,
        start_y + 3,
        f"DISTANCE: {distance} m",
    )

    add_centered(
        screen,
        start_y + 4,
        f"BEST SCORE: {best_score}",
    )

    add_centered(
        screen,
        start_y + 6,
        "TOP 5",
    )

    # Wyświetlenie tabeli najlepszych wyników
    for index, result in enumerate(
        highscores,
        start=1,
    ):
        result_text = (
            f"{index}. {result['name']} - "
            f"{result['score']} pkt - "
            f"{result['distance']} m"
        )

        result_y = start_y + 6 + index

        add_centered(
            screen,
            result_y,
            result_text,
        )

    action_text = (
        "R - restart | Q lub Esc - wyjscie"
    )

    action_y = start_y + 13

    if action_y >= height:
        action_y = height - 1

    add_centered(
        screen,
        action_y,
        action_text,
    )

    screen.refresh()

    while True:
        key = screen.getch()

        if key in (
            ord("r"),
            ord("R"),
        ):
            return "restart"

        if is_exit_key(key):
            return "quit"

def wait_for_terminal_size(screen):
    """
    Czeka, aż terminal będzie wystarczająco duży.

    Zwraca:
    True  – terminal ma poprawny rozmiar,
    False – użytkownik nacisnął Q albo Esc.
    """
    screen.timeout(200)

    while True:
        height, width = screen.getmaxyx()

        terminal_is_large_enough = (
            width >= MIN_TERMINAL_WIDTH
            and height >= MIN_TERMINAL_HEIGHT
        )

        if terminal_is_large_enough:
            return True

        screen.erase()

        center_y = height // 2

        add_centered(
            screen,
            center_y - 1,
            "Terminal window is too small.",
        )

        add_centered(
            screen,
            center_y,
            "Please enlarge the window.",
        )

        add_centered(
            screen,
            center_y + 2,
            "Q or Esc - exit",
        )

        screen.refresh()

        key = screen.getch()

        if is_exit_key(key):
            return False

def show_game_screen(screen):
    """Uruchamia jedną rozgrywkę."""

    if not wait_for_terminal_size(screen):
        return "quit"

    height, width = screen.getmaxyx()

    player_lane = 1

    enemies = [create_enemy()]
    spawn_counter = 0

    decorations = []
    decoration_spawn_counter = 0

    line_offset = 0

    score = 0
    distance = 0

    level = 1
    current_delay = FRAME_DELAY_MS
    speed_up_frames = 0

# Początkowy pas gracza
    player_lane = 1

# Przeszkody
    enemies = [create_enemy()]
    spawn_counter = 0

# Dekoracje
    decorations = []
    decoration_spawn_counter = 0

# Animacja drogi
    line_offset = 0

# Wyniki
    score = 0
    distance = 0

# Poziom i szybkość
    level = 1
    current_delay = FRAME_DELAY_MS
    speed_up_frames = 0

# Wczytanie najlepszych wyników
    highscores = load_highscores()
    best_score = get_best_score(highscores)
# Odliczanie przed rozpoczęciem rozgrywki
    show_countdown(screen)
    screen.timeout(current_delay)

    while True:
        current_height, current_width = screen.getmaxyx()

        if (
                current_width < MIN_TERMINAL_WIDTH
                or current_height < MIN_TERMINAL_HEIGHT
        ):
            if not wait_for_terminal_size(screen):
                return "quit"

            height, width = screen.getmaxyx()

            # Przywrócenie szybkości gry po powiększeniu okna
            screen.timeout(current_delay)

        screen.erase()

        # Tytuł gry
        title_x = (
            width - len(GAME_TITLE)
        ) // 2

        screen.addstr(
            0,
            title_x,
            GAME_TITLE,
        )

        # Najlepszy wynik widoczny podczas gry
        displayed_best = max(
            best_score,
            score,
        )

        panel_text = (
            f"SCORE: {score}  "
            f"DIST: {distance} m  "
            f"LEVEL: {level}  "
            f"BEST: {displayed_best}"
        )

        screen.addnstr(
            1,
            2,
            panel_text,
            width - 4,
        )

        controls = (
            "A/D lub strzalki | "
            "Q/Esc - wyjscie"
        )

        add_centered(
            screen,
            2,
            controls,
        )

        if speed_up_frames > 0:
            add_centered(
                screen,
                3,
                "SPEED UP!",
            )

        road_y = 4

        road_x = (
            width - ROAD_WIDTH
        ) // 2

        # Rysowanie planszy
        draw_road(
            screen,
            road_y,
            road_x,
            line_offset,
        )

        draw_decorations(
            screen,
            road_y,
            road_x,
            decorations,
        )

        draw_enemies(
            screen,
            road_y,
            road_x,
            enemies,
        )

        draw_player(
            screen,
            road_y,
            road_x,
            player_lane,
        )

        screen.refresh()

        # Odczyt klawisza
        key = screen.getch()

        # Wyjście przez Q albo Esc
        if is_exit_key(key):
            return "quit"

        # Ruch w lewo
        if key in (
            curses.KEY_LEFT,
            ord("a"),
            ord("A"),
        ):
            player_lane = max(
                0,
                player_lane - 1,
            )

        # Ruch w prawo
        elif key in (
            curses.KEY_RIGHT,
            ord("d"),
            ord("D"),
        ):
            player_lane = min(
                LANE_COUNT - 1,
                player_lane + 1,
            )

        # Przesuwanie samochodów-przeszkód
        for enemy in enemies:
            enemy["y"] += 1

        # Punkty i dystans za jazdę
        distance += 1
        score += 1

        # Obliczenie aktualnego poziomu
        new_level = min(
            distance // DISTANCE_PER_LEVEL + 1,
            MAX_LEVEL,
        )

        # Zwiększenie szybkości
        if new_level > level:
            level = new_level

            current_delay = get_frame_delay(
                level
            )

            screen.timeout(current_delay)

            speed_up_frames = (
                SPEED_UP_MESSAGE_FRAMES
            )

        # Sprawdzenie kolizji
        if check_collision(
            player_lane,
            enemies,
        ):
            show_crash(
                screen,
                road_y,
                road_x,
                player_lane,
                enemies,
                decorations,
                line_offset,
            )

            # Zapisanie wyniku
            highscores = save_highscore(
                PLAYER_NAME,
                score,
                distance,
            )

            best_score = get_best_score(
                highscores
            )

            action = show_game_over(
                screen,
                score,
                distance,
                best_score,
                highscores,
            )

            return action

        # Dolna krawędź samochodu gracza
        player_bottom = (
            get_player_y()
            + get_sprite_height(PLAYER_CAR)
            - 1
        )

        # Bonus za ominięcie samochodu
        for enemy in enemies:
            if (
                enemy["y"] > player_bottom
                and not enemy["passed_player"]
            ):
                score += 20
                enemy["passed_player"] = True

        # Usuwanie przeszkód poza drogą
        enemies = [
            enemy
            for enemy in enemies
            if enemy["y"] < ROAD_HEIGHT
        ]

        # Liczenie klatek do nowej przeszkody
        spawn_counter += 1

        # Dodanie nowej przeszkody
        if (
            spawn_counter
            >= ENEMY_SPAWN_FRAMES
            and len(enemies) < MAX_ENEMIES
            and can_spawn_enemy(enemies)
        ):
            enemies.append(
                create_enemy()
            )

            spawn_counter = 0

        # Przesuwanie dekoracji
        for decoration in decorations:
            decoration["y"] += 1

        # Usuwanie dekoracji poza ekranem
        decorations = [
            decoration
            for decoration in decorations
            if decoration["y"] < ROAD_HEIGHT
        ]

        decoration_spawn_counter += 1

        # Tworzenie nowej dekoracji
        if (
            decoration_spawn_counter
            >= DECORATION_SPAWN_FRAMES
            and len(decorations)
            < MAX_DECORATIONS
        ):
            decorations.append(
                create_decoration()
            )

            decoration_spawn_counter = 0

        # Skracanie czasu komunikatu SPEED UP
        if speed_up_frames > 0:
            speed_up_frames -= 1

        # Animacja linii drogi
        line_offset = (
            line_offset + 1
        ) % 2


def main(screen):
    """Główna funkcja programu."""
    try:
        curses.curs_set(0)
    except curses.error:
        pass

    screen.keypad(True)

    while True:
        action = show_game_screen(screen)

        if action == "restart":
            continue

        if action == "quit":
            break


if __name__ == "__main__":
    curses.wrapper(main)