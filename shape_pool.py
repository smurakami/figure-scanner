# -*- coding: utf-8 -*-
import json
import numpy as np
import glob
import os
from calc_feature import get_feature
#import ipdb


def main():
    onomatpeia_list = [
        'clutter', 'gochagocha',
        'murmur', 'sarasara',
        'twinkle', 'kirakira',
    ]

    shape_pool = []
    shape_feat_pool = []
    for onomatpeia in onomatpeia_list:
        dirname_pattern = 'jsons/%s/*' % onomatpeia
        print dirname_pattern
        for dirname in sorted(glob.glob(dirname_pattern)):
            shapes, feats = get_shapes_from_dir(dirname, 30)
            shape_pool.append(shapes)
            shape_feat_pool.append(feats)

    np.save('shape_pool.npy', shape_pool)
    np.save('shape_feat_pool.npy', shape_feat_pool)


def get_shapes_from_dir(dirname, shape_len):
    file_list = glob.glob(os.path.join(dirname, '*.json'))

    shape_list = []
    feat_list = []
    for filename in file_list:
        shapes, feats = get_shapes_from_file(filename, shape_len)
        shape_list += shapes
        feat_list += feats

    return shape_list, feat_list


def get_shapes_from_file(filename, shape_len):
    data = json.load(open(filename))
    angle = data["angle"]
    shapes = []
    feats = []

    for i in range(0, len(angle) - shape_len, shape_len):
        shape = (angle[i:i+shape_len])
        feat = get_feature(shape)
        shapes.append(shape)
        feats.append(feat)

    return shapes, feats


if __name__ == '__main__':
    main()
