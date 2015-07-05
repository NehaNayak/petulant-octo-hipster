import sys
import nltk
from nltk.corpus import wordnet as wn

topSynset = wn.synset(sys.argv[1])

hypoFunc = lambda s: s.hyponyms()
hyperFunc = lambda s: s.hypernyms()
allHyponyms = set(topSynset.closure(hypoFunc))
allHyponyms.add(topSynset)

outFile = open("pairs_"+topSynset.name(),'w')

for hypo in allHyponyms:
    hypernyms = set(hypo.closure(hyperFunc))

    for otherHypo in allHyponyms:
        if otherHypo != hypo:
            if otherHypo in hypernyms:
                outFile.write(otherHypo.name()+"\t"+hypo.name()+"\t1\n")
            else:
                outFile.write(otherHypo.name()+"\t"+hypo.name()+"\t0\n")

