import cv2
import scanner
import numpy as np
import json
import os


class Figure:
    def __init__(self, filename):
        ext = os.path.splitext(filename)[1]
        if ext == '.png':
            self.loadPNG(filename)
        elif ext == '.json':
            self.loadJSON(filename)

    def loadPNG(self, filename):
        image = cv2.imread(filename)
        self.image = image
        self.scanner = scanner.Scanner(self.image)
        self.vertex = self.scanner.vertex
        self.angle = self.calcAngle(self.vertex)

    def loadJSON(self, filename):
        '''TODO'''
        pass

    def draw(self):
        mat = self.image.copy()
        self.drawVertex(mat)
        cv2.imshow('figure', mat)

    def drawVertex(self, mat):
        for a, b in zip(self.vertex, self.vertex[1:]):
            cv2.line(mat, self.idx2pos(a), self.idx2pos(b), [0, 0, 255])

    def idx2pos(self, idx):
        return (idx[1], idx[0])

    def calcAngle(self, vertex):
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

    def saveJSON(self, filename):
        dic = {
                "vertex": self.vertex.tolist(),
                "angle": self.angle.tolist()
                }
        with open(filename, 'w') as f:
            json.dump(dic, f, sort_keys=True, indent=4)

    def saveTestPNG(self, filename):
        vertexImage = np.zeros(self.image.shape) + 255
        self.drawVertex(vertexImage)
        cv2.imwrite(filename, np.hstack([self.image, vertexImage]))
    
    def rotate(self, vec, x):
        mat = np.array([
            [np.cos(x), np.sin(x)],
            [-np.sin(x), np.cos(x)]        
        ])
        return np.dot(vec, mat)

