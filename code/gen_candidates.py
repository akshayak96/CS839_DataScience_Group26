import numpy as np
import pandas as pd
import os
import nltk
from nltk.util import ngrams
from nltk import word_tokenize
from collections import Counter
import re
import string
import spacy
from nltk.corpus import stopwords
import features as feat
import sys


def create_bgramms(type_file):

    prefix = ['mr', 'mrs', 'ms', 'miss', 'mx', 'master', 'maid', 'madam','professor', 'prof', 'chief', 'phd', 'dphil', 'dr', 'doc','advocate', 'economist', 'chancellor', 'lord', 'sir', 'dame','jr', 'duke', 'don', 'president', 'prince', 'king', 'emperor','queen', 'leader', 'emperor', 'empress', 'lord', 'tsar', 'tsarina','count', 'countess', 'duchess', 'vice', 'ambassador', 'secretary','governor', 'mayor', 'councillor', 'speaker', 'doctor', 'representative','senator', 'hon', 'aunt', 'uncle', 'prelate', 'premier', 'Prefect', 'burgess''envoy', 'provost', 'priest','father', 'catholic', 'cardinal', 'dean', 'minister','reader', 'teacher', 'christ', 'major', 'general', 'officer', 'captain', 'engineer','principal', 'coach', 'player', 'citizen', 'male', 'female', 'mother', 'father', 'executive','founder', 'lawyer', 'former', 'challenger', 'laureate', 'pioneer', 'chairman', 'boss', 'member','challenger', 'minister', 'explained', 'boss','member', 'analyst', 'commissioner', 'explains','commented', 'creator', 'director',  'co-chairman', 'former', 'manager', 'who', 'designer','told', 'star', 'writer', 'ruled', 'actor', 'spokesman', 'nominee', 'actress', 'daughter','winner', 'artist', 'anchor', 'model', 'comedian', 'spokeswoman', 'singer','member', 'prop']

    path = "/Users/elenamilkai/Desktop/project/data/"+type_file+'/'
    stop_words = set(stopwords.words('english'))
    stop_words.add('however')
    stop_words.add('although')
    sc = set('!,.@_!#$%^&*()<>?/\}{~:]')

    grams_all = []
    bigrams_all = []
    trigrams_all = []
    fprefix_all = []
    fprefix_in_all = []
    fpos_all = []
    ftag_all = []
    fdep_all = []
    three_grams_all = []
    two_grams_all = []
    one_grams = []
    onegrams_all = []
    one_grams_all = []
    meta_one = []
    date_all =[]
    dest_all = []
    sym_all = []
    X = []
    meta = []
    i = 0
    for filename in os.listdir(path):
        if not filename.startswith('.'):
            i += 1
            print('--------File--------> '+str(i)+'\n')
            with open(path + filename, 'r') as myfile:
                data = myfile.read().replace('\n', ' ')
                sentences = nltk.tokenize.sent_tokenize(data)
                for j in range(0, len(sentences)):
                    data = sentences[j]

                    tokens = nltk.word_tokenize(data)
                    bigrams = list(ngrams(tokens, 2))
                    tokens_up = []
                    bigrams_up = []
                    meta_bi = []
                    meta_one = []

                    for t in range(0, len(tokens)):
                        if str.isupper(tokens[t][0]) is True and t != 0 and tokens[t].isupper() is False and \
                                not tokens[t].lower() in stop_words and not tokens[t].lower() in prefix:
                            tokens_up.append(tokens[t])
                            meta_one.append([int(filename.replace('.txt', '')), j])

                    for t in range(0, len(bigrams)):
                        if str.isupper(bigrams[t][0][0]) is True and str.isupper(bigrams[t][1][0]) is True \
                                and not bigrams[t][0].lower() in stop_words and not bigrams[t][1].lower() in stop_words \
                                and len(sc.intersection(bigrams[t][0])) == 0 and len(sc.intersection(bigrams[t][1])) == 0 \
                                and not bigrams[t][0].lower() in prefix and not bigrams[t][1].lower() in prefix:
                            bigrams_up.append(" ".join(bigrams[t]))
                            meta_bi.append([int(filename.replace('.txt', '')), j])

                    fprefix = feat.feat_prefix_neighb(tokens, tokens_up, bigrams_up, prefix)
                    fprefix_in = feat.feat_prefix_in(tokens_up, bigrams_up, prefix)
                    fpos, ftag, fdep = feat.feat_pos_tag(data, tokens_up, bigrams_up)
                    one_grams, two_grams = feat.feat_grams(tokens_up, bigrams_up)
                    fdest = feat. feat_destination(tokens_up, bigrams_up)
                    fdate = feat.feat_date(tokens_up, bigrams_up)
                    sym = feat.feat_sym(tokens_up, bigrams_up)

                    if len(tokens_up) != 0:
                        onegrams_all = onegrams_all + tokens_up
                        meta = meta + meta_one
                        grams_all = grams_all + tokens_up
                    if len(bigrams_up) != 0:
                        bigrams_all = bigrams_all + bigrams_up
                        meta = meta + meta_bi
                        grams_all = grams_all + bigrams_up

                    fprefix_all = fprefix_all + fprefix
                    fprefix_in_all = fprefix_in_all + fprefix_in
                    fpos_all = fpos_all + fpos
                    ftag_all = ftag_all + ftag
                    fdep_all = fdep_all + fdep
                    two_grams_all = two_grams_all + two_grams
                    one_grams_all = one_grams_all + one_grams
                    dest_all = dest_all + fdest
                    date_all = date_all + fdate
                    sym_all = sym_all + sym
                    fpos_tel = feat.feat_pos(fpos_all)
                    X, buf = feat.feat_all(fprefix_all, fprefix_in_all, one_grams_all, two_grams_all, date_all, dest_all, sym_all, fpos_tel)

    pd.Series(bigrams_all).to_csv('results/'+type_file+'/bigrams_all.csv', sep=',')
    pd.Series(trigrams_all).to_csv('results/'+type_file+'/trigrams_all.csv', sep=',')
    pd.Series(grams_all).to_csv('results/'+type_file+'/grams_all.csv', sep=',')
    pd.Series(fprefix_all).to_csv('results/'+type_file+'/fprefix_all.csv', sep=',')
    pd.Series(fprefix_in_all).to_csv('results/'+type_file+'/fprefix_in_all.csv', sep=',')
    pd.Series(fpos_all).to_csv('results/'+type_file+'/fpos_all.csv', sep=',')
    pd.Series(ftag_all).to_csv('results/'+type_file+'/ftag_all.csv', sep=',')
    pd.Series(fdep_all).to_csv('results/'+type_file+'/fdep_all.csv', sep=',')
    pd.Series(two_grams_all).to_csv('results/'+type_file+'/two_grams_all.csv', sep=',')
    pd.Series(three_grams_all).to_csv('results/'+type_file+'/three_grams_all.csv', sep=',')
    pd.Series(list(buf)).to_csv('results/'+type_file+'/Xbuff.csv', sep=',')
    X.to_csv('results/'+type_file+'/X.csv', sep=',')
    pd.Series(meta).to_csv('results/'+type_file+'/meta.csv', sep=',')
    pd.Series(one_grams).to_csv('results/' + type_file + '/one-grams.csv', sep=',')


if __name__ == '__main__':

    type_file = sys.argv[1]
    create_bgramms(type_file)
