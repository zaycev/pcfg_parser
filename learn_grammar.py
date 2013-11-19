#!/usr/bin/env python
# coding: utf-8

import sys
import tree
import collections

grammar = collections.Counter()

def update_grammar(subtree, grammar):
    if len(subtree.children) == 0: return
    if len(subtree.children) == 1: children = [ch.label.lower() for ch in subtree.children]
    else: children = [ch.label for ch in subtree.children]
    grammar["%s\t%s" % (subtree.label, " ".join(children))] += 1
    for ch in subtree.children:
        update_grammar(ch, grammar)

for line in sys.stdin:
    update_grammar(tree.Tree.from_str(line).root, grammar)


total_freqs = collections.Counter()
for s,freq in grammar.iteritems():
    top = s.split("\t")[0]
    total_freqs[top] += freq + 1

for subst, freq in grammar.most_common():
    top, children = subst.split("\t")
    print "%s -> %s # %.16f" % (top, children, float(freq + 1) / float(total_freqs[top]))