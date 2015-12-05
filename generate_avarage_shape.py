#coding: utf-8
import json
import numpy as np
import glob
import matplotlib.pyplot as plt
import os


"""
描画関数
"""


def generateAvarageShapeWithFile(filename):
    """
    クラスタリング結果から平均図形作成

    Parameters
    ----------
    filename : string
        クラスタリング結果が格納されているファイルの名前
    """
    clusters = json.load(open(filename))
    point_arrays = generateAvarageShape(clusters)
    basename = os.path.basename(filename)
    root, ext = os.path.splitext(basename)
    drawPointArrayList(point_arrays, "avarage_images/%s.png" % root)


def generateAvarageShape(clusters):
    """
    クラスタリング結果から平均図形作成

    Parameters
    ----------
    clusters : array_like
        クラスタリング結果
    """
    component_num = 8
    point_array_list = []
    for cluster in clusters[:component_num]:
        point_array_list.append(getPointArrayFromCluster(cluster))

    point_array_list = point_array_list[:3]

    if len(point_array_list) < component_num:
        point_array_list = [point_array_list[i % len(point_array_list)]
                            for i in range(component_num)]
    return joinPointArrays(point_array_list)


def getPointArrayFromCluster(cluster):
    angle_array = cluster[0]
    return convertAngleToPoint(angle_array)


def joinPointArrays(point_array_list):
    component_num = len(point_array_list)
    expected_total_angle_list = \
        [np.pi * (i * 2 / float(component_num)) for i in range(component_num)]

    retval = []
    pos = np.array([0, 0])
    for point_array, expected_total_angle in zip(point_array_list,
                                                 expected_total_angle_list):
        size = 50.0
        if getToInvert(point_array):
            point_array = invert(point_array)
        total_angle = getTotalAngle(point_array)
        total_move_len = getTotalMoveLen(point_array)
        point_array = rotate(point_array, expected_total_angle - total_angle)
        point_array = scale(point_array, size / total_move_len)
        retval.append(point_array + pos)
        pos = pos + point_array[-1]

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


def drawPointArrayList(point_array_list, filename):
    """
    図形の頂点列から図形を描画する
    Parameters
    ----------
    pos_arrays : array_like, each element is (length, 2) array
    """
    # 画面サイズ
    total_array = np.vstack(point_array_list)
    margin = np.array([50, 50])
    height, width = total_array.max(0) - total_array.min(0) + margin * 2
    y_origin, x_origin = total_array.min(0)
    # import ipdb
    # ipdb.set_trace()
    plt.xlim(width)
    plt.ylim(height)
    for point_array in point_array_list:
        ys, xs = np.array(point_array).T
        plt.plot(xs - x_origin + margin[1], ys - y_origin + margin[0])
    plt.savefig(filename)
    plt.clf()


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
    for json_file in glob.glob("clusters/*.json"):
        generateAvarageShapeWithFile(json_file)


if __name__ == "__main__":
    main()
