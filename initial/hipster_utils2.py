from numpy.linalg import inv
from numpy.linalg import det
from numpy import * 

def unpack(vec1, vec2):

    dim = vec1.size/2

    mu1 = vec1[:dim]
    mu2 = vec2[:dim]
    sig1 = diag(vec1[dim:])
    sig2 = diag(vec2[dim:])

    return (mu1, mu2, sig1, sig2)

def pack(mu1, mu2, sig1, sig2):

    vec1 = concatenate((mu1, diag(sig1)))
    vec2 = concatenate((mu2, diag(sig2)))
        
    return (vec1, vec2)

def KLD(vec1, vec2):

    print "in KLD"

    (mu1, mu2, sig1, sig2) = unpack(vec1, vec2)

    #print "vec1", vec1, "vec2", vec2
    #print mu1, mu2
    #print sig1, sig2
    
    traceSigs = trace(inv(sig2).dot(sig1))
    #print "traceSigs", traceSigs
    mus = ((mu2 - mu1).T.dot(inv(sig2))).dot(mu2-mu1)
    #print "mus", mus
    d = mu1.size
    #print "d",d
    logs = log(det(sig2)/det(sig1))
    #print log(det(sig1)), log(det(sig2))
    #print "logs", logs
    
    KLDValue = 0.5*(traceSigs + mus - d + logs)
   
    return KLDValue

def dKLD(vec1, vec2):
    
    (mu1, mu2, sig1, sig2) = unpack(vec1, vec2)
    
    del_12 = inv(sig2).dot(mu2-mu1)

    del_mu1 = -1.0*del_12
    del_mu2 = del_12

    del_sig1 = 0.5*(inv(sig2) - inv(sig1))
    del_sig2 = 0.5*(inv(sig2) - inv(sig2).dot(sig1).dot(inv(sig2)) - del_12.dot(del_12.T))

    (d_vec1, d_vec2) = pack(del_mu1, del_mu2, del_sig1, del_sig2)

    return (d_vec1, d_vec2) 

def KLDnumGrad(vec1, vec2):

    eps = 0.000001

    for i in range(vec1.size):
        p = onehot(i, vec1.size)
        v1 = vec1+eps*p
        f1 = KLD(v1,vec2)
        v2 = vec1-eps*p
        f2 = KLD(v2,vec2)
        num_deriv = (f1-f2)/(2*eps)
        (d_vec1, d_vec2) = dKLD(vec1, vec2)
        if abs(num_deriv-d_vec1[i])<10e-5:
            print "Pass"
        else:
            print i, "Fail" , num_deriv, d_vec1[i]

    for i in range(vec2.size):
       p = onehot(i, vec2.size)
       v1 = vec2+eps*p
       f1 = KLD(vec1,v1)
       v2 = vec2-eps*p
       f2 = KLD(vec1,v2)
       num_deriv = (f1-f2)/(2*eps)
       (d_vec1, d_vec2) = dKLD(vec1, vec2)
       if abs(num_deriv-d_vec2[i])<10e-5:
            print "Pass"
       else:
            print i, "Fail" , num_deriv, d_vec2[i]

def onehot(index, length):
    v = zeros(length)
    v[index]+=1
    return v

def SGD(pairs, Vectors, func, gradfunc, iters=10000, step=0.01):
    for iternum in range(iters):
        print "--", iternum
        for word1, word2, maxMin in pairs:
            vec1 = Vectors[word1]
            vec2 = Vectors[word2]
            (d_vec1, d_vec2) = gradfunc(vec1, vec2)
            if maxMin > 0.0:
                Vectors[word1] -= step*d_vec1
                Vectors[word2] -= step*d_vec2
            """
            else:
                Vectors[word1] -= step*d_vec1
                Vectors[word2] -= step*d_vec2
            """

            print word1, word2, KLD(vec1, vec2)

    #for word1, word2, maxMin in pairs:
    #    print word1, word2, maxMin, func(Vectors[word1], Vectors[word2])
