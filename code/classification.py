from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn import svm
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import pandas as pd
import accuracy as acc


def log_regres(trainX, trainY, testX):

    clf = LogisticRegression(random_state=0, solver='liblinear').fit(trainX, trainY)
    return clf.predict(testX)


def lin_regres(trainX, trainY, testX):

    reg = LinearRegression().fit(trainX, trainY)
    return reg.predict(testX)


def svm_class(trainX, trainY, testX):

    clf = svm.SVC(gamma='scale')
    clf.fit(trainX, trainY)
    return clf.predict(testX)


def tree_class(trainX, trainY, testX):

    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(trainX, trainY)
    return clf.predict(testX)


def rf_class(trainX, trainY, testX):

    clf = RandomForestClassifier(n_estimators=10, max_depth=5, random_state=0)
    clf = clf.fit(trainX, trainY)
    return clf.predict(testX)


if __name__ == '__main__':

    trainX = pd.read_csv('results/train/X.csv', sep=',', index_col=0).values
    trainY = pd.read_csv('results/train/labels.csv', sep=',', index_col=0, header=None).values.flatten()
    testX = pd.read_csv('results/test/X.csv', sep=',', index_col=0).values
    testY = pd.read_csv('results/test/labels.csv', sep=',', index_col=0, header=None).values.flatten()

    pred = lin_regres(np.array(trainX), trainY, np.array(testX))
    print(pred)
    print(testY)
    acc.comp_acc(testY, pred)

    pred = log_regres(np.array(trainX), trainY, np.array(testX))
    print(pred)
    print(testY)
    acc.comp_acc(testY, pred)

    pred = svm_class(np.array(trainX), trainY, np.array(testX))
    print(pred)
    print(testY)
    acc.comp_acc(testY, pred)

    pred = tree_class(np.array(trainX), trainY, np.array(testX))
    print(pred)
    print(testY)
    acc.comp_acc(testY, pred)

    pred = rf_class(np.array(trainX), trainY, np.array(testX))
    print(pred)
    print(testY)
    acc.comp_acc(testY, pred)



