#!/usr/bin/env python3

from app import *
from struct import * 
from keys_generator import *

if __name__== "__main__":    
    #img = ImageViewer()
    keysGenerator = KeysGenerator()
    #keysGenerator.generateNewKeys()
    val = keysGenerator.encrypt("90")
    print(keysGenerator.decrypt(val))
    (pubKey, privKey) = keysGenerator.getKeysFromFile()