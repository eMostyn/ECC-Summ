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
        #Add the number to the beginning
        vector.insert(0,num%2)
        #Integer division to remove last digit
        num = num//2
    return vector
        
def repetitionEncoder(m,n):
    vector = []
    #For i in range add the number 0/1
    for i in range(0,n):
        vector.extend(m)
    return vector

def repetitionDecoder(v):
    #Count the amount of 1s and 0s and return the largest of the two or [] if same
    numof1 = v.count(1)
    numof0 = v.count(0)
    if numof1 == numof0:
        return []
    elif numof1 > numof0:
        return [1]
    else:
        return [0]

def message(a):
    msg = []
    l = len(a)
    found = False
    r = 2
    #Find r
    while(found == False):
        num = 2**r - 2*r -1
        if num >= l:
            found = True
        else:
            r += 1
    k = 2**r - r -1
    #Add the l as a binary vector
    msg.extend(decimalToVector(l,r))
    msg.extend(a)
    #Add the 0s to the end
    while(len(msg)< k):
        msg.append(0)
    return msg
         

def hammingEncoder(m):
    #Find r and if the message is suitable
    r = 2
    while (2**r -r - 1 < len(m)):
        r += 1
    if 2**r -r - 1 != len(m):
        return []
    #Create the generator matrix
    genMatrix = hammingGeneratorMatrix(r)
    result = []
    #Multiply the vector to the matrix
    for i in range(0,len(genMatrix[0])):
        num = 0
        for j in range(0,len(m)):
            num = (num + (m[j] * genMatrix[j][i])%2)
        result.append(num)
            
    return result

def hammingDecoder(v):
    #Find r and if the hamming code is suitable
    r = 2
    while (2**r - 1 < len(v)):
        r += 1
    if 2**r - 1 != len(v):
        return []
    #Generator the tranpose matrix of H
    HT = [[0 for x in range(r)] for y in range(2**r-1)]
    for i in range(1,2**r):
        #Add the values which are decimals values 1 => 1-r
        HT[i-1] = decimalToVector(i,r)
    result = []
    #Multiply the vector by the matrix
    for i in range(0,len(HT[0])):
        num = 0
        for j in range(0,len(v)):
            num = (num + (v[j] * HT[j][i])%2)
        result.append(num)
    #Find the decimal value of the result
    num = binaryToDecimal(result)
    #If its 0 then v is a code
    if num == 0:
        return v
    else:
        #Generate e and add it to v
        e = [0 for x in range(len(v)+1)]
        e[num-1] = 1
        for i in range(0,len(v)):
            v[i] = (v[i] + e[i])%2
    return v
def binaryToDecimal(v):
    #Function that converts binary to decimal
    total = 0
    for i in range(1,len(v)+1):
        num = v[-1]
        total += num * 2**(i-1)
        if len(v) >1:
            v = v[:-1]
    return total
def messageFromCodeword(c):
    cWord = c.copy()
    #Find r and see if codeword is suitable
    r = 2
    while (2**r - 1 < len(cWord)):
        r += 1
    if 2**r - 1 != len(cWord):
        return []
    i = 2**(r-1)
    #Delete the values at powers 2 indexes starting from the largest
    while i >=1:
        del cWord[i-1]
        i = i//2
    return cWord

def dataFromMessage(m):
    #Find r and if the message is suitable
    r = 2
    while (2**r - r- 1 < len(m)):
        r += 1
    if 2**r - r- 1 != len(m):
        return []
    #Find the value of r, which is the first r values of the message
    lBin = m[:r]
    l = binaryToDecimal(lBin)
    #If l is greater than the remaining space then its invalid return []
    if(l > len(m)-r):
        return []
    #Find and return data
    data = m[r:l+r+1]
    return data
    
    
