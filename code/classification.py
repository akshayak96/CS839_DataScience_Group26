from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn import svm
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import pandas as pd
import accuracy as acc


def log_regres(trainX, trainY, testX):

    clf = LogisticRegression(fit_intercept=True).fit(trainX, trainY)
    clf.fit(trainX, trainY)
    pred = clf.predict(testX)
    return pred


def lin_regres(trainX, trainY, testX):

    reg = LinearRegression().fit(trainX, trainY)
    p = reg.predict(testX)
    pred = []
    for i in range(0, len(p)):
        if p[i] >= 0:
            pred.append(1)
        else:
            pred.append(0)
    return pred


def svm_class(trainX, trainY, testX):

    clf = svm.SVC(C=5)
    clf.fit(trainX, trainY)
    return clf.predict(testX)


def tree_class(trainX, trainY, testX):

    clf = tree.DecisionTreeClassifier(criterion="entropy", random_state=0)
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

    print('-----Logistic Regression----')
    pred = log_regres(np.array(trainX), trainY, np.array(testX))
    acc.comp_acc(testY, pred)

    print('----Linear Regression----')
    pred = lin_regres(np.array(trainX), trainY, np.array(testX))
    acc.comp_acc(testY, pred)
    print('\n')

    print('\n')
    print('----SVM----')
    pred = svm_class(np.array(trainX), trainY, np.array(testX))
    acc.comp_acc(testY, pred)
    print('\n')
    print('----Tree Classification----')
    pred = tree_class(np.array(trainX), trainY, np.array(testX))
    acc.comp_acc(testY, pred)
    print('\n')
    print('----Random Forest----')
    pred = rf_class(np.array(trainX), trainY, np.array(testX))
    acc.comp_acc(testY, pred)
    print('\n')
    pd.Series(pred).to_csv('pred.csv', sep=',')





