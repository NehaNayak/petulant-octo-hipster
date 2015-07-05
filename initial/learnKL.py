import sys
from numpy import * 
from numpy.linalg import inv
from numpy.linalg import det

def unpack(vecP, vecQ):

    dim = vecP.size/2

    muP = vecP[:dim]
    muQ = vecQ[:dim]
    sigP = diag(vecP[dim:])
    sigQ = diag(vecQ[dim:])

    return (muP, muQ, sigP, sigQ)

def pack(muP, muQ, sigP, sigQ):

    vecP = concatenate((muP, diag(sigP)))
    vecQ = concatenate((muQ, diag(sigQ)))
        
    return (vecP, vecQ)

def KLD(vecj, veci):

    (muj, mui, sigj, sigi) = unpack(vecj, veci)
    
    traceSigs = trace(inv(sigi).dot(sigj))
    mus = ((mui - muj).T.dot(inv(sigi))).dot(mui-muj)
    d = mui.size
    logs = log(det(sigj)/det(sigi))
    
    KLDValue = 0.5*(traceSigs + mus - d - logs)
   
    return KLDValue

def dKLD(veci, vecj):
    
    (muj, mui, sigj, sigi) = unpack(vecj, veci)
    
    del_i_j = inv(sigi).dot(mui-muj)

    del_mui = -1.0*del_i_j
    del_muj = del_i_j

    del_sigi = 0.5*(inv(sigi).dot(sigj).dot(inv(sigi))+del_i_j.dot(del_i_j.T) -inv(sigi))
    del_sigj = 0.5*(inv(sigj) - inv(sigi))

    print del_mui
    print del_muj
    print del_sigi
    print del_sigj

def main():    
    dim = 5
   
    words = set() 
    Vectors = {}
    pairsMinimize = list()
    pairsMaximize = list()
    
    for line in sys.stdin:
        (wordP, wordQ, label) = line.split()
        if label=='1':
            pairsMinimize.append((wordP, wordQ))
        else:
            pairsMaximize.append((wordP, wordQ))

        words.add(wordP)
        words.add(wordQ)
    
    for word in words:
        muWord = random.rand(dim)
        sigWord = absolute(random.rand(dim))
        Vectors[word] = concatenate((muWord, sigWord))
        
    for pair in pairsMinimize:
        (wordP, wordQ) = pair
        print KLD(Vectors[wordP], Vectors[wordQ])
        dKLD(Vectors[wordP], Vectors[wordQ])

if __name__=="__main__":
    main()
