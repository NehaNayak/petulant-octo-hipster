from numpy.linalg import inv
from numpy.linalg import det
from numpy import * 

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

def dKLD(vecj, veci):
    
    (muj, mui, sigj, sigi) = unpack(vecj, veci)
    
    del_i_j = inv(sigi).dot(mui-muj)

    del_mui = del_i_j
    del_muj = -1.0*del_i_j

    del_sigi = -0.5*(inv(sigi).dot(sigj).dot(inv(sigi)) + del_i_j.dot(del_i_j.T) - inv(sigi))
    del_sigj = 0.5*(inv(sigi) - inv(sigj))

    (d_vecj, d_veci) = pack(del_muj, del_mui, del_sigj, del_sigi)

    return (d_vecj, d_veci) 

def KLDnumGrad(vecj, veci):
    eps = 0.00000001
    for i in range(vecj.size):
        p = onehot(i, vecj.size)
        v1 = vecj+eps*p
        f1 = KLD(v1,veci)
        v2 = vecj-eps*p
        f2 = KLD(v2,veci)
        num_deriv = (f1-f2)/(2*eps)
        (d_vecj, d_veci) = dKLD(vecj, veci)
        if abs(num_deriv-d_vecj[i])<10e-5:
            print "Pass"
        else:
            print i, "Fail"

    for i in range(veci.size):
       p = onehot(i, veci.size)
       v1 = veci+eps*p
       f1 = KLD(vecj,v1)
       v2 = veci-eps*p
       f2 = KLD(vecj,v2)
       num_deriv = (f1-f2)/(2*eps)
       (d_vecj, d_veci) = dKLD(vecj, veci)
       if abs(num_deriv-d_veci[i])<10e-5:
            print "Pass"
       else:
            print i, "Fail" , num_deriv, d_veci[i]

def onehot(index, length):
    v = zeros(length)
    v[index]+=1
    return v

def SGD(pairs, Vectors, func, gradfunc, iters=10000, step=0.01):
    for iternum in range(iters):
        print "--", iternum
        for wordP, wordQ, maxMin in pairs:
            vecj = Vectors[wordQ]
            veci = Vectors[wordP]
            (d_vecj, d_veci) = gradfunc(vecj, veci)
            if maxMin > 0.0:
                Vectors[wordQ] -= step*d_vecj
                Vectors[wordP] -= step*d_veci
            else:
                Vectors[wordQ] += step*d_vecj
                Vectors[wordP] += step*d_veci

            #print veci, vecj
            print wordP, wordQ, maxMin, KLD(vecj, veci)

    for wordP, wordQ, maxMin in pairs:
        print wordP, wordQ, maxMin, func(Vectors[wordQ], Vectors[wordP])
