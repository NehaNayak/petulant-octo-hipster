import sys
from numpy import * 
from hipster_utils2 import *

def main():    
    dim = 2

    words = set() 
    Vectors = {}
    pairs = list()
    
    for line in sys.stdin:
        (wordP, wordQ, label) = line.split()
        if label=='1':
            pairs.append((wordP, wordQ, -1.0))
        else:
            pairs.append((wordP, wordQ, 1.0))

        words.add(wordP)
        words.add(wordQ)
   
    for word in words:
        muWord = random.rand(dim)
        sigWord = absolute(random.rand(dim))
        print sigWord
        Vectors[word] = concatenate((muWord, sigWord))
    
    KLDnumGrad(Vectors.values()[0], Vectors.values()[1])
        
    #SGD(pairs, Vectors, KLD, dKLD, 500, 0.00001)

if __name__=="__main__":
    main()
