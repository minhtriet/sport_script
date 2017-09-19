import os
import pdb
import sys

for sub_r, sub_s, sub_files in os.walk(sys.argv[1]):
    for folder in sub_s:
        for aVid in os.listdir(sub_r+folder):
            if aVid.startswith('flow'):
                print aVid
                os.remove(sub_r+folder+'/'+aVid)
