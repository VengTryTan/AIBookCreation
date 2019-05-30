# -*- coding: utf-8 -*-
import MeCab
import pandas as pd
import numpy as np
import warnings


class Text_pn():
    def __init__(self):

        self.m = MeCab.Tagger()
        # set pn dictionary
        self.pndic = {}
        with open("jpdb.dic", 'r', encoding='utf-8') as f:

            parts = [line.split(':')[2] for line in f]
            parts = set(parts)
            for part in parts:
                self.pndic[part] = []
        with open("jpdb.dic", 'r', encoding='utf-8') as f:

            for line in f:
                line = line.strip('\n')
                line = line.split(':')
                line[3] = float(line[3])
                self.pndic[line[2]].append({'kanji': line[0], 'yomi': line[1], 'point': line[3]})

    def mecab_list(self, s):

        # return list of mecab analysis
        s = self.m.parse(s)

        return [word.split(',') for word in s.replace('\t', ',').split('\n')[:-2]]

    def pn(self, s):
        # return average positive vs negative points of text
        points_of_s = []
        for line in self.mecab_list(s):

            try:

                word = line[7]
                word_part = line[1]
            except IndexError as e:

                # skip symbols like (, ), $, %,
                continue
            if word_part in self.pndic.keys():

                '''if word part is noun, verb, adjective and auxiliary.'''
                for i in self.pndic[word_part]:  # for each word i = dict in pndict=list

                    if word == i['kanji'] or word == i['yomi']:
                        points_of_s.append(i['point'])
                        print(word, word_part, i['point'])

                        break
                else:

                    print('{0} is not in the pn-dictionary.'.format(word))
            else:

                continue

        points_of_s = np.array(points_of_s)
        avg_point = np.mean(points_of_s)
        avg_point = round(int(avg_point), 2)
        print('{0}\npoint = {1}'.format(s, avg_point))
        return avg_point


s = 'つっかかってこなかったので、王子くんは花にいった。'
text_pn = Text_pn()
# print point
print(text_pn.pn(s))
