import pygame
import sys
import physics
import math
from pygame.locals import *


class Turn(object):
    def __init__(self):
        self.turn = 1
        self._map = {1: 2, 2: 1}

    def next(self):
        self.turn = self._map[self.turn]


def terminate():
    pygame.quit()
    sys.exit()


def main():
    pygame.init()

    window_width = 400
    window_height = 300
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Gobcoin-Coincidence - By Zyzzyva038")
    white = (255, 255, 255)
    light_blue = (32, 171, 255)
    pink = (255, 90, 195)

    coin1 = physics.Coin(10, 100, 170, light_blue)
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

    space_down = False
    finger = 0
    finger_speed = 24
    finger_surfs = tuple((pygame.image.load("images/fingers/%d.png" % x) for x in range(0, 8)))
    finger_rect = finger_surfs[0].get_rect()
    finger_rect.topleft = (0, 0)
    initial_speed_constant = 10
    fire = False

    turn = Turn()

    while True:
        # draw screen
        screen.fill(white)
        direction_surf = pygame.transform.rotate(direction_original_surf, direction)
        direction_rect = direction_surf.get_rect()
        direction_rect.center = (direction_x, direction_y)
        screen.blit(direction_surf, direction_rect)
        screen.blit(finger_surfs[int(finger)], finger_rect)
        coin1.draw(screen)
        coin2.draw(screen)
        pygame.display.update()

        # get events
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key in (K_LEFT, K_a):
                    left_key_down = True
                elif event.key in (K_RIGHT, K_d):
                    right_key_down = True
                elif event.key == K_SPACE:
                    space_down = True

            elif event.type == KEYUP:
                if event.key in (K_LEFT, K_a):
                    left_key_down = False
                elif event.key in (K_RIGHT, K_d):
                    right_key_down = False
                elif event.key == K_SPACE:
                    space_down = False
                    fire = True

        # update game state
        if coin1.velocity.length < 0.01 and coin2.velocity.length < 0.01:
            if move:
                print("Stop\n")
                turn.next()
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
        screen_direction_vector = physics.Vector(direction_vector.x, -direction_vector.y)

        elastic1, elastic2 = physics.get_elastic(coin1, coin2, elastic_constant)
        coin1.apply_force(elastic1)
        coin2.apply_force(elastic2)

        coin1.apply_friction(friction_constant)
        coin2.apply_friction(friction_constant)

        coin1.update(time_constant / fps)
        coin2.update(time_constant / fps)

        if space_down:
            finger += finger_speed / fps
            if finger >= 7:
                finger = 0
        else:
            finger = 0

        if fire and not move:
            if turn.turn == 1:
                coin1.velocity = screen_direction_vector * finger * initial_speed_constant
            elif turn.turn == 2:
                coin2.velocity = screen_direction_vector * finger * initial_speed_constant

        if (coin1.position.x <= - coin1.mass or coin1.position.x >= window_width + coin1.mass or
                coin1.position.y <= - coin1.mass or coin1.position.y >= window_height + coin1.mass):
            win_state = 2
            return win_state
        elif (coin2.position.x <= - coin2.mass or coin2.position.x >= window_width + coin1.mass or
                coin2.position.y <= - coin2.mass or coin2.position.y >= window_height + coin1.mass):
            win_state = 1
            return win_state

        # tick FPS
        fps_clock.tick(fps)


if __name__ == "__main__":
    print(main())
