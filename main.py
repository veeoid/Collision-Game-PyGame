import pygame
import time
import random

WIDTH, HEIGHT = 1200, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Collision Game")

BG = pygame.transform.scale(
    pygame.image.load("CollisionGame/game_bg.png"), (WIDTH, HEIGHT)
)

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60


def draw(player):
    WIN.blit(BG, (0, 0))

    pygame.draw.rect(WIN, "blue", player)

    pygame.display.update()


# loop to keep game running
def main():
    run = True

    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        draw(player)

    pygame.quit()


if __name__ == "__main__":
    main()
