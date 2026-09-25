import struct
import unittest

from tools.stoneage_stoneage5_cab_probe import (
    dos_datetime,
    parse_cab_files,
    parse_cab_folders,
    parse_cab_header,
)


def synthetic_cab():
    name=b"battle_2.bin\x00"
    folder_off=36
    file_off=44
    data_off=file_off+16+len(name)
    b=bytearray(data_off+8)
    b[:4]=b"MSCF"
    struct.pack_into("<I",b,8,len(b))
    struct.pack_into("<I",b,16,file_off)
    b[24]=3
    b[25]=1
    struct.pack_into("<HHHHH",b,26,1,1,0,7,0)
    struct.pack_into("<IHH",b,folder_off,data_off,1,1)
    date=((2002-1980)<<9)|(12<<5)|27
    time=(2<<11)|(21<<5)|(8//2)
    struct.pack_into("<IIHHHH",b,file_off,187500,1234,0,date,time,0x20)
    b[file_off+16:file_off+16+len(name)]=name
    struct.pack_into("<IHH",b,data_off,0x12345678,100,200)
    return bytes(b)


class Stoneage5CabProbeTests(unittest.TestCase):
    def test_parse_header_folder_file(self):
        b=synthetic_cab()
        h=parse_cab_header(b)
        self.assertEqual(h["c_folders"],1)
        self.assertEqual(h["c_files"],1)
        folders=parse_cab_folders(b,h)
        self.assertEqual(folders[0]["compress_name"],"MSZIP")
        files,end=parse_cab_files(b,h)
        self.assertEqual(files[0]["name"],"battle_2.bin")
        self.assertEqual(files[0]["size"],187500)
        self.assertGreater(end,h["coff_files"])

    def test_dos_timestamp(self):
        date=((2002-1980)<<9)|(12<<5)|27
        time=(2<<11)|(21<<5)|(8//2)
        self.assertEqual(dos_datetime(date,time),"2002-12-27T02:21:08")


if __name__=="__main__":
    unittest.main()
