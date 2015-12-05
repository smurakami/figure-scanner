#coding: utf-8
import json
import numpy as np
import ipdb
import matplotlib.pyplot as plt

"""
描画関数
"""


def genearteAvarageShapeWithFile(filename):
    """
    クラスタリング結果を可視化する

    Parameters
    ----------
    filename : string
        クラスタリング結果が格納されているファイルの名前
    """
    jsondata = json.load(open(filename))
    point_array_list = []
    for cluster in jsondata[:6]:
        point_array_list.append(getPointArrayFromCluster(cluster))
    point_arrays = joinPointArrays(point_array_list)
    drawPointArrayList(point_arrays)


def getPointArrayFromCluster(cluster):
    angle_array = cluster[0]
    return convertAngleToPoint(angle_array)


def joinPointArrays(point_array_list):
    # point_array_list = np.array(point_array_list)
    expected_total_angle_list = [
        np.pi * (0 + 0.25),
        np.pi * (0.5 + 0.25),
        np.pi * (1 + 0.25),
        np.pi * (1.5 + 0.25),
    ]

    retval = []
    pos = np.array([0, 0])
    for point_array, expected_total_angle in zip(point_array_list, expected_total_angle_list):
        size = 100.0
        if getToInvert(point_array):
            point_array = invert(point_array)
        total_angle = getTotalAngle(point_array)
        total_move_len = getTotalMoveLen(point_array)
        point_array = rotate(point_array, expected_total_angle - total_angle)
        point_array = scale(point_array, size / total_move_len)
        print getTotalAngle(point_array)
        print point_array[0]
        retval.append(point_array + pos)
        pos = pos + point_array[-1]

    # point_array_list = point_array_list / total_move_list[:, None] * 100

    # new_list = []
    # pos = np.array([0, 0])
    # for point_array in point_array_list:
    #     new_list.append(point_array + pos)
    #     pos = point_array[-1] + pos
    return retval


def rotate(point_array, rad):
    '''
    図形を回転する
    '''
    mat = np.array([
        [np.cos(rad), np.sin(rad)],
        [-np.sin(rad), np.cos(rad)]])

    return point_array.dot(mat)


def scale(point_array, val):
    '''
    図形を拡大する．
    '''
    return point_array * val


def getTotalMove(point_array):
    '''
    始点と最終点の座標の差
    '''
    return point_array[-1] - point_array[0]


def getTotalMoveLen(point_array):
    '''
    始点と最終点の距離
    '''
    move = getTotalMove(point_array)
    return np.sqrt((move ** 2).sum(-1))


def getTotalAngle(point_array):
    '''
    最初の辺と最後の辺のなす角
    '''
    total_move = getTotalMove(point_array)
    return np.arctan2(total_move[1], total_move[0])


def getToInvert(point_array):
    """
    図形を反転するべきかどうか判定する
    """
    angle = getTotalAngle(point_array)
    point_array = rotate(point_array, -angle)
    x, y = point_array.mean(0)
    return y > 0


def invert(point_array, axis='vertilal'):
    """
    図形を鏡像判定する
    """
    angle = getTotalAngle(point_array)
    point_array = rotate(point_array, -angle)
    point_array[:, 1] = -point_array[:, -1]
    return point_array


def drawPointArray(point_array):
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
    xs, ys = np.array(point_array).T
    plt.plot(xs + width/2, ys + height/2)
    plt.show()


def drawPointArrayList(point_array_list):
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
    genearteAvarageShapeWithFile("clusters/twinkle.json")


if __name__ == "__main__":
    main()
