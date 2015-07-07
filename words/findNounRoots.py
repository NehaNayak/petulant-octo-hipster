import sys
import pickle
from math import sqrt

Tree = pickle.load(open(sys.argv[1],'r'))
AccCounts = pickle.load(open(sys.argv[2],'r'))

allHypos = set([hypo for hypos in Tree.values() for hypo in hypos])
allHypers = set(Tree.keys())
nounRoots = [ (word, sqrt(float(AccCounts[word])/AccCounts['entity.n.01'])) for word in list(allHypers - allHypos) if '.n.' in word]

for nounSynset, weight in nounRoots:
    print nounSynset+"\t"+str(weight)
