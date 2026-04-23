import pygame
import time
import random

pygame.font.init()

WIDTH, HEIGHT = 1200, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Collision Game")

PLAYER_WIDTH = 80
PLAYER_HEIGHT = 80
PLAYER_VEL = 6

STAR_WIDTH = 50
STAR_HEIGHT = 50
STAR_VEL = 3


BG = pygame.transform.scale(pygame.image.load("game_bg.png"), (WIDTH, HEIGHT))
# remove background from player image
PLAYER_IMG = pygame.transform.scale(
    pygame.image.load("spaceship.png"), (PLAYER_WIDTH, PLAYER_HEIGHT)
)
STAR_IMG = pygame.transform.scale(
    pygame.image.load("star.png"), (STAR_WIDTH, STAR_HEIGHT)
)


FONT = pygame.font.SysFont("comicsans", 30)


class Player:
    def __init__(self):
        self.image_rect = pygame.Rect(
            WIDTH / 2 - PLAYER_WIDTH / 2,
            HEIGHT - PLAYER_HEIGHT,
            PLAYER_WIDTH,
            PLAYER_HEIGHT,
        )
        self.vel = PLAYER_VEL

        self.rect = pygame.Rect(0, 0, int(PLAYER_WIDTH * 0.5), int(PLAYER_HEIGHT * 0.5))
        self.update_hitbox()

    def update_hitbox(self):
        self.rect.centerx = self.image_rect.centerx
        self.rect.centery = self.image_rect.centery + 8

    def move(self, keys):
        if (
            keys[pygame.K_LEFT] or keys[pygame.K_a]
        ) and self.image_rect.x - self.vel >= 0:
            self.image_rect.x -= self.vel
        if (
            keys[pygame.K_RIGHT] or keys[pygame.K_d]
        ) and self.image_rect.x + self.vel + PLAYER_WIDTH <= WIDTH:
            self.image_rect.x += self.vel

        self.update_hitbox()

    def draw(self):
        WIN.blit(PLAYER_IMG, self.image_rect)


class Star:
    def __init__(self):
        star_x = random.randint(0, WIDTH - STAR_WIDTH)
        self.rect = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)

    def update(self):
        self.rect.y += STAR_VEL

    def draw(self):
        WIN.blit(STAR_IMG, (self.rect.x, self.rect.y))


def draw(player, elapsed_time, stars):
    WIN.blit(BG, (0, 0))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

    player.draw()
    # pygame.draw.rect(WIN, (255, 0, 0), player.rect, 2)

    for star in stars:
        star.draw()

    pygame.display.update()


# loop to keep game running
def main():
    run = True

    player = Player()
    clock = pygame.time.Clock()

    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 2000
    star_count = 0

    stars = []
    hit = False

    while run:
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        if star_count > star_add_increment:
            for _ in range(3):
                stars.append(Star())

            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        player.move(keys)

        for star in stars[:]:
            star.update()
            if star.rect.y > HEIGHT:
                stars.remove(star)
            elif (
                star.rect.y + star.rect.height >= player.rect.y
                and star.rect.colliderect(player.rect)
            ):
                stars.remove(star)
                hit = True
                break

        if hit:
            lost_text = FONT.render("You Lost!", 1, "white")
            WIN.blit(
                lost_text,
                (
                    WIDTH / 2 - lost_text.get_width() / 2,
                    HEIGHT / 2 - lost_text.get_height() / 2,
                ),
            )
            pygame.display.update()
            pygame.time.delay(4000)
            break

        draw(player, elapsed_time, stars)

    pygame.quit()


if __name__ == "__main__":
    main()
