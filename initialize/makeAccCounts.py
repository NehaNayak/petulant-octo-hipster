import nltk
from nltk.corpus import wordnet as wn
import sys
from collections import defaultdict
import pickle
from math import log

Hyponyms = defaultdict(list)

def BFS(word,path):
    hypos = Hyponyms[word]
    if len(hypos) == 0:
        lemma, pos, synset_index_str = word.lower().rsplit('.', 2)
        AccCounts[word]=Counts[lemma]
    else:
        lemma, pos, synset_index_str = word.lower().rsplit('.', 2)
        AccCounts[word]=Counts[lemma]
        for hypo in Hyponyms[word]:
            if hypo not in path:
                if hypo not in AccCounts.keys():
                    BFS(hypo,path+[hypo])
                AccCounts[word]+=AccCounts[hypo] 
Counts = {}
AccCounts = {}

for line in open(sys.argv[1]):
    (word, count) = line.split()
    Counts[word]=int(count)

Hypos = set()
Hypers = set()

for line in sys.stdin:
    (hyper, hypo) = line.split()
    Hyponyms[hyper].append(hypo)
    Hypers.add(hyper)
    Hypos.add(hypo)

for start in Hypers-Hypos:
    BFS(start,[start])

pickle.dump(AccCounts, sys.stdout)
