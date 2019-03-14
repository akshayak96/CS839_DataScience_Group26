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
    feat = pd.read_csv(feat_path, sep=',', index_col=0).values.flatten()
    meta = pd.read_csv('results/'+type_file+'/meta.csv', sep=',', index_col=0).values.flatten()
    print(meta)
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
                        if tokens[k] == 'person' and tokens[k-1] == '<':
                            found += 1
                            if len(sc.intersection(tokens[k+2])) == 0:
                                tok = tokens[k+2]
                                if len(sc.intersection(tokens[k+3])) == 0 and tokens[k+3] != '<':
                                    tok = tok + ' ' + tokens[k+3]
                                    if tokens[k+4] != '<' and len(sc.intersection(tokens[k+3])) == 0 and tokens[k+4] != "'s":
                                        tok = tok + ' ' + tokens[k+4]
                                all.append(tok)
                                for i in range(0, len(feat)):
                                    if tok == feat[i] and ast.literal_eval(meta[i])[0] == int(filename.replace('.txt', '')) and ast.literal_eval(meta[i])[1] == j:
                                        labels.append(i)
                                        break
    print(len(labels))
    print(found)
    pd.Series(all).to_csv('results/'+type_file+'/all.csv', sep=',')
    train_labels = [0]*(len(feat)+1)
    for idx in range(0, len(labels)):
        train_labels[labels[idx]] = 1
    pd.Series(train_labels).to_csv('results/'+type_file+'/labels.csv', sep=',')


if __name__ == '__main__':

    type_file = sys.argv[1]
    get_labels(type_file)