import pickle
import os
import pandas as pd


def save_to_pkl(filename, data):
    """data为任意数据格式"""
    with open('data/{}.pkl'.format(filename), 'wb') as f:
        pickle.dump(data, f)
        print('Save {} is done! '.format(filename))


def read_to_pkl(filename):
    with open('data/{}.pkl'.format(filename), 'rb') as f:
        data = pickle.load(f)
        print('Read {} is done! '.format(filename))
    return data


def save_to_txt(data, filename):
    """data为DataFrame的数据格式"""
    filename = 'data/{}.txt'.format(filename)
    if os.path.exists(filename):
        os.remove(filename)

    try:
        cols = list(data.columns)
        header = '\t'.join(cols) + '\n'
        with open(filename, 'a') as f:
            f.write(header)
        data_values = data.values

        for row in data_values:
            row = '\t'.join(row) + '\n'
            with open(filename, 'a') as f:
                f.write(row)
        print('Save {} is done!'.format(filename))
    except Exception as e:
        print(e)


def transform_to_list(data):
    """data为DataFrame数据类型"""
    values = data.values
    cols = list(data.columns)
    w = []
    for i in values:
        d = {}
        for j in cols:
            d[j] = i[cols.index(j)]
        w.append(d)
    return w


if __name__ == '__main__':
    pass
