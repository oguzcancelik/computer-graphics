import pygame
from OpenGL.GL import *


def load_texture(file_name):
    surface = pygame.image.load(file_name)
    data = pygame.image.tostring(surface, "RGBA", 1)
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, surface.get_width(), surface.get_height(), 0,
                 GL_RGBA, GL_UNSIGNED_BYTE, data)
    return texture_id


class ObjectLoader(object):
    def __init__(self, file_name):
        self.vertices = []
        self.triangle_faces = []
        self.quad_faces = []
        self.polygon_faces = []
        self.normals = []
        try:
            f = open(file_name)
            for line in f:
                if line[:2] == "v ":
                    index1 = line.find(" ") + 1
                    index2 = line.find(" ", index1 + 1)
                    index3 = line.find(" ", index2 + 1)
                    vertex = (round(float(line[index1:index2]), 2),
                              round(float(line[index2:index3]), 2),
                              round(float(line[index3:-1]), 2))
                    self.vertices.append(vertex)

                elif line[:2] == "vn":
                    index1 = line.find(" ") + 1
                    index2 = line.find(" ", index1 + 1)
                    index3 = line.find(" ", index2 + 1)
                    normal = (round(float(line[index1:index2]), 2),
                              round(float(line[index2:index3]), 2),
                              round(float(line[index3:-1]), 2))
                    self.normals.append(normal)

                elif line[0] == "f":
                    line = line.replace("//", "/")
                    face = []
                    i = line.find(" ") + 1
                    for item in range(line.count(" ")):
                        if line.find(" ", i) == -1:
                            face.append(line[i:-1])
                            break
                        face.append(line[i:line.find(" ", i)])
                        i = line.find(" ", i) + 1
                    if line.count("/") == 3:
                        self.triangle_faces.append(tuple(face))
                    elif line.count("/") == 4:
                        self.quad_faces.append(tuple(face))
                    else:
                        self.polygon_faces.append(tuple(face))
            f.close()
        except IOError:
            print("Could not open the .obj file...")

    def render_scene(self):
        if len(self.triangle_faces) > 0:
            glBegin(GL_TRIANGLES)
            for face in self.triangle_faces:
                n = face[0]
                normal = self.normals[int(n[n.find("/") + 1:]) - 1]
                glNormal3fv(normal)
                for f in face:
                    glVertex3fv(self.vertices[int(f[:f.find("/")]) - 1])
            glEnd()

        if len(self.quad_faces) > 0:
            glBegin(GL_QUADS)
            for face in self.quad_faces:
                n = face[0]
                normal = self.normals[int(n[n.find("/") + 1:]) - 1]
                glNormal3fv(normal)
                for f in face:
                    glVertex3fv(self.vertices[int(f[:f.find("/")]) - 1])
            glEnd()

        if len(self.polygon_faces) > 0:
            for face in self.polygon_faces:
                glBegin(GL_POLYGON)
                n = face[0]
                normal = self.normals[int(n[n.find("/") + 1:]) - 1]
                glNormal3fv(normal)
                for f in face:
                    glVertex3fv(self.vertices[int(f[:f.find("/")]) - 1])
                glEnd()

    def render_texture(self, texture_id, texture_coordinates):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glBegin(GL_QUADS)
        for face in self.quad_faces:
            n = face[0]
            normal = self.normals[int(n[n.find("/") + 1:]) - 1]
            glNormal3fv(normal)
            for i, f in enumerate(face):
                glTexCoord2fv(texture_coordinates[i])
                glVertex3fv(self.vertices[int(f[:f.find("/")]) - 1])
        glEnd()
        glDisable(GL_TEXTURE_2D)
