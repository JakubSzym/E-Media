from struct import unpack, pack
import zlib

PngSignature = b'\x89PNG\r\n\x1a\n'


class Decoder:
    def __init__(self, file):
        self.file = file
        self.image_data = []
        self.ptr = 0
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
            if(chunk_type == b'IEND'):
                break
        