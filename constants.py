GAME_TITLE = "AUTOGONKI"

MIN_TERMINAL_WIDTH = 50
MIN_TERMINAL_HEIGHT = 20

ROAD_WIDTH = 25
ROAD_HEIGHT = 15
LANE_COUNT = 3


PLAYER_CAR = (
    "╭─╮",
    "│█│",
    "╰─╯",
)


ENEMY_CARS = (
    (
        "╭#╮",
        "│#│",
        "╰#╯",
    ),
    (
        "╭X╮",
        "│X│",
        "╰X╯",
    ),
    (
        "╭O╮",
        "│O│",
        "╰O╯",
    ),
)


CRASH_SPRITE = (
    "\\|/",
    "-X-",
    "/|\\",
)


# Początkowe opóźnienie klatki
FRAME_DELAY_MS = 120

# Przeszkody
ENEMY_SPAWN_FRAMES = 8
MAX_ENEMIES = 3
MIN_ENEMY_GAP = 5

# Efekt zderzenia
CRASH_DELAY_MS = 600

# Poziomy i szybkość
DISTANCE_PER_LEVEL = 100
MAX_LEVEL = 6
SPEED_STEP_MS = 15
MIN_FRAME_DELAY_MS = 50
SPEED_UP_MESSAGE_FRAMES = 8

# Gracz i wyniki
PLAYER_NAME = "Vladislav"
MAX_HIGH_SCORES = 5

# Dekoracje pobocza
DECORATION_SPRITES = (
    "Y",  # drzewo
    "*",  # krzak
    "o",  # kamień
    "!",  # znak drogowy
)

DECORATION_SPAWN_FRAMES = 4
MAX_DECORATIONS = 8

# Odliczanie
COUNTDOWN_DELAY_MS = 700
START_DELAY_MS = 500