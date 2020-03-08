def hammingGeneratorMatrix(r):
    n = 2**r-1
    
    #construct permutation pi
    pi = []
    for i in range(r):
        pi.append(2**(r-i-1))
    for j in range(1,r):
        for k in range(2**j+1,2**(j+1)):
            pi.append(k)

    #construct rho = pi^(-1)
    rho = []
    for i in range(n):
        rho.append(pi.index(i+1))

    #construct H'
    H = []
    for i in range(r,n):
        H.append(decimalToVector(pi[i],r))

    #construct G'
    GG = [list(i) for i in zip(*H)]
    for i in range(n-r):
        GG.append(decimalToVector(2**(n-r-i-1),n-r))

    #apply rho to get Gtranpose
    G = []
    for i in range(n):
        G.append(GG[rho[i]])

    #transpose    
    G = [list(i) for i in zip(*G)]

    return G

def decimalToVector(i,l):
    num = i
    vector = []
    for k in range(0,l):
        vector.insert(0,num%2)
        num = num//2
    return vector
        
def repetitionEncoder(m,n):
    vector = []
    for i in range(0,n):
        vector.extend(m)
    return vector

def repetitionDecoder(v):
    numof1 = v.count(1)
    numof0 = v.count(0)
    if numof1 == numof0:
        return []
    elif numof1 > numof0:
        return [1]
    else:
        return [0]
