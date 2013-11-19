echo "Fitting PCFG."
cat < train.trees \
| pypy preprocess.py\
| pypy unknown.py \
| pypy learn_grammar.py > grammar.txt

echo "Parsing test.strings."
pypy parse.py grammar.txt < dev.strings > dev.parses

echo "Postprocessing results."
cat < dev.parses \
| pypy postprocess.py > dev.parses.post

echo "Running evaluation script."
pypy evalb.py dev.parses.post dev.trees


echo "Fitting PCFG."
cat train.trees > dev.train.trees
cat < dev.train.trees \
| pypy preprocess.py\
| pypy unknown.py \
| pypy learn_grammar.py > grammar.txt

echo "Parsing test.strings."
pypy parse.py grammar.txt < test.strings > test.parses

echo "Postprocessing results."
cat < test.parses \
| pypy postprocess.py > test.parses.post

echo "Running evaluation script."
pypy evalb.py test.parses.post test.trees


echo "Fitting PCFG."
cat train.trees dev.trees > dev.train.trees
cat < dev.train.trees \
| pypy preprocess.py\
| pypy unknown.py \
| pypy learn_grammar.py > grammar.txt

echo "Parsing test.strings."
pypy parse.py grammar.txt < test.strings > test.parses

echo "Postprocessing results."
cat < test.parses \
| pypy postprocess.py > test.parses.post

echo "Running evaluation script."
pypy evalb.py test.parses.post test.trees





