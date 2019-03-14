import nltk
import spacy
import numpy as np
import pandas as pd


def feat_prefix_neighb(tokens, onegrams, bigrams, prefix):

    fprefix = []
    if len(onegrams) != 0:
        for i in range(0, len(onegrams)):
            # temp = nltk.word_tokenize(trigrams[i])
            # indices = tokens.index(temp[0])
            indices = tokens.index(onegrams[i])
            if indices != 0:
                if tokens[indices - 1].lower() in prefix:
                    fprefix.append(1)
                elif indices < len(tokens) - 1:
                    if tokens[indices + 1].lower() in prefix:
                        fprefix.append(1)
                    else:
                        fprefix.append(0)
            else:
                fprefix.append(0)

    if len(bigrams) != 0:
        for i in range(0, len(bigrams)):
            temp = nltk.word_tokenize(bigrams[i])
            indices = tokens.index(temp[0])
            if indices != 0:
                if tokens[indices-1].lower() in prefix:
                    fprefix.append(1)
                elif indices < len(tokens)-2:
                    if tokens[indices + 2].lower() in prefix:
                        fprefix.append(1)
                    else:
                        fprefix.append(0)
                else:
                    fprefix.append(0)
            else:
                fprefix.append(0)
    return fprefix


def feat_prefix_in(onegrams, bigrams,  prefix):

    fprefix_in = []
    if len(onegrams) != 0:
        for i in range(0, len(onegrams)):
            fprefix_in.append(0)  # 1-grams do not contain
    if len(bigrams) != 0:
        for i in range(0, len(bigrams)):
            temp = nltk.word_tokenize(bigrams[i])
            if temp[0].lower() in prefix or temp[1].lower() in prefix:
                fprefix_in.append(1)
            elif temp[0].lower() not in prefix and temp[1].lower() not in prefix:
                fprefix_in.append(0)
    return fprefix_in


def feat_pos_tag(sentence, onegrams, bigrams):

    fpos = []
    ftag = []
    fdep = []
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(sentence)
    if len(onegrams) != 0:
        for i in range(0, len(onegrams)):
            for token in doc:
                # temp = nltk.word_tokenize(bigrams[i])
                if onegrams[i] == str(token):
                    fpos.append(token.pos_)
                    ftag.append(token.tag_)
                    fdep.append(token.dep_)
                    break
    if len(bigrams) != 0:
        for i in range(0, len(bigrams)):
            for token in doc:
                temp = nltk.word_tokenize(bigrams[i])
                if temp[0] == str(token):
                    fpos.append(token.pos_)
                    ftag.append(token.tag_)
                    fdep.append(token.dep_)
                    break
    return fpos, ftag, fdep


def feat_grams(onegrams, bigrams):

    one_grams = [1] * len(onegrams) + [1] * len(bigrams)
    two_grams = [0] * len(onegrams) + [1] * len(bigrams)
    # three_grams = [0] * len(bigrams) + [1] * len(trigrams)
    return one_grams, two_grams


def feat_date(onegrams, bigrams):

    date = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'january', 'february', 'march','april', 'may', 'june', 'july', 'september', 'october', 'november', 'december', 'day', 'month', 'year','eve', 'christmas']

    f_date = []

    if len(onegrams) != 0:
        for i in range(0, len(onegrams)):
            if onegrams[i].lower() in date:
                f_date.append(1)
            else:
                f_date.append(0)

    if len(bigrams) != 0:
        for i in range(0, len(bigrams)):
                temp = nltk.word_tokenize(bigrams[i])
                if temp[0].lower() in date or temp[1].lower() in date:
                    f_date.append(1)
                else:
                    f_date.append(0)
    return f_date


