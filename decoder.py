from struct import unpack, pack
import math

PngSignature = b'\x89PNG\r\n\x1a\n'

def append_hex(a, b):
    sizeof_b = 0
    while((b >> sizeof_b) > 0):
        sizeof_b += 1
    sizeof_b_hex = math.ceil(sizeof_b/4) * 4
    return (a << sizeof_b_hex) | b

class Decoder:
    def __init__(self, file):
        self.image_data = []
        self.critical_chunks = []
        self.f = open(file, 'rb')
        if self.f.read(len(PngSignature)) != PngSignature:
            raise Exception('Invalid PNG Signature')
    def decode(self):
        while(True):
            #Długość kawałka - 4 bajty
            chunk_length,  = unpack('>I', self.f.read(4))
            #typ kawałka - 4 bajty
            chunk_type, = unpack('4s', self.f.read(4))
            #Dane kawałka - długość kawałka w bajtach
            chunk_data = self.f.read(chunk_length)
            chunk_crc = unpack('4s', self.f.read(4)) 
            self.image_data.append((chunk_type,chunk_data))
            if(chunk_type == b'IHDR' or chunk_type == b'IEND' or chunk_type == b'IDAT' or chunk_type == b'PLTE'):
                self.critical_chunks.append((chunk_type,chunk_data))
            if(chunk_type == b'IEND'):
                break
    def header_info(self):
        width = 0
        height = 0
        for i in range(4):
            width = append_hex(width,self.critical_chunks[0][1][i])
        for i in range(4,8):
            height = append_hex(height,self.critical_chunks[0][1][i])
        bit_depth = self.critical_chunks[0][1][8]
        color_type = self.critical_chunks[0][1][9]
        compr_type = self.critical_chunks[0][1][10]
        filter_type = self.critical_chunks[0][1][11]
        interl_type = self.critical_chunks[0][1][12]
        print(f"Width: {width} \nHeight: {height}\nBit depth: {bit_depth}\nColor type: {color_type}")
        print(f"Compr type: {compr_type}\nFilter type: {filter_type}\nInterl type: {interl_type}")