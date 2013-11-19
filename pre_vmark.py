#!/usr/bin/env python

import sys, fileinput
import tree

def annotate_tree(subtree):
    
    if len(subtree.children) != 0:
        if subtree.parent is not None:
            label = "%s&%s" % (subtree.label, subtree.parent.label)
        else:
            label = subtree.label
        return "(%s %s)" % (label, " ".join(annotate_tree(child) for child in subtree.children))
    else:
        s = '%s' % subtree.label
        #s = s.replace("(", "-LRB-")
        #s = s.replace(")", "-RRB-")
        return s

for line in fileinput.input():
    t = tree.Tree.from_str(line)

    assert t.root.label == 'TOP'

    print annotate_tree(t.root)
    
    