def feat_destination(onegrams, bigrams):

    destinations = ['greece', 'greek', 'athens', 'netherlands', 'italy', 'south', 'korea', 'europe','spain', 'france', 'finland', 'sweden', 'asia', 'continental', 'british','britain', 'uk', 'usa', 'london', 'manchester', 'egeland', 'central', 'america', 'north''east', 'west', 'thailand', 'indonesia', 'india', 'sri', "lan", 'world', 'maldives','islands', 'malaysia', 'zurich', 'german', 'swiss', 'hanover', 'western', 'eastern','australia', 'australian', 'cambridge', 'england', 'jamaica', 'jamaican','hill', 'troy', 'australian', 'las', 'vegas', 'california', 'los', 'angeles''russia', 'russian', 'china', 'italy', 'siberian', 'sudan', 'vietnam', 'indian','new', 'delhi', 'moscow', 'boston', 'albania', 'albanian', 'balkans','atlantic', 'euro',  'macedonia', 'bulgaria', 'sea', 'adriatic', 'vlore','burgas', 'bulgarian', 'macedonian', 'turkish', 'caspioan', 'york','maryland', 'washington', 'county', 'chelsea', 'united', 'zealand', 'paris','miami', 'florida', 'hoolywood', 'denmark', 'angola', 'korea','germany', 'palestinian', 'israel', 'utah', 'french', 'france', 'irish','northwest', 'canada', 'ontario', 'africa', 'jamaica', 'nation', 'nations','international', 'iraq', 'city', 'town', 'country', 'czech', 'republic','portugal', 'ohio', 'river', 'mountain', 'canal', 'canals', 'chicago', 'scadinavian''indonesia', 'egypt', 'earth', 'norway', 'global', 'scotland', 'taiwan','japanese', 'rotterdam', 'scotland', 'sydney', 'houston', 'midlands', 'latin','kingdom', 'mississipi', 'chinese', 'mongolia', 'deutsche', 'central','brixton', 'bristol', 'ireland', 'national', 'cambridge', 'australasia','japan', 'pacific', 'chile', 'federal', 'boulevard', 'world','philadelphia', 'disney', 'venezuela', 'argentina', 'brazil', 'aires', 'buenos','venezuelan', 'dublin', 'frances', 'mexican', 'oklahoma', 'michigan', 'street','edinburgh']

    f_dest = []

    if len(onegrams) != 0:
        for i in range(0, len(onegrams)):
            if onegrams[i].lower() in destinations:
                f_dest.append(1)
            else:
                f_dest.append(0)

    if len(bigrams) != 0:
        for i in range(0, len(bigrams)):
                temp = nltk.word_tokenize(bigrams[i])
                if temp[0].lower() in destinations or temp[1].lower() in destinations:
                    f_dest.append(1)
                else:
                    f_dest.append(0)
    return f_dest

def feat_sym(onegrams, bigrams):

    symbols = ["'s", "'"]
    fsymbol = []

    if len(onegrams) != 0:
        for i in range(0, len(onegrams)):
            if onegrams[i].lower() in symbols:
                fsymbol.append(1)
            else:
                fsymbol.append(0)

    if len(bigrams) != 0:
        for i in range(0, len(bigrams)):
            temp = nltk.word_tokenize(bigrams[i])
            if temp[0].lower() in symbols or temp[1].lower() in symbols:
                fsymbol.append(1)
            else:
                fsymbol.append(0)
    return fsymbol


def feat_pos(fpos):

    fpos_n = []

    for i in range(0, len(fpos)):
        if fpos[i] == 'NOUN':
            fpos_n.append(1)
        else:
            fpos_n.append(0)

    return fpos_n


def feat_all(fprefix, fprefix_in, one_grams, two_grams, fdate, fdest, fsymbol, fpos):

    X = []

    df = pd.DataFrame({'f1': fprefix})
    df['f2'] = pd.Series(fprefix_in, index=df.index)
    df['f3'] = pd.Series(one_grams, index=df.index)
    df['f4'] = pd.Series(two_grams, index=df.index)
    df['f5'] = pd.Series(fdate, index=df.index)
    df['f6'] = pd.Series(fdest, index=df.index)
    df['f7'] = pd.Series(fsymbol, index=df.index)
    df['f8'] = pd.Series(fpos, index=df.index)

    return df, X

