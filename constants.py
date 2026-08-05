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

FRAME_DELAY_MS = 120

ENEMY_SPAWN_FRAMES = 8
MAX_ENEMIES = 3
MIN_ENEMY_GAP = 5

CRASH_SPRITE = (
    "\\|/",
    "-X-",
    "/|\\",
)
CRASH_DELAY_MS = 600

# Zwiększanie trudności
DISTANCE_PER_LEVEL = 100
MAX_LEVEL = 6
SPEED_STEP_MS = 15
MIN_FRAME_DELAY_MS = 50
SPEED_UP_MESSAGE_FRAMES = 8

# Najlepsze wyniki
PLAYER_NAME = "Vladislav"
MAX_HIGH_SCORES = 5

DECORATION_SPRITES = (
    "Y",   # drzewo
    "*",   # krzak
    "o",   # kamień
    "!",   # znak
)

DECORATION_SPAWN_FRAMES = 4
MAX_DECORATIONS = 8
COUNTDOWN_DELAY_MS = 700
START_DELAY_MS = 500