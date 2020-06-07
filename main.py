import pygame
import sys
import physics
from pygame.locals import *


def terminate():
    pygame.quit()
    sys.exit()


def main():
    pygame.init()

    screen = pygame.display.set_mode((400, 300))
    white = (255, 255, 255)

    coin1 = physics.Coin(10, 100, 170)
    coin1.velocity = physics.Vector(5, 0)
    coin2 = physics.Coin(15, 300, 150)
    friction_constant = 0.15

    elastic_constant = 10

    fps_clock = pygame.time.Clock()
    fps = 60

    move = False

    while True:
        screen.fill(white)
        coin1.draw(screen)
        coin2.draw(screen)
        pygame.display.update()

        if coin1.velocity.length < 0.01 and coin2.velocity.length < 0.01:
            if move:
                print("Stop\n")
                move = False
        elif not move:
            print("Start\n")
            move = True

        elastic1, elastic2 = physics.get_elastic(coin1, coin2, elastic_constant)
        coin1.apply_force(elastic1)
        coin2.apply_force(elastic2)

        coin1.apply_friction(friction_constant)
        coin2.apply_friction(friction_constant)

        coin1.update()
        coin2.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

        fps_clock.tick(fps)


if __name__ == "__main__":
    main()
