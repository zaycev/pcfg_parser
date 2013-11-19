#!/usr/bin/env python
# coding: utf-8

import re
import string
import collections

try: import numpy as np
except:
    try: import numpypy as np
    except: import _numpypy as np

class Grammar(object):
    SEP_1 = chr(243)
    SEP_2 = chr(244)
    RE_LINE = re.compile("^(?P<top>.+) \-\> (?P<derivs>.+) \# (?P<prob>.+)$")
    
    def __init__(self):
        self.probs = collections.Counter()
        self.default = 0.0
        self.N = {"TOP"}
        self.w_X_index = None
        self.YZ_X_index = None
        self.SIGMA = set()
        self.R = set()
        self.S = "TOP"

    def is_terminal(self, symbol):
        return symbol in self.SIGMA

    def is_nonterminal(self, symbol):
        return symbol in self.N

    def use_log(self):
        for k, v in self.probs.iteritems():
            self.probs[k] = np.log10(np.float64(v))
        self.default = -np.inf

    def __getitem__(self, top_derivs):
        return self.probs.get(Grammar.key(*top_derivs), self.default)

    def __setitem__(self, top_derivs, value):
        self.probs[Grammar.key(*top_derivs)] = value

    @staticmethod
    def key(top, derivs):
        return Grammar.SEP_1.join([top, Grammar.SEP_2.join(derivs)])

    @staticmethod
    def load(grammar_filepath):
        grammar = Grammar()
        with open(grammar_filepath, "rb") as grammar_fl:
            for line in grammar_fl:
                m = Grammar.RE_LINE.search(line)
                top = m.group("top")
                derivs = m.group("derivs").split(" ")
                prob = float(m.group("prob"))
                grammar[(top, derivs)] = prob
                grammar.R.add(tuple([top] + derivs))
                if len(derivs) == 1:
                    grammar.SIGMA.update(derivs)
                else:
                    grammar.N.update(derivs)
        return grammar
    
    def create_indexes(self):
        self.w_X_index = dict()
        self.YZ_X_index = dict()
        for rule in self.R:
            
            if len(rule) == 3:
                X, Y, Z = rule
                YZ = (Y, Z)
                p = self[(X, [Y, Z])]
                if YZ in self.YZ_X_index:
                    self.YZ_X_index[YZ].append([X, p])
                else:
                    self.YZ_X_index[YZ] = [(X, p)]

            elif len(rule) == 2:
                X, w = rule
                p = self[(X, [w])] 
                if w in self.w_X_index:
                    self.w_X_index[w].append((X, p))
                else:
                    self.w_X_index[w] = [(X, p)]

            else:
                raise Exception("Logic error.")