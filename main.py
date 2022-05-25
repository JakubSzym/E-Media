#!/usr/bin/env python3

from app import *
from struct import * 
from keys_generator import *

if __name__== "__main__":    
    generator = KeysGenerator()
    #generator.generateNewKeys()
    encryptionValue = generator.encrypt('50')
    print(generator.decrypt(encryptionValue))
