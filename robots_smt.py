import pygame

from model.bprogram import BProgram
from model.event_selection.experimental_smt_event_selection_strategy import SMTEventSelectionStrategy
from z3helper import *

H = 250
W = 250

N = 5

p = Real('p')

X = RealVector('x', N)
Y = RealVector('y', N)

dX = RealVector('dx', N)
dY = RealVector('dy', N)

dT = 0.05
speed = 0.2

nextX = [X[i] + dX[i] * dT for i in range(N)]
nextY = [Y[i] + dY[i] * dT for i in range(N)]


def center_of_mass():
    req = Or(And(sum(dX) == speed, sum(dY) == speed, p == 3),
             And(sum(dX) == 0, sum(dY) == -speed, p == 2))

    yield {'request': req, 'wait-for': false}


def obstacle(i):
    obs = And(nextX[i] >= Q(7, 10), nextX[i] <= Q(3, 4),
              nextY[i] >= Q(7, 10), nextY[i] <= Q(3, 4))

    yield {'block': obs, 'wait-for': false}


def structure_x():
    yield {'block': Or([Not(dX[i] == dX[i - 1]) for i in range(1, N)]), 'wait-for': false}


def structure_y():
    yield {'block': Or([Not(dY[i] == dY[i - 1]) for i in range(1, N)]), 'wait-for': false}


def init_x():
    yield {'request': And([X[i] == Q(i, 10) for i in range(N)])}


def init_y():
    yield {'request': And([Y[i] == Q(i, 10) for i in range(N)])}


def step(i):
    m = yield {}
    while True:
        d = And(X[i] == m.eval(nextX[i]), Y[i] == m.eval(nextY[i]))
        m = yield {'request': d, 'block': Not(d)}


def walls(i):
    yield {'block': Or(nextX[i] < 0, nextX[i] > 1, nextY[i] < 0, nextY[i] > 1), 'wait-for': false}


def display():
    pygame.init()
    screen = pygame.display.set_mode((W + 15, H + 15))

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                yield {'block': true for i in range(N)}

        m = yield {}
        screen.fill((0, 0, 0))

        for i in range(N):
            x = toFloat(m[X[i]])
            y = toFloat(m[Y[i]])
            pygame.draw.rect(screen, (255, 100, 0),
                             pygame.Rect(5 + x * H, 5 + y * W, 5, 5))

        pygame.draw.rect(screen, (255, 255, 255),
                         pygame.Rect(11.25 + 0.7 * H, 11.25 + 0.7 * W, 10, 10))

        pygame.display.flip()
        clock.tick(60)


bounds = [walls(i) for i in range(N)]
step = [step(i) for i in range(N)]
obstacle = [obstacle(i) for i in range(N)]

if __name__ == "__main__":
    b_program = BProgram(
        bthreads=[display(), init_x(), init_y(), center_of_mass(), structure_x(),
                  structure_y()] + step + bounds + obstacle,
        event_selection_strategy=SMTEventSelectionStrategy())

    b_program.run()
