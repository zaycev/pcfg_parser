#!/usr/bin/env python

import sys, fileinput
import tree

def deannotate_tree(subtree):
    
    if len(subtree.children) != 0:
        if "@" in subtree.label:
            label,_ = subtree.label.split("@")
        else:
            label = subtree.label
        return "(%s %s)" % (label, " ".join(deannotate_tree(child) for child in subtree.children))
    else:
        s = '%s' % subtree.label
        #s = s.replace("(", "-LRB-")
        #s = s.replace(")", "-RRB-")
        return s

for line in fileinput.input():
    t = tree.Tree.from_str(line)

    assert t.root.label == 'TOP'

    print deannotate_tree(t.root)
    
    
