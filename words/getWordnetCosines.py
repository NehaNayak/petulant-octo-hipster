import sys
import numpy as np

Vectors = {}
wordnetFile = open(sys.argv[1],'r')
wordnetLemmas = []

for line in wordnetFile:
    word = line.split()[0]
    wordnetLemmas.append(word)

print wordnetLemmas    

for line in sys.stdin:
    thisLine = line.split()
    vec = np.array(map(lambda x:float(x),thisLine[1:]))
    vec/=np.linalg.norm(vec)
    Vectors[thisLine[0]] = vec

p = np.matrix(Vectors.values())
words = Vectors.keys()

for j in words:
    x= np.array(p.dot(Vectors[j]).reshape(400000,))
    idx = x.argsort()
    for i in idx[0][-21:][::-1]:
        print j+"\t0\t"+words[i]+"\t0\t"+"{0:0.8f}".format(1-x[0][i])


