import sys
from numpy import * 
from hipster_utils import *

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
        Vectors[word] = concatenate((muWord, sigWord))
        
    SGD(pairs, Vectors, KLD, dKLD, 100, 0.001)

if __name__=="__main__":
    main()
