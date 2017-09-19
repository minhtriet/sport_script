# walk through all file

import os
import json
import re
import random
import sys
import pdb

""" 
    load all frames and write to file
"""


def create_split_file(input_path, output_path):
    with open(input_path) as fi:
        with open(output_path, 'w') as fo:
            for line in fi:
                item = line.split(' ')
                print item
                file_number = len(os.listdir(item[0])) / 3 # rgb, flow_x, flow_y
                for i in range(file_number):
                    fo.write("%s %d %s \n" % (item[0], i + 1, item[1]))  # frame starts from 1

if __name__ == '__main__':
    if len(sys.argv) == 1:
        path = ''
    else:
        path = sys.argv[1]

    create_split_file(os.path.join(path, 'trainlist01.txt'), 'train.txt')
    
    create_split_file(os.path.join(path, 'testlist01.txt'), 'test.txt')
