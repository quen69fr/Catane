from outils import *


def affiche_route(x1, y1, x2, y2, couleur):
    pygame.draw.line(SCREEN, NOIR, (x1, y1), (x2, y2))
    c = 0.1
    dx = x2 - x1
    dy = y2 - y1
    cx = int(c * dx)
    cy = int(c * dy)
    x3 = x1 + cx
    y3 = y1 + cy
    x4 = x2 - cx
    y4 = y2 - cy
    pygame.draw.line(SCREEN, NOIR, (x3, y3), (x4, y4), l + 2)
    pygame.gfxdraw.filled_circle(SCREEN, x3, y3, int(LARGEUR_ROUTE / 2), NOIR)
    pygame.gfxdraw.filled_circle(SCREEN, x4, y4, int(LARGEUR_ROUTE / 2), NOIR)
    pygame.draw.line(SCREEN, couleur, (x3, y3), (x4, y4), LARGEUR_ROUTE - 2)
    pygame.gfxdraw.filled_circle(SCREEN, x3, y3, int(LARGEUR_ROUTE / 2) - 2, couleur)
    pygame.gfxdraw.filled_circle(SCREEN, x4, y4, int(LARGEUR_ROUTE / 2) - 2, couleur)


while True:
    souris = pygame.mouse.get_pos()
    x_souris = souris[0]
    y_souris = souris[1]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

    SCREEN.fill(-1)
    affiche_route(20 + 200, 20 + 200, 80 + 200, 65 + 200, ROUGE)

    pygame.display.update()
    pygame.time.Clock().tick(FPS)