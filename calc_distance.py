#coding: utf-8
import json
import numpy as np
import glob
import matplotlib.pyplot as plt
import matplotlib
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
    clusters = clusters[:8]
    angle_array_list = [getAngleArrayFromCluster(cluster)
                        for cluster in clusters]
    return np.hstack(angle_array_list)


def getAngleArrayFromCluster(cluster):
    angle_array = cluster[0]
    return angle_array


def DTW(vec1, vec2):
    d = np.zeros([len(vec1)+1, len(vec2)+1])
    d[:] = np.inf
    d[0, 0] = 0
    for i in range(1, d.shape[0]):
        for j in range(1, d.shape[1]):
            cost = abs(vec1[i-1]-vec2[j-1])
            d[i, j] = cost + min(d[i-1, j], d[i, j-1], d[i-1, j-1])
    return d[-1][-1]

"""
MAIN
"""


def main():
    for json_file in glob.glob("clusters/*.json"):
        _, filename = os.path.split(json_file)
        basename, _ = os.path.splitext(filename)
        en_shape_name, ja_shape_name = basename.split('_')
        json_file_list = \
            sum([glob.glob('jsons/%s/*/*.json' % shape_name)
                 for shape_name in [en_shape_name, ja_shape_name]], [])

        avarage_shape = generateAvarageShapeWithFile(json_file)

        data = []
        for filename in json_file_list:
            json_data = json.load(open(filename))
            shape = json_data['angle']
            print filename
            data.append([filename, DTW(shape, avarage_shape)])

        data = sorted(data, lambda x, y: cmp(x[1], y[1]))
        print data

        with open("distance/%s.txt" % basename, 'w') as f:
            for filename, val in data:
                f.write("%s\t%f\n" % (filename, val))


if __name__ == "__main__":
    main()
