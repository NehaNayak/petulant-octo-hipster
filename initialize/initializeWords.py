import sys
from numpy import *
from scipy import *
from scipy.stats import multivariate_normal

dim = 50

roots = ['entity.n.01','thing.n.01']

Distributions = {}

for root in roots:
    fitsIn = False
    while fitsIn is False:
        mu = random.rand(dim)
        print mu
        mu = mu/linalg.norm(mu)
        sigma = abs(random.rand())
        print sigma
        fitsIn = True
        for root, dist in Distributions.iteritems():
            multpdf=multivariate_normal.pdf(mu, dist[0], dist[1]*eye(dim))
            print multpdf
            if multpdf > 10e-10:
                fitsIn = False
                break
        
    Distributions[root] = (mu, sigma)    

print Distributions
