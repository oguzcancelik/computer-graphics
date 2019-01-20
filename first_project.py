import os
import random

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *


def set_colors():
    global colors
    colors = [(random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)) for _ in range(36 * len(cube_valid))]


def set_vertices(i=1):
    global vertice
    vertice.clear()
    vertice.append((
        (i, -i, -i),
        (i, i, -i),
        (-i, i, -i),
        (-i, -i, -i),
        (i, -i, i),
        (i, i, i),
        (-i, -i, i),
        (-i, i, i))
    )
    vertice.append((
        (i + 3 * i, -i, -i),
        (i + 3 * i, i, -i),
        (i + i, i, -i),
        (i + i, -i, -i),
        (i + 3 * i, -i, i),
        (i + 3 * i, i, i),
        (i + i, -i, i),
        (i + i, i, i))
    )
    vertice.append((
        (-i - 3 * i, -i, -i),
        (-i - 3 * i, i, -i),
        (-i - i, i, -i),
        (-i - i, -i, -i),
        (-i - 3 * i, -i, i),
        (-i - 3 * i, i, i),
        (-i - i, -i, i),
        (-i - i, i, i))
    )
    vertice.append((
        (i, i + i, -i),
        (i, i + 3 * i, -i),
        (-i, i + 3 * i, -i),
        (-i, i + i, -i),
        (i, i + i, i),
        (i, i + 3 * i, i),
        (-i, i + i, i),
        (-i, i + 3 * i, i))
    )
    vertice.append((
        (i, -i - i, -i),
        (i, -i - 3 * i, -i),
        (-i, -i - 3 * i, -i),
        (-i, -i - i, -i),
        (i, -i - i, i),
        (i, -i - 3 * i, i),
        (-i, -i - i, i),
        (-i, -i - 3 * i, i))
    )
    vertice.append((
        (i + 3 * i, i + i, -i),
        (i + 3 * i, i + 3 * i, -i),
        (i + i, i + 3 * i, -i),
        (i + i, i + i, -i),
        (i + 3 * i, i + i, i),
        (i + 3 * i, i + 3 * i, i),
        (i + i, i + i, i),
        (i + i, i + 3 * i, i))
    )
    vertice.append((
        (i + 3 * i, -i - i, -i),
        (i + 3 * i, -i - 3 * i, -i),
        (i + i, -i - 3 * i, -i),
        (i + i, -i - i, -i),
        (i + 3 * i, -i - i, i),
        (i + 3 * i, -i - 3 * i, i),
        (i + i, -i - i, i),
        (i + i, -i - 3 * i, i))
    )
    vertice.append((
        (-i - 3 * i, i + i, -i),
        (-i - 3 * i, i + 3 * i, -i),
        (-i - i, i + 3 * i, -i),
        (-i - i, i + i, -i),
        (-i - 3 * i, i + i, i),
        (-i - 3 * i, i + 3 * i, i),
        (-i - i, i + i, i),
        (-i - i, i + 3 * i, i))
    )
    vertice.append((
        (-i - 3 * i, -i - i, -i),
        (-i - 3 * i, -i - 3 * i, -i),
        (-i - i, -i - 3 * i, -i),
        (-i - i, -i - i, -i),
        (-i - 3 * i, -i - i, i),
        (-i - 3 * i, -i - 3 * i, i),
        (-i - i, -i - i, i),
        (-i - i, -i - 3 * i, i))
    )


def cube():
    global vertice, colors, colorful, samecolor
    glBegin(GL_QUADS)
    temp = 0
    x = 0
    for i in range(len(vertice)):
        if not cube_valid[i]:
            continue
        if samecolor:
            x = 0
            temp = 0
        for surface in surfaces:
            y = temp
            x += 1
            for vertex in surface:
                y += 1
                if colorful:
                    glColor3fv(colors[y])
                else:
                    glColor3fv(colors[x])
                glVertex3fv(vertice[i][vertex])
            temp += 6
    glEnd()


def main():
    global colorful, samecolor
    set_colors()
    i = 1
    speed = 1
    set_vertices(i)
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    display = (1200, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(30, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0, 0, -10)
    rotate = True
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    speed *= 2
                if event.key == pygame.K_DOWN:
                    speed /= 2
                if event.key == pygame.K_1:
                    cube_valid[0] = True if not cube_valid[0] else False
                if event.key == pygame.K_2:
                    cube_valid[1] = True if not cube_valid[1] else False
                if event.key == pygame.K_3:
                    cube_valid[2] = True if not cube_valid[2] else False
                if event.key == pygame.K_4:
                    cube_valid[3] = True if not cube_valid[3] else False
                if event.key == pygame.K_5:
                    cube_valid[4] = True if not cube_valid[4] else False
                if event.key == pygame.K_6:
                    cube_valid[5] = True if not cube_valid[5] else False
                if event.key == pygame.K_7:
                    cube_valid[6] = True if not cube_valid[6] else False
                if event.key == pygame.K_8:
                    cube_valid[7] = True if not cube_valid[7] else False
                if event.key == pygame.K_9:
                    cube_valid[8] = True if not cube_valid[8] else False
                if event.key == pygame.K_SPACE:
                    samecolor = True if not samecolor else False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    rotate = True if not rotate else False
                if event.button == 2:
                    colorful = True if not colorful else False
                    set_colors()
                if event.button == 3:
                    set_colors()
                if event.button == 4:
                    i *= 2
                    set_vertices(i)
                if event.button == 5:
                    i = i / 2
                    set_vertices(i)
        if rotate:
            glRotatef(speed, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        cube()
        pygame.display.flip()
        pygame.time.wait(10)


surfaces = (
    (0, 1, 2, 3),
    (3, 2, 7, 6),
    (6, 7, 5, 4),
    (4, 5, 1, 0),
    (1, 5, 7, 2),
    (4, 0, 3, 6)
)

colors = ()
vertice = []
cube_valid = [True, False, False, False, False, False, False, False, False]
colorful = False
samecolor = True

if __name__ == '__main__':
    main()
