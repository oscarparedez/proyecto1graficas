import random
import math
from obj import Obj
from lib import *
from math import cos, sin 
import operations

def color(r, g, b):
    return bytes([int(b*255), int(g*255), int(r*255)])
class Renderer(object):

    def glInit(self):
        self.current_color = color(1, 1, 1)
        self.light = V3(0,0,1)
        self.active_texture = None
        self.active_vertex_array = []

    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height
        self.glClear()

    def glClear(self):
        self.framebuffer = [
            [color(1,1,1) for x in range(self.width)]
            for y in range(self.height)
        ]
        self.zbuffer = [
            [-float('inf') for x in range(self.width)]
            for y in range(self.height)
        ]

    def glViewPort(self, x, y, width, height):
        if x >= 0 and y >= 0 and width >= 0 and height >= 0 and x + width <= self.width and y + height <= self.height:
            self.xvp = x
            self.yvp = y
            self.wvp = width
            self.hvp = height

    def glPoint(self, x, y, color = None):
        self.framebuffer[y+self.yvp][x+self.xvp] = color or self.current_color

    def triangle(self):
        A = next(self.active_vertex_array)
        B = next(self.active_vertex_array)
        C = next(self.active_vertex_array)

        if self.active_texture:
            tA = next(self.active_vertex_array)
            tB = next(self.active_vertex_array)
            tC = next(self.active_vertex_array)

        nA = next(self.active_vertex_array)
        nB = next(self.active_vertex_array)
        nC = next(self.active_vertex_array)

        bbox_min, bbox_max = bbox(A, B, C)    
        normal = norm(cross(sub(B, A), sub(C, A)))
        intensity = dot(normal, self.light)
        if intensity < 0:
            return
        for x in range(bbox_min.x, bbox_max.x + 1):
            for y in range(bbox_min.y, bbox_max.y + 1):
                w, v, u = barycentric(A, B, C, V2(x, y))
                if w < 0 or v < 0 or u < 0:
                    continue
                if self.active_texture:
                    tx = tA.x * w + tB.x * v + tC.x * u
                    ty = tA.y * w + tB.y * v + tC.y * u
                color = self.active_shader(
                    self,
                    triangle=(A, B, C),
                    bar=(w, v, u),
                    texture_coords=(tx, ty),
                    varying_normals=(nA, nB, nC)
                )

                z = A.z * w + B.z * v + C.z * u

                if x < 0 or y < 0:
                    continue

                if x < len(self.zbuffer) and y < len(self.zbuffer[x]) and z > self.zbuffer[x][y]:
                    self.glPoint(x, y, color)
                    self.zbuffer[x][y] = z

    def transform(self, vertex):
        augmented_vertex = [
            vertex.x,
            vertex.y,
            vertex.z,
            1
        ]

        tranformed_vertex = operations.dot(operations.dot(operations.dot(operations.dot(self.Viewport, self.Projection), self.View), self.Model), augmented_vertex)
        tranformed_vertex = [
            (tranformed_vertex[0][0]/tranformed_vertex[3][0]),
            (tranformed_vertex[1][0]/tranformed_vertex[3][0]),
            (tranformed_vertex[2][0]/tranformed_vertex[3][0])
        ]
        return V3(*tranformed_vertex)

    def load(self, filename, translate=(0, 0, 0), scale=(1, 1, 1), rotate=(0, 0, 0)):
        self.loadModelMatrix(translate, scale, rotate)

        model = Obj(filename)
        vertex_buffer_object = []
        for face in model.faces:
            for facepart in face:
                if facepart != [None]:
                    vertex = self.transform(V3(*model.vertices[facepart[0]]))
                    vertex_buffer_object.append(vertex)

            if self.active_texture:
                for facepart in face:
                    if facepart != [None]:
                        tvertex = V3(*model.tvertices[facepart[1]])
                        vertex_buffer_object.append(tvertex)

                for facepart in face:
                    if facepart != [None]:
                        nvertex = V3(*model.normals[facepart[2]])
                        vertex_buffer_object.append(nvertex)

        self.active_vertex_array = iter(vertex_buffer_object)

    def loadModelMatrix(self, translate=(0, 0, 0), scale=(1, 1, 1), rotate=(0, 0, 0)):
        translate = V3(*translate)
        scale = V3(*scale)
        rotate = V3(*rotate)

        translation_matrix = [
            [1, 0, 0, translate.x],
            [0, 1, 0, translate.y],
            [0, 0, 1, translate.z],
            [0, 0, 0, 1],
        ]

        a = rotate.x
        rotation_matrix_x = [
            [1, 0, 0, 0],
            [0, cos(a), -sin(a), 0],
            [0, sin(a),  cos(a), 0],
            [0, 0, 0, 1]
        ]

        a = rotate.y
        rotation_matrix_y = [
            [cos(a), 0,  sin(a), 0],
            [     0, 1,       0, 0],
            [-sin(a), 0,  cos(a), 0],
            [     0, 0,       0, 1]
        ]

        a = rotate.z
        rotation_matrix_z = [
            [cos(a), -sin(a), 0, 0],
            [sin(a),  cos(a), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]

        rotation_matrix = operations.dot(operations.dot(rotation_matrix_x, rotation_matrix_y), rotation_matrix_z)

        scale_matrix = [
            [scale.x, 0, 0, 0],
            [0, scale.y, 0, 0],
            [0, 0, scale.z, 0],
            [0, 0, 0, 1],
        ]

        self.Model = operations.dot(operations.dot(translation_matrix, rotation_matrix), scale_matrix)
    
    def loadViewMatrix(self, x, y, z, center):
        M = [
            [x.x, x.y, x.z,  0],
            [y.x, y.y, y.z, 0],
            [z.x, z.y, z.z, 0],
            [0,     0,   0, 1]
        ]

        O = [
            [1, 0, 0, -center.x],
            [0, 1, 0, -center.y],
            [0, 0, 1, -center.z],
            [0, 0, 0, 1]
        ]

        self.View = operations.dot(M, O)
    def loadProjectionMatrix(self, coeff):
        self.Projection =  [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, coeff, 1]
        ]

    def loadViewportMatrix(self, x = 0, y = 0):
        self.Viewport =  [
            [self.width/2, 0, 0, x + self.width/2],
            [0, self.height/2, 0, y + self.height/2],
            [0, 0, 128, 128],
            [0, 0, 0, 1]
        ]

    def lookAt(self, eye, center, up):
        z = norm(sub(eye, center))
        x = norm(cross(up, z))
        y = norm(cross(z, x))
        self.loadViewMatrix(x, y, z, center)
        self.loadProjectionMatrix(-1 / length(sub(eye, center)))
        self.loadViewportMatrix()

    def draw_arrays(self, polygon):
        if polygon == 'TRIANGLES':
            try:
                while True:
                    self.triangle()
            except StopIteration:
                print('Done.')