import pygame
import math

__author__ = "Zyzzyva038"


collide = False


class Vector(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vector(self.x * other, self.y * other)

    def __truediv__(self, other):
        return Vector(self.x / other, self.y / other)

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __repr__(self):
        return "(x: %.3f, y: %.3f, length: %.3f)" % (self.x, self.y, self.length)

    __str__ = __repr__

    @property
    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def normalize(self):
        if self.x == 0 and self.y == 0:
            return Vector(1, 0)
        return Vector(self.x / self.length, self.y / self.length)


class Coin(object):
    def __init__(self, mass, pos_x, pos_y):
        self.mass = mass
        self.velocity = Vector(0, 0)
        self.acceleration = Vector(0, 0)
        self.resultant = Vector(0, 0)
        self.position = Vector(pos_x, pos_y)

    def apply_force(self, force):
        self.resultant += force

    def apply_friction(self, constant):
        self.apply_force(-self.velocity * constant)

    def update(self, time):
        self.acceleration = self.resultant / self.mass
        self.resultant = Vector(0, 0)
        self.velocity += self.acceleration * time
        self.position += self.velocity * time

    def draw(self, screen):
        pygame.draw.circle(screen, (0, 0, 0), (int(self.position.x), int(self.position.y)), self.mass)

    def show(self):
        print(f"v: {self.velocity}, \na: {self.acceleration}, \npos: {self.position}\n")

    def __repr__(self):
        return "Coin(pos=(%.3f, %.3f), size=%d)" % (self.position.x, self.position.y, self.mass)

    __str__ = __repr__


def get_elastic(ball1, ball2, constant):
    global collide
    direction = ball2.position - ball1.position
    elastic = direction.normalize() * (- direction.length + ball2.mass + ball1.mass) * constant
    if - direction.length + ball2.mass + ball1.mass > 0:
        if not collide:
            print("Collide: %s and %s" % (ball1, ball2))
            collide = True
        return -elastic, elastic
    if collide:
        print("Depart\n")
        collide = False
    return Vector(0, 0), Vector(0, 0)
