import pygame
import sys
import physics
import math
from pygame.locals import *


def terminate():
    pygame.quit()
    sys.exit()


def main():
    pygame.init()

    screen = pygame.display.set_mode((400, 300))
    white = (255, 255, 255)
    light_blue = (32, 171, 255)
    pink = (255, 90, 195)

    coin1 = physics.Coin(10, 100, 170, light_blue)
    coin1.velocity = physics.Vector(6, 0)
    coin2 = physics.Coin(15, 300, 150, pink)
    friction_constant = 0.15

    elastic_constant = 10

    fps_clock = pygame.time.Clock()
    fps = 60
    time_constant = 60

    move = False

    direction = 0
    direction_original_surf = pygame.transform.scale(pygame.image.load("images/direction.png"), (100, 100))
    rotation_speed = 5
    direction_x = 60
    direction_y = 220
    left_key_down = False
    right_key_down = False
    direction_original_vector = physics.Vector(0, 1)

    while True:
        screen.fill(white)
        direction_surf = pygame.transform.rotate(direction_original_surf, direction)
        direction_rect = direction_surf.get_rect()
        direction_rect.center = (direction_x, direction_y)
        screen.blit(direction_surf, direction_rect)
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

        if left_key_down:
            direction += rotation_speed * time_constant / fps
        elif right_key_down:
            direction -= rotation_speed * time_constant / fps
        direction_radian = direction / 180 * math.pi
        direction_vector = direction_original_vector.rotate(direction_radian)

        elastic1, elastic2 = physics.get_elastic(coin1, coin2, elastic_constant)
        coin1.apply_force(elastic1)
        coin2.apply_force(elastic2)

        coin1.apply_friction(friction_constant)
        coin2.apply_friction(friction_constant)

        coin1.update(time_constant / fps)
        coin2.update(time_constant / fps)

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key in (K_LEFT, K_a):
                    left_key_down = True
                elif event.key in (K_RIGHT, K_d):
                    right_key_down = True
            elif event.type == KEYUP:
                if event.key in (K_LEFT, K_a):
                    left_key_down = False
                elif event.key in (K_RIGHT, K_d):
                    right_key_down = False
                elif event.key == K_SPACE:
                    pass

        fps_clock.tick(fps)


if __name__ == "__main__":
    main()
