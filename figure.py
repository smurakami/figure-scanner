import cv2
import scanner
import numpy as np


class Figure:
    def __init__(self, image):
        self.image = image
        self.scanner = scanner.Scanner(self.image)
        self.vertex = self.scanner.vertex
        self.movement = self.calcMovement(self.vertex)

    def draw(self):
        mat = self.image
        self.scanner.draw(mat)
        cv2.imshow('figure', self.image)

    def calcMovement(self, vertex):
        vertex = np.vstack([vertex, vertex[-1]])

        es = [b - a for b, a in zip(vertex, vertex[1:])]
        es = np.vstack([es, es[0]])

        rad = []
        for a, b in zip(es, es[1:]):
            x = np.arctan2(a[1], a[0])
            b_ = self.rotate(b, -x)
            rad.append(np.arctan2(b_[1], b_[0]))
        rad = np.array(rad)
        return rad
    
    def rotate(self, vec, x):
        mat = np.array([
            [np.cos(x), np.sin(x)],
            [-np.sin(x), np.cos(x)]        
        ])
        return np.dot(vec, mat)


