import pygame

pygame.init()

SZEROKOSC = 800
WYSOKOSC = 500

okno = pygame.display.set_mode((SZEROKOSC, WYSOKOSC))
pygame.display.set_caption("gra ze samochodem")

zegar = pygame.time.Clock()


def rysuj_samochod(x, y):
    
    pygame.draw.rect(okno, "red", (x, y + 30, 140, 50))

    
    pygame.draw.polygon(
        okno,
        "red",
        [
            (x + 30, y + 30),
            (x + 50, y),
            (x + 105, y),
            (x + 125, y + 30)
        ]
    )

    pygame.draw.polygon(
        okno,
        "lightblue",
        [
            (x + 48, y + 27),
            (x + 60, y + 5),
            (x + 82, y + 5),
            (x + 82, y + 27)
        ]
    )

    pygame.draw.polygon(
        okno,
        "lightblue",
        [
            (x + 87, y + 5),
            (x + 102, y + 5),
            (x + 117, y + 27),
            (x + 87, y + 27)
        ]
    )

    pygame.draw.circle(okno, "black", (x + 30, y + 80), 18)
    pygame.draw.circle(okno, "black", (x + 110, y + 80), 18)

    pygame.draw.circle(okno, "gray", (x + 30, y + 80), 8)
    pygame.draw.circle(okno, "gray", (x + 110, y + 80), 8)


x = 300
y = 300

gra_dziala = True

while gra_dziala:
    for wydarzenie in pygame.event.get():
        if wydarzenie.type == pygame.QUIT:
            gra_dziala = False



    okno.fill("skyblue")

    pygame.draw.rect(okno, "gray", (0, 380, 800, 120))

    pygame.draw.rect(okno, "white", (0, 435, 800, 8))

    rysuj_samochod(x, y)

    pygame.display.update()
    zegar.tick(60)

pygame.quit()