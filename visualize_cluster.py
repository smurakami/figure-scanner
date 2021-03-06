#coding: utf-8
import json
import numpy as np
import ipdb
import matplotlib.pyplot as plt
import sys

"""
描画関数
"""


def drawClustersInFile(filename):
    """
    クラスタリング結果を可視化する

    Parameters
    ----------
    filename : string
        クラスタリング結果が格納されているファイルの名前
    """
    jsondata = json.load(open(filename))
    for cluster in jsondata:
        drawCluster(cluster)


def drawCluster(cluster):
    """
    クラスタ中の全ての点列を描画
    """
    point_array_cluster = []
    for angle_array in cluster:
        point_array_cluster.append(convertAngleToPoint(angle_array))
    drawPointArrays(point_array_cluster)


def drawPointArrays(point_array_list):
    """
    図形の頂点列から図形を描画する
    Parameters
    ----------
    pos_arrays : array_like, each element is (length, 2) array
    """
    # 画面サイズ
    width = 400
    height = 300
    plt.xlim(width)
    plt.ylim(height)
    for point_array in point_array_list:
        xs, ys = np.array(point_array).T
        plt.plot(xs + width/2, ys + height/2)
    plt.show()


"""
汎用関数
"""


def nextPos(pos, direction):
    """
    posからdirection方向に進んだ位置を計算する．
    Parameters
    ----------
    pos : np.ndarray
    direction : float

    Returns
    -------
    pos : np.ndarray
    """
    edge_len = 5
    edge = np.array([np.cos(direction), np.sin(direction)]) * edge_len
    return pos + edge


def convertAngleToPoint(angle_array):
    """
    外角列から点列を生成する
    Parameters
    ----------
    angle_array : array_like
        図形の外角列

    Returns
    -------
    point_array : np.ndarray
        図形の頂点配列
    """
    angle_array = np.array(angle_array)
    direction = 0
    first_pos = np.array([0, 0])
    pos = nextPos(first_pos, direction)
    point_array = [first_pos, pos]
    for angle in angle_array:
        direction += angle
        pos = nextPos(pos, direction)
        point_array.append(pos)

    point_array = np.vstack(point_array)

    return point_array

"""
MAIN
"""


def main():
    if len(sys.argv) >= 2:
        filename = sys.argv[1]
    else:
        filename = "clusters/twinkle.json"
    drawClustersInFile(filename)


if __name__ == "__main__":
    main()
