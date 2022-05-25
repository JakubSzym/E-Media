from struct import unpack
import math

png_signature = b'\x89PNG\r\n\x1a\n'
critical_chunks = ('IHDR', 'IEND', 'IDAT', 'PLTE')
ancillary_chunks = ('cHRM', 'gAMA', 'sBIT', 'sBIT', 'bKGD', 'hIST', 'tRNS', 'pHYs', 'tIME', 'tEXT', 'zTXt')

def append_hex(a, b):
    sizeof_b = 0
    while((b >> sizeof_b) > 0):
        sizeof_b += 1
    sizeof_b_hex = math.ceil(sizeof_b/4) * 4
    return (a << sizeof_b_hex) | b


class ChunkReader:
    def __init__(self, file):
        self.normal_image_bytes = 8
        self.reduced_image_bytes = 8
        self.normal_image_data = []
        self.reduced_image_data = []
        self.critical_chunks = []
        self.critical_chunks_names = []
        self.ancillary_chunks = []
        self.ancillary_chunks_names = []
        self.f = open(file, 'rb')
        if self.f.read(len(png_signature)) != png_signature:
            raise Exception('Invalid PNG Signature')

    def decode(self):
        while(True):
            chunk_length,  = unpack('>I', self.f.read(4))
            chunk_type, = unpack('4s', self.f.read(4))
            chunk_data = self.f.read(chunk_length)
            chunk_crc = unpack('4s', self.f.read(4)) 
            self.normal_image_data.append((chunk_type, chunk_data))
            self.normal_image_bytes += 12 + chunk_length
            
            if str(chunk_type)[2:-1] in critical_chunks:
                self.reduced_image_data.append((chunk_type, chunk_length, chunk_data, chunk_crc))
                self.critical_chunks.append((chunk_type, chunk_data))
                self.critical_chunks_names.append(chunk_type)

                self.reduced_image_bytes += 12 + chunk_length
            elif str(chunk_type)[2:-1] in ancillary_chunks:
                self.ancillary_chunks.append((chunk_type, chunk_data))
                self.ancillary_chunks_names.append(chunk_type)
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
        return width, height, bit_depth, color_type, compr_type, filter_type, interl_type, self.normal_image_bytes, self.reduced_image_bytes, self.critical_chunks_names, self.ancillary_chunks_names

    def make_reduced_image(self, filename):
        path = filename.split('/')
        reducedImgName = "reduced_" + path[len(path) - 1]
        f = open(reducedImgName,"wb")
        f.write(png_signature)
        for type, length, data, crc in self.reduced_image_data:
            bites = length.to_bytes(4, byteorder='big')
            f.write(bites)
            f.write(type)
            f.write(data)
            f.write(crc[0])
        f.close()
