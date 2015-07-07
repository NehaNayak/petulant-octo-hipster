import sys
import nltk
from nltk.corpus import wordnet as wn
import pickle

Tree = {}

for syn in list(wn.all_synsets()):
    if len(syn.hyponyms())>0 or len(syn.hypernyms())<0:
        Tree[syn.name()]=map(lambda x:x.name(),syn.hyponyms())

words = list(set(Tree.keys()).union(set([word for hypos in Tree.values() for word in hypos])))

lemmas = set()

for word in list(words):
    lemma, pos, synset_index_str = word.lower().rsplit('.', 2)
    lemmas.add(lemma)

for lemma in lemmas:
    print lemma
