#!/usr/bin/env python3
import struct, sys
 
xor42 = lambda b: bytes(x ^ 0x42 for x in b)
 
data = open("secret_archive.zip.crdownload", "rb").read()
 
# CRDL header - url at 0x12, encoded payload at 0x40 (after null padding)
# decodes to XORHINT:/\x00<flag>
url_len = struct.unpack_from("<H", data, 0x10)[0]
raw = data[0x40 : data.index(b"\x00\x00", 0x40)]
flag = xor42(raw).split(b"\x00")[1].decode()
print(f"header: {flag}")
 
# same flag is also in hidden/.flagdata inside the embedded zip
zdata = data[data.find(b"PK\x03\x04"):]
idx = 0
while True:
    pos = zdata.find(b"PK\x03\x04", idx)
    if pos == -1:
        break
    fn_len  = struct.unpack_from("<H", zdata, pos+26)[0]
    ex_len  = struct.unpack_from("<H", zdata, pos+28)[0]
    comp_sz = struct.unpack_from("<I", zdata, pos+18)[0]
    fn      = zdata[pos+30 : pos+30+fn_len]
    if fn == b"hidden/.flagdata":
        raw = zdata[pos+30+fn_len+ex_len : pos+30+fn_len+ex_len+comp_sz]
        print(f"zip:    {xor42(raw).decode()}")
        break
    idx = pos + 1
 