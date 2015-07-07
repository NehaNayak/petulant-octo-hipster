import sys
import nltk
from nltk.corpus import wordnet as wn
import pickle

Tree = {}

for syn in list(wn.all_synsets()):
    if len(syn.hyponyms())>0 or len(syn.hypernyms())<0:
        Tree[syn.name()]=map(lambda x:x.name(),syn.hyponyms())

pickle.dump(Tree, sys.stdout)
