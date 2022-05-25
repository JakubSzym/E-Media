from matplotlib.pyplot import get
from numpy import mod, power
import rsa
import random

def gcd(p, q):
    while q != 0:
        p, q = q, p % q
    return p

def isCoprime(x, y):
    return gcd(x, y) == 1

def isPrime(n):
    if n == 2 or n == 3:
        return True
    if n % 2 == 0 or n < 2:
        return False
    for i in range(3, int(n ** 0.5) + 1, 2):
        if n%i==0:
            return False    
    return True


class KeysGenerator():
    def generateNewKeys(self):
        primes = [i for i in range(10, 100) if isPrime(i)]
        p = random.choice(primes)
        q = random.choice(primes)
        N = p * q
        T = (p - 1) * (q - 1)
        possibleE = [i for i in range(3, T) if (isCoprime(i, T))]
        e = random.choice(possibleE)
        possibleD = [i for i in range(3, T) if ((e * i) % T == 1 and isCoprime(i, N))]
        d = random.choice(possibleD)
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
        encryptedValue = mod(dec ** self.pubKey[0], self.pubKey[1])
        return encryptedValue
    
    def decrypt(self, encryptedValue):
        self.getKeysFromFile()
        decryptedValue = mod(encryptedValue ** self.privKey[0], self.privKey[1])
        return decryptedValue