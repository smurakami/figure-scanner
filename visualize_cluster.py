#coding: utf-8
import json
import numpy as np
import ipdb
import matplotlib.pyplot as plt

"""
描画関数
"""


def drawClusters(filename):
    """
    クラスタリング結果を可視化する

    Parameters
    ----------
    filename : string
        クラスタリング結果が格納されているファイルの名前
    """
    jsondata = json.load(open(filename))
    for angle_array in jsondata:
        drawAngleArray(angle_array)


def drawPointArray(point_array):
    """
    図形の頂点列から図形を描画する
    Parameters
    ----------
    pos_array : (n, 2) array
    """
    xs, ys = np.array(point_array).T
    # 画面サイズ
    width = 400
    height = 300
    plt.xlim(width)
    plt.ylim(height)
    plt.plot(xs + width/2, ys + height/2)
    plt.show()


def drawAngleArray(angle_array):
    """
    図形の外角列から図形を描画する

    Parameters
    ----------
    angle_array : [Float]
    """
    point_array = convertAngleToPoint(angle_array)
    drawPointArray(point_array)

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
    # 平均座標
    mean_pos = point_array.mean(0)
    # 原点中心に平行移動
    point_array -= mean_pos

    return point_array

"""
MAIN
"""


def main():
    drawClusters("clusters/twinkle.json")


if __name__ == "__main__":
    main()
