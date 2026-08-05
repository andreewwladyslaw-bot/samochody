import json
from pathlib import Path

from constants import MAX_HIGH_SCORES


# Folder, w którym znajduje się storage.py
PROJECT_DIR = Path(__file__).resolve().parent

# Ścieżka do folderu data i pliku JSON
DATA_DIR = PROJECT_DIR / "data"
HIGHSCORES_FILE = DATA_DIR / "highscores.json"


def load_highscores():
    """Wczytuje najlepsze wyniki z pliku JSON."""
    try:
        # Plik jeszcze nie istnieje
        if not HIGHSCORES_FILE.exists():
            return []

        file_content = HIGHSCORES_FILE.read_text(
            encoding="utf-8",
        )

        # Plik jest pusty
        if not file_content.strip():
            return []

        data = json.loads(file_content)

        # JSON powinien zawierać listę
        if not isinstance(data, list):
            return []

        valid_results = []

        for result in data:
            if not isinstance(result, dict):
                continue

            name = result.get("name")
            score = result.get("score")
            distance = result.get("distance")

            if (
                isinstance(name, str)
                and isinstance(score, int)
                and isinstance(distance, int)
                and score >= 0
                and distance >= 0
            ):
                valid_results.append(
                    {
                        "name": name,
                        "score": score,
                        "distance": distance,
                    }
                )

        valid_results.sort(
            key=lambda result: (
                result["score"],
                result["distance"],
            ),
            reverse=True,
        )

        return valid_results[:MAX_HIGH_SCORES]

    except (
        OSError,
        json.JSONDecodeError,
        UnicodeDecodeError,
    ):
        # Uszkodzony lub niemożliwy do odczytania plik
        return []


def save_highscore(player_name, score, distance):
    """Dodaje wynik, sortuje tabelę i zapisuje pięć najlepszych."""
    highscores = load_highscores()

    new_result = {
        "name": player_name,
        "score": score,
        "distance": distance,
    }

    highscores.append(new_result)

    highscores.sort(
        key=lambda result: (
            result["score"],
            result["distance"],
        ),
        reverse=True,
    )

    highscores = highscores[:MAX_HIGH_SCORES]

    try:
        # Utworzenie folderu data, jeśli go nie ma
        DATA_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        HIGHSCORES_FILE.write_text(
            json.dumps(
                highscores,
                ensure_ascii=False,
                indent=4,
            ),
            encoding="utf-8",
        )

    except OSError:
        # Błąd zapisu nie powinien wyłączyć całej gry
        pass

    return highscores


def get_best_score(highscores):
    """Zwraca najlepszy wynik albo zero."""
    if not highscores:
        return 0

    return highscores[0]["score"]