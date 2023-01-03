import os

newpath = r'C:\Users\Admin\Desktop'

name_list = ["The.War.with.Grandpa.2020.480p.BluRay.x264.400MB-Pahe.in", "Bill.Ted.Face.the.Music.2020.720p.WEB-HD.x265.10Bit-Pahe.in", "Unknown.Origins.2020.1080p.WEBRip.x264.AAC5.1-[YTS.MX]",
             "Brahms.The.Boy.II.2020.1080p.BluRay.x264.AAC5.1-[YTS.MX]", "ABCD - American Born Confused Desi [2013] 480p BSub Syncable 450MB AA"]

name_file = open("other/New_Movies.txt", "r")


def from_file(newpath, name_file):
    name_list = []
    for i in name_file:
        name_list.append(i.strip())
    for i in name_list:
        if not os.path.exists(newpath + "\\" + i):
            os.makedirs(newpath + "\\" + i)


def from_list(newpath, name_list):
    for i in name_list:
        if not os.path.exists(newpath + "\\" + i):
            os.makedirs(newpath + "\\" + i)


from_list(newpath, name_list)
from_file(newpath, name_list)
