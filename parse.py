#!/usr/bin/env python
# coding: utf-8

import sys
import time
import parser
import grammar


try:
    _, grammar_filepath = sys.argv
except:
    sys.stderr("Error")
    exit(1)


g = grammar.Grammar.load(grammar_filepath)
g.use_log()

p = parser.Parser(g)


# print g[("WDT", ["what"])]
# print g.N
# print g.SIGMA
# print g.R
# print g.S

def print_subtree(subtree):
    if len(subtree) == 2:
        root, leaf = subtree
        return "(%s %s)" % (root, leaf)
    else:
        root, children = subtree[0], subtree[1:]
        return "(%s %s)" % (root, " ".join([print_subtree(child) for child in children]))

# data = []
for line in sys.stdin:
    
    # for i in xrange(10):
    #     time1 = time.time()
    words, prob, tree = p.parse(line)
        # time2 = time.time()
        # delta = time2 - time1
        # data.append((len(words), delta))
    
    print print_subtree(tree)


# import pickle
# 
# pickle.dump(data, open("data.pkl", "wb"))
