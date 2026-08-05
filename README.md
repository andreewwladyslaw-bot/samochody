# Autogonki

Terminalowa gra samochodowa napisana w języku Python.

Gracz steruje samochodem znajdującym się na jednej z trzech
drogowych alei. Z góry ekranu nadjeżdżają inne pojazdy.
Zadaniem gracza jest unikanie kolizji i zdobycie jak największej
liczby punktów.

## Funkcje gry

- terminalowa animacja;
- trzy pasy ruchu;
- sterowanie samochodem w lewo i w prawo;
- losowe samochody-przeszkody;
- losowe pasy i sprite'y przeszkód;
- wykrywanie kolizji;
- animowana drogowa linia rozdzielająca;
- drzewa, krzaki, kamienie i znaki przy drodze;
- punkty i przebyty dystans;
- bonus za bezpieczne ominięcie samochodu;
- poziomy trudności;
- stopniowe zwiększanie szybkości;
- odliczanie 3, 2, 1, START!;
- zapis pięciu najlepszych wyników do pliku JSON;
- możliwość rozpoczęcia nowej gry.

## Wymagania

- Windows 11;
- Python 3.14 lub nowszy;
- biblioteka `windows-curses`;
- terminal obsługujący znaki Unicode.

## Instalacja

Otwórz terminal w folderze projektu.

Zainstaluj wymagane biblioteki:

```cmd
python -m pip install -r requirements.txt
```

Możesz również zainstalować bibliotekę bezpośrednio:

```cmd
python -m pip install windows-curses
```

## Uruchomienie

W terminalu przejdź do folderu projektu:

```cmd
cd C:\sciezka\do\projektu
```

Uruchom grę:

```cmd
python main.py
```

Gry nie należy uruchamiać w zwykłym oknie `Run` programu PyCharm.
Należy użyć CMD albo terminala wbudowanego w PyCharm.

## Sterowanie

| Klawisz | Działanie |
|---|---|
| A | ruch w lewo |
| D | ruch w prawo |
| strzałka w lewo | ruch w lewo |
| strzałka w prawo | ruch w prawo |
| R | rozpoczęcie nowej gry po kolizji |
| Q | wyjście |
| Esc | wyjście |

## Zasady gry

Samochód gracza rozpoczyna grę na środkowym pasie.

Przeszkody pojawiają się u góry drogi i poruszają się w dół.
Gracz powinien zmieniać pasy, aby ich unikać.

Kolizja następuje wtedy, gdy samochód gracza i przeszkoda:

1. znajdują się na tym samym pasie;
2. mają przecinające się zakresy pionowe.

Po kolizji gra zapisuje wynik i wyświetla ekran `GAME OVER`.

## Punkty

Wynik jest obliczany według prostych zasad:

- każda klatka gry: 1 punkt;
- każda klatka gry: 1 metr dystansu;
- bezpieczne ominięcie samochodu: 20 dodatkowych punktów.

Przykład:

```text
100 klatek jazdy = 100 punktów
2 ominięte samochody = 40 punktów

SCORE: 140
DISTANCE: 100 m
```

## Poziomy trudności

Poziom zwiększa się po przejechaniu określonego dystansu.

Przykład:

```text
0–99 m       LEVEL 1
100–199 m    LEVEL 2
200–299 m    LEVEL 3
```

Po wejściu na nowy poziom:

- zmniejsza się opóźnienie między klatkami;
- przeszkody poruszają się szybciej;
- pojawia się komunikat `SPEED UP!`.

Gra ma ustawiony maksymalny poziom oraz minimalne opóźnienie,
dlatego szybkość nie zwiększa się bez końca.

## Struktura projektu

```text
car_racing/
│
├── main.py
├── constants.py
├── storage.py
├── requirements.txt
├── README.md
│
└── data/
    └── highscores.json
```

### main.py

Zawiera:

- główną pętlę gry;
- obsługę klawiatury;
- rysowanie drogi i pojazdów;
- ruch przeszkód;
- dekoracje;
- sprawdzanie kolizji;
- poziomy trudności;
- ekran `GAME OVER`;
- restart gry.

### constants.py

Zawiera stałe, między innymi:

- rozmiary drogi;
- liczbę pasów;
- sprite'y;
- szybkość gry;
- odstępy między przeszkodami;
- maksymalny poziom;
- liczbę najlepszych wyników.

### storage.py

Odpowiada za:

- wczytywanie wyników;
- sprawdzanie danych;
- sortowanie wyników;
- zapis do JSON;
- tworzenie folderu `data`;
- obsługę braku lub uszkodzenia pliku.

### data/highscores.json

Zawiera pięć najlepszych wyników zapisanych między
uruchomieniami programu.

## Przykład pliku JSON

```json
[
    {
        "name": "Vladislav",
        "score": 450,
        "distance": 350
    },
    {
        "name": "Vladislav",
        "score": 320,
        "distance": 260
    }
]
```

Wyniki są sortowane malejąco według liczby punktów.
Przy takiej samej liczbie punktów porównywany jest dystans.

## Użyte struktury danych

### Lista

Listy przechowują:

- przeszkody;
- dekoracje;
- najlepsze wyniki;
- dostępne sprite'y.

Przykład:

```python
enemies = []
decorations = []
```

### Słownik

Każda przeszkoda jest zapisana jako słownik:

```python
enemy = {
    "lane": 1,
    "y": 0,
    "sprite": (
        "╭#╮",
        "│#│",
        "╰#╯",
    ),
    "passed_player": False,
}
```

### Krotka

Krotki przechowują wiersze sprite'ów:

```python
PLAYER_CAR = (
    "╭─╮",
    "│█│",
    "╰─╯",
)
```

## Użyte algorytmy

### Losowanie przeszkód

Moduł `random` wybiera:

- pas ruchu;
- wygląd samochodu;
- stronę dekoracji;
- typ dekoracji.

### Usuwanie obiektów

Po opuszczeniu drogi przeszkody są usuwane z listy:

```python
enemies = [
    enemy
    for enemy in enemies
    if enemy["y"] < ROAD_HEIGHT
]
```

### Sprawdzanie kolizji

Program porównuje pasy oraz pionowe zakresy samochodów:

```python
vertical_overlap = (
    enemy_top <= player_bottom
    and enemy_bottom >= player_top
)
```

Kolizja występuje, gdy pojazdy znajdują się na tym samym pasie
i ich zakresy pionowe się przecinają.

### Sortowanie wyników

Wyniki są sortowane według punktów i dystansu:

```python
highscores.sort(
    key=lambda result: (
        result["score"],
        result["distance"],
    ),
    reverse=True,
)
```

Po sortowaniu program zachowuje tylko pięć najlepszych wyników.

## Obsługa błędów

Program obsługuje sytuacje, gdy:

- plik wyników jeszcze nie istnieje;
- folder `data` nie istnieje;
- plik JSON jest pusty;
- plik JSON jest uszkodzony;
- terminal jest zbyt mały;
- nie można ustawić widoczności kursora.

Jeżeli terminal jest zbyt mały, program pokazuje:

```text
Terminal window is too small.
Please enlarge the window.
```

## Autor

Vladislav
