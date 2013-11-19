#!/usr/bin/env python

import sys, fileinput
import tree

def annotate_tree(subtree, prev):
    
    if len(subtree.children) != 0:
        if prev is not None:
            label = "%s@%s" % (subtree.label, prev)
        else:
            label = subtree.label
        if len(subtree.children) == 1:
            ch = subtree.children[0]
            return "(%s %s)" % (label, " ".join([annotate_tree(ch, None)]))
        if len(subtree.children) == 2:
            ch1, ch2 = subtree.children
            return "(%s %s)" % (label, " ".join([annotate_tree(ch1, None),  annotate_tree(ch2, ch1.label)]))
        else:
            raise Exception("Error")
    else:
        s = '%s' % subtree.label
        #s = s.replace("(", "-LRB-")
        #s = s.replace(")", "-RRB-")
        return s

for line in fileinput.input():
    t = tree.Tree.from_str(line)

    assert t.root.label == 'TOP'

    print annotate_tree(t.root, None)
    
    
