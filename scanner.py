import numpy as np
import cv2
import sys

sys.setrecursionlimit(10000)

class Scanner:
    def __init__(self, color_image):
        image = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
        self.first_idx = self.getFirstIdx(image)
        self.vertex = self.scan(image, self.first_idx)
        self.counter = 0

    def getFirstIdx(self, image):
        th = (int(image.max()) + int(image.min())) / 2
        for i in range(image.shape[0]):
            to_break = False
            for j in range(image.shape[1]):
                if image[i, j] < th:
                    to_break = True
                    break
            if to_break:
                break
        return np.array([i, j])

    def scan(self, image, first_idx):
        th = 200
        edge_len = 5
        bmap = image < th
        self.bmap = bmap.copy()
        directions = [
                np.array([ 1, 0]),
                np.array([ 1, 1]),
                np.array([ 0, 1]),
                np.array([-1, 1]),
                np.array([-1, 0]),
                np.array([-1,-1]),
                np.array([ 0,-1]),
                np.array([ 1,-1]),
                ]

        self.vertex = np.array([first_idx])
        def next(idx):
            flg = bmap[tuple(idx)]
            if not flg:
                return
            bmap[tuple(idx)] = False

            dist = np.sqrt(((self.vertex - idx) ** 2).sum(1))
            if (edge_len < dist).all():
                self.vertex = np.vstack([self.vertex, idx])

            for d in directions:
                next(idx + d)

        next(first_idx)

        self.bmap_after = bmap.copy()
        return self.vertex

    def idx2pos(self, idx):
        return (idx[1], idx[0])

    def draw(self, mat):
        mat[:, :, :] = 0
        cv2.circle(mat, self.idx2pos(self.first_idx), 4, (0, 255, 255))

        max_idx = min(len(self.vertex) - 1, self.counter)

        for a, b in zip(self.vertex, self.vertex[1:])[:max_idx]:
            cv2.line(mat, self.idx2pos(a), self.idx2pos(b), [0, 0, 255])
        self.counter += 1


def scan(image):
    scanner = Scanner(image)
    return scanner.vertex

