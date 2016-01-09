#coding: utf-8
import json
import numpy as np
import glob
import matplotlib.pyplot as plt
import matplotlib
import os



"""
MAIN
"""


def main():
    feature_list = json.load(open('figure_features.json'))
    filename_list = json.load(open('figure_features_filename.json'))

    # print feature_list
    # print filename_list

    genshou_name_list = [
        ['clutter', 'gochagocha'],
        ['murmur', 'sarasara'],
        ['twinkle', 'kirakira'],
    ]

    genshou_list = [[] for i in range(len(genshou_name_list))]
    genshou_list_filename = [[] for i in range(len(genshou_name_list))]

    for features, filenames in zip(feature_list, filename_list):
        filename = filenames[0]
        for i, genshou_names in enumerate(genshou_name_list):
            for name in genshou_names:
                if filename.split('/')[1] == name:
                    genshou_list[i] += features
                    genshou_list_filename[i] += filenames
                    break

    genshou_mean_list = []

    for genshou_feat in genshou_list:
        genshou_feat = np.array(genshou_feat)
        genshou_mean_list.append(genshou_feat.mean(0))

    for genshou_name, features, filenames, genshou_mean in \
        zip(genshou_name_list,
            genshou_list,
            genshou_list_filename,
            genshou_mean_list):
        print '======================================='
        print genshou_name
        print '======================================='

        features = np.array(features)
        filenames = np.array(filenames)
        distance = np.linalg.norm(features - genshou_mean, axis=1)

        idx = np.argsort(distance)

        for filename, dist in zip(filenames[idx], distance[idx]):
            print "%s\t%s" % (filename, dist)

if __name__ == "__main__":
    main()
