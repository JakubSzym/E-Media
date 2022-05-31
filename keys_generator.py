from matplotlib.pyplot import get
from numpy import mod, power
import rsa
import random
import sympy

M = 256

def gcd(p, q):
    while q != 0:
        p, q = q, p % q
    return p

def isCoprime(x, y):
    return gcd(x, y) == 1

def generateLargePrime(bits):
    while True:
        number = random.randrange(2**(bits-1), 2**(bits))
        if sympy.isprime(number):
            return number

class KeysGenerator():
    def generateNewKeys(self):
        p = generateLargePrime(M)
        q = generateLargePrime(M)
        N = p * q
        T = (p - 1) * (q - 1)
        while True:
            possibleE = generateLargePrime(M)
            if (isCoprime(possibleE, T) and possibleE < T):
                break
        e = possibleE
        d = pow(e, -1, T)
        self.pubKey = (e, N)
        self.privKey = (d, N)
        self.saveKeysInFile()

    def saveKeysInFile(self):
        with open("keys/public_key.dat", "w") as f:
            f.write(str(self.pubKey[0]))
            f.write(",")
            f.write(str(self.pubKey[1]))

        with open("keys/private_key.dat", "w") as f:
            f.write(str(self.privKey[0]))
            f.write(",")
            f.write(str(self.privKey[1]))

    def getKeysFromFile(self):
        with open("keys/public_key.dat", "r") as f:
            self.pubKey = tuple(map(int, f.readline().split(',')))
        with open("keys/private_key.dat", "r") as f:
            self.privKey = tuple(map(int, f.readline().split(',')))
        return (self.pubKey, self.privKey)

    def encrypt(self, hex):
        self.getKeysFromFile()
        dec = int(hex, 16)
        encryptedValue = pow(dec, self.pubKey[0], self.pubKey[1]) 
        return encryptedValue
    
    def decrypt(self, encryptedValue):
        self.getKeysFromFile()
        decryptedValue = pow(encryptedValue, self.privKey[0], self.privKey[1])
        return decryptedValue