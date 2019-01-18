import math
import os

from OpenGL.GLU import *

from graphics import *


class Cube(object):
    left_key = False
    right_key = False
    up_key = False
    down_key = False
    w_key = False
    s_key = False
    angle = 0
    angle2 = 0
    cube_angle = 0
    dist = 0.5

    def __init__(self):
        self.vertices = []
        self.faces = []
        self.rubik_id = load_texture("rubik.png")
        self.surface_id = load_texture("ConcreteTriangles.png")
        self.coordinates = [0, 0, 0]
        self.ground = ObjectLoader("plane.txt")
        self.cube = ObjectLoader("cube.txt")

    def render_scene(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # glClearColor(0.7,0.9,1,1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        # Add ambient light:
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
        # Add positioned light:
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [2, 2, 2, 1])
        glLightfv(GL_LIGHT0, GL_POSITION, [4, 8, 1, 1])
        glTranslatef(0, -0.5, 0)
        gluLookAt(0, 0, 0, math.sin(math.radians(self.angle)), math.sin(math.radians(self.angle2)),
                  math.cos(math.radians(self.angle)) * -1, 0, 1, 0)
        glTranslatef(self.coordinates[0], self.coordinates[1], self.coordinates[2])
        self.ground.render_texture(self.surface_id, ((0, 0), (2, 0), (2, 2), (0, 2)))
        glTranslatef(-7.5, 2, 0)
        glRotatef(self.cube_angle, 0, 1, 0)
        glRotatef(45, 1, 0, 0)
        self.cube.render_texture(self.rubik_id, ((0, 0), (1, 0), (1, 1), (0, 1)))

    def move_forward(self):
        self.coordinates[0] += self.dist

    def move_back(self):
        self.coordinates[0] -= self.dist

    def move_left(self):
        self.coordinates[2] -= self.dist

    def move_right(self):
        self.coordinates[2] += self.dist

    def move_up(self):
        self.coordinates[1] -= self.dist

    def move_down(self):
        self.coordinates[1] += self.dist

    def rotate(self, n, m):
        if self.angle >= 360 or self.angle <= -360:
            self.angle = 0
        self.angle += n
        if -360 <= self.angle2 + m <= 360:
            self.angle2 += m

    def update(self):
        if self.left_key:
            self.move_left()
        elif self.right_key:
            self.move_right()
        elif self.up_key:
            self.move_forward()
        elif self.down_key:
            self.move_back()
        elif self.w_key:
            self.move_up()
        elif self.s_key:
            self.move_down()

        pos = pygame.mouse.get_pos()
        if pos[0] < 100 and pos[1] in range(99, 540):
            self.rotate(-2, 0)
        elif pos[0] > 540 and pos[1] in range(99, 540):
            self.rotate(2, 0)
        if pos[1] < 100 and pos[0] in range(99, 540):
            self.rotate(0, 2)
        elif pos[1] > 540 and pos[0] in range(99, 540):
            self.rotate(0, -2)

        if self.cube_angle >= 360:
            self.cube_angle = 0
        else:
            self.cube_angle += 0.5

    def keyup(self):
        self.left_key = False
        self.right_key = False
        self.up_key = False
        self.down_key = False
        self.w_key = False
        self.s_key = False

    def delete_texture(self):
        glDeleteTextures(self.rubik_id)
        glDeleteTextures(self.surface_id)


os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
pygame.display.set_mode((640, 640), pygame.DOUBLEBUF | pygame.OPENGL)
pygame.display.set_caption("Computer Graphics")
clock = pygame.time.Clock()
keep_loop = True
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(45, 640.0 / 640.0, 0.1, 200.0)
glEnable(GL_DEPTH_TEST)
glEnable(GL_LIGHTING)
glEnable(GL_LIGHT0)
glEnable(GL_NORMALIZE)

cube = Cube()
while keep_loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keep_loop = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                cube.move_left()
                cube.left_key = True
            elif event.key == pygame.K_RIGHT:
                cube.move_right()
                cube.right_key = True
            elif event.key == pygame.K_UP:
                cube.move_forward()
                cube.up_key = True
            elif event.key == pygame.K_DOWN:
                cube.move_back()
                cube.down_key = True
            elif event.key == pygame.K_w:
                cube.move_up()
                cube.w_key = True
            elif event.key == pygame.K_s:
                cube.move_down()
                cube.s_key = True
            elif event.key == pygame.K_r:
                cube.coordinates = [0, 0, 0]

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                cube.keyup()
            elif event.key == pygame.K_RIGHT:
                cube.keyup()
            elif event.key == pygame.K_UP:
                cube.keyup()
            elif event.key == pygame.K_DOWN:
                cube.keyup()
            elif event.key == pygame.K_w:
                cube.keyup()
            elif event.key == pygame.K_s:
                cube.keyup()

    cube.update()
    cube.render_scene()
    pygame.display.flip()
    clock.tick(30)
cube.delete_texture()
pygame.quit()
