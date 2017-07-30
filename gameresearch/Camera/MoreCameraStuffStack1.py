import sys
import pygame as pg
from pygame.math import Vector2


class Player(pg.sprite.Sprite):

    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.image = pg.Surface((30, 50))
        self.image.fill(pg.Color('dodgerblue'))
        self.rect = self.image.get_rect(center=pos)
        self.vel = Vector2(0, 0)
        self.pos = Vector2(pos)

    def update(self):
        self.pos += self.vel
        self.rect.center = self.pos


class Wall(pg.sprite.Sprite):

    def __init__(self, x, y, w, h, *groups):
        super().__init__(*groups)
        self.image = pg.Surface((w, h))
        self.image.fill(pg.Color('sienna2'))
        self.rect = self.image.get_rect(topleft=(x, y))


def main():
    screen = pg.display.set_mode((640, 480))
    clock = pg.time.Clock()
    all_sprites = pg.sprite.Group()
    player = Player((320, 240), all_sprites)
    walls = pg.sprite.Group()
    Wall(100, 170, 90, 20, all_sprites, walls)
    Wall(200, 100, 20, 140, all_sprites, walls)
    Wall(400, 60, 150, 100, all_sprites, walls)
    Wall(300, 470, 150, 100, all_sprites, walls)

    camera = Vector2(0, 0)

    done = False

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_d:
                    player.vel.x = 5
                elif event.key == pg.K_a:
                    player.vel.x = -5
                elif event.key == pg.K_w:
                    player.vel.y = -5
                elif event.key == pg.K_s:
                    player.vel.y = 5
            elif event.type == pg.KEYUP:
                if event.key == pg.K_d and player.vel.x > 0:
                    player.vel.x = 0
                elif event.key == pg.K_a and player.vel.x < 0:
                    player.vel.x = 0
                elif event.key == pg.K_w:
                    player.vel.y = 0
                elif event.key == pg.K_s:
                    player.vel.y = 0

        camera -= player.vel
        all_sprites.update()

        screen.fill((30, 30, 30))
        for sprite in all_sprites:
            screen.blit(sprite.image, sprite.rect.topleft+camera)

        pg.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()
    sys.exit()
