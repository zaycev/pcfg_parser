#!/usr/bin/env python
# coding: utf-8

import re
import collections

try: import numpy as np
except:
    try: import numpypy as np
    except: import _numpypy as np


class Dict3D():
    
    def __init__(self, default=-np.inf):
        self.default = default
        self.sep = " "
        self.dict = dict()
    
    def __getitem__(self, ijX):
        i, j, X = ijX
        key = self.sep.join([str(i), str(j), str(X)])
        return self.dict.get(key, self.default)
    
    def __setitem__(self, ijX, value):
        i, j, X = ijX
        key = self.sep.join([str(i), str(j), str(X)])
        self.dict[key] = value

    def __iter__(self):
        for k, v in self.dict.iteritems():
            i, j, X = k.split(self.sep)
            yield (int(i), int(j), X), v
            

class Parser(object):

    def __init__(self, grammar):
        self.g = grammar
        self.g.create_indexes()
        self.words = None

    @staticmethod
    def __range(a, b):
        return xrange(a, b + 1)
    
    def __iword(self, i):
        return self.words[i - 1]

    def parse(self, string):
        
        if string[-1] == "\n":
            string = string[:(len(string) - 1)]

        words = string.split(" ")
        
        self.words = [w.lower() for w in words]
        self.words = [w if w in self.g.SIGMA else "<unk>" for w in self.words]
        
        best = Dict3D(default=-np.inf)
        back = Dict3D(default=None)
        n = len(self.words)
        flat = [self.g.S]

        for i in self.__range(1, n):
            w = self.__iword(i)
            for X, p in self.g.w_X_index[w]:
                if p > best[i - 1, i, X]:
                    best[i - 1, i, X] = p
                    back[i - 1, i, X] = (X, words[i - 1])
            flat.append(back[i - 1, i, X])

        for l in self.__range(2, n):
            for i in self.__range(0, n - l):
                j = i + l
                for k in self.__range(i + 1, j - 1):
                    for YZ, Xps in self.g.YZ_X_index.iteritems():
                        Y, Z = YZ                        
                        for X, p in Xps:
                            p_ = p + best[i, k, Y] + best[k, j, Z]
                            if p_ > best[i, j, X]:
                                best[i, j, X] = p_
                                back[i, j, X] = (X, Y, Z, i, j, k)

        G = []
        best_p = -np.inf
        for (i, j, X), XYZ in back:
            if i < j:
                G.append(XYZ)
                p = best[i, j, X]
        
        tree = self.extract(self.g.S, 0, n, G, back)
        prob = best[0, n, self.g.S]
        
        if tree is None:
            tree = flat

        return self.words, prob, tree

    def extract(self, X, i, j, G, back):
        XYZijk = back[i, j, X]
        if XYZijk is None:
            return None
        if len(XYZijk) == 6:
            X, Y, Z, i, j, k = XYZijk
            return (X,
                   self.extract(Y, i, k, G, back),
                   self.extract(Z, k, j, G, back))
        X, w = XYZijk
        return (X, w)
        



                    