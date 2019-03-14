import numpy as np
import pandas as pd
import nltk
import os
import ast
import sys

def get_labels(type_file):
    found = 0
    all = []
    path = "/Users/elenamilkai/Desktop/project/data/"+type_file+"Y/"
    feat_path = "/Users/elenamilkai/Desktop/project/results/"+type_file+"/grams_all.csv"
    feat = pd.read_csv(feat_path, sep=',', index_col=0, header=None).values.flatten()
    meta = pd.read_csv('results/'+type_file+'/meta.csv', sep=',', index_col=0, header=None).values.flatten()

    sc = set('!,.@_!#$%^&*()<>?/\}{~:]')
    labels = []
    for filename in os.listdir(path):
        if not filename.startswith('.'):
            with open(path + filename, 'r') as myfile:
                data = myfile.read().replace('\n', ' ')
                sentences = nltk.tokenize.sent_tokenize(data)
                for j in range(0, len(sentences)):
                    data = sentences[j]
                    tokens = nltk.word_tokenize(data)
                    for k in range(0, len(tokens)):
                        if (tokens[k] == 'name' or tokens[k] == 'fname' or tokens[k] == 'lname') and tokens[k-1] == '<':
                            found += 1
                            tok = tokens[k+2]
                            if tokens[k+3] != '<':
                                tok = tok + ' ' + tokens[k+3]
                                if tokens[k+4] != '<':
                                    tok = tok + ' ' + tokens[k+4]
                            all.append(tok)
                            # print(tok)
                            for i in range(0, len(feat)):
                                if tok == feat[i] and ast.literal_eval(meta[i])[0] == int(filename.replace('.txt', '')) and ast.literal_eval(meta[i])[1] == j:
                                    labels.append(i)
                                    break

    pd.Series(all).to_csv('results/'+type_file+'/all.csv', sep=',')
    train_labels = [0]*(len(feat))
    for idx in range(0, len(labels)):
        train_labels[labels[idx]] = 1
    pd.Series(train_labels).to_csv('results/'+type_file+'/labels.csv', sep=',')


if __name__ == '__main__':

    type_file = sys.argv[1]
    get_labels(type_file)