import os
import numpy as np
import random
from shutil import copyfile
import pandas as pd



def select_files():
    """
    We took our data from "http://mlg.ucd.ie/datasets/bbc.html". There are 5 different types of articles,
    {'business', 'entertainment', 'politics', 'sport', 'tech'}. We select randomly 80 different files
    from each category. So, initially we have 400 files. Some of them will be pruned in tha cleaning process.
    :return: 400 files from the 5 different categories.
    """

    types = ['business', 'entertainment', 'politics', 'sport', 'tech']
    path = "/Users/elenamilkai/Desktop/bbc/"
    tmp = "/Users/elenamilkai/Desktop/data"
    lengths = []
    for i in range(0, len(types)):
        lengths.append(len([name for name in os.listdir(path+types[i])]))

    counter = 1
    for i in range(0, len(types)):
        indices = random.sample(range(1, lengths[i]), 80)
        for j in range(0, len(indices)):
            src = path+types[i]+'/'+format(indices[j], '03d')+'.txt'
            dst = format(counter, '03d') + ".txt"
            dst = '/Users/elenamilkai/Desktop/project/data/' + dst
            os.rename(src, dst)
            # shutil.copy(src, tmp)
            counter += 1
    print(counter)


def rename_files():

    i = 0

    for filename_u in os.listdir("/Users/elenamilkai/Desktop/project/data/unlabeled"):
        found = 0
        for filename_l in os.listdir("/Users/elenamilkai/Desktop/project/data/labeled"):
            if filename_u == filename_l:
                i += 1
                dst = format(i, '03d') + ".txt"
                src = "/Users/elenamilkai/Desktop/project/data/labeled/" + filename_l
                dst = '/Users/elenamilkai/Desktop/project/data/labeledFinal/' + dst
                # os.rename(src, dst)
                copyfile(src, dst)
                found = 1
                break
        if found == 1:
            dst = format(i, '03d') + ".txt"
            src = "/Users/elenamilkai/Desktop/project/data/unlabeled/" + filename_u
            dst = '/Users/elenamilkai/Desktop/project/data/unlabeledFinal/' + dst
            # os.rename(src, dst)
            copyfile(src, dst)
        

def create_IJ(files, size):
    random.shuffle(files)
    trainSet = files[0:size:1]
    testSet = files[size:len(files):1]
    print(len(testSet))
    i = 0

    for filename in os.listdir("/Users/elenamilkai/Desktop/project/data/unlabeled/"):
        if not filename.startswith('.'):
            if int(filename.replace('.txt', '')) in trainSet:
                src = "/Users/elenamilkai/Desktop/project/data/unlabeled/" + filename
                dst = '/Users/elenamilkai/Desktop/project/data/train/' + filename
                copyfile(src, dst)
            if int(filename.replace('.txt', '')) in testSet:
                src = "/Users/elenamilkai/Desktop/project/data/unlabeled/" + filename
                dst = '/Users/elenamilkai/Desktop/project/data/test/' + filename
                copyfile(src, dst)
        i += 1
    i = 0

    for filename in os.listdir("/Users/elenamilkai/Desktop/project/data/labeled/"):
        if not filename.startswith('.'):
            if int(filename.replace('.txt', '')) in trainSet:
                src = "/Users/elenamilkai/Desktop/project/data/labeled/" + filename
                dst = '/Users/elenamilkai/Desktop/project/data/trainY/' + filename
                copyfile(src, dst)
            if int(filename.replace('.txt', '')) in testSet:
                src = "/Users/elenamilkai/Desktop/project/data/labeled/" + filename
                dst = '/Users/elenamilkai/Desktop/project/data/testY/' + filename
                copyfile(src, dst)

    return trainSet, testSet


if __name__ == '__main__':
    train, test = create_IJ(list(range(1, 317, 1)), 216)
    print(train)
    print(test)
    pd.Series(train).to_csv('results/train_idx.csv', sep=',')
    pd.Series(test).to_csv('results/test_idx.csv', sep=',')


