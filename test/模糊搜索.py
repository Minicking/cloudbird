import struct
packBody=None
packLength=struct.pack('I',len(packBody)) if packBody else struct.pack('I',0)
print(packLength)
