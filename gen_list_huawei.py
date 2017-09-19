# walk through all file

import os
import json
import re
import random
import sys
import pdb

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'gen_list_huawei <fb/bb>'
        sys.exit(-1)
        
    path = '/media/data/mtriet/dataset/'

    with open('classes_%s.json' % sys.argv[1], 'r') as f:
        classes = json.load(f)

    d = dict.fromkeys(classes)
    for x in d:
        d[x] = []

    src_folder = '%s_flow' % sys.argv[1]
    test_file = "test_%s.txt" % sys.argv[1]
    train_file = "train_%s.txt" % sys.argv[1]
    val_file = "val_%s.txt" % sys.argv[1]

    sub_path = os.path.join(path, src_folder)
    for sub_r, sub_s, sub_files in os.walk(sub_path):
        for aVid in sub_s:
            class_name = re.split('_', aVid)[-1]
            d[class_name].append(os.path.join(sub_r, aVid))

    for x in d:
       random.shuffle(d[x])

    with open(test_file, 'w') as f:
        for x in d:
            for video in d[x][: len(d[x]) / 3]:
                # divide b.c flow_x, img, flow_y
#                f.write("%s %s %s \n" % (video, len(os.listdir(video)) / 3, classes[x]))
                f.write("%s %s \n" % (video, classes[x]))
    with open(train_file, 'w') as f:
        for x in d:
            for video in d[x][len(d[x]) / 3 : ]:
                f.write("%s %s %s \n" % (video, len(os.listdir(video)) / 3, classes[x]))

#    with open(val_file, 'w') as f:
#        for x in d:
#            for video in d[x][int(len(d[x]) * 0.95) : ]:
#                f.write("%s %s %s \n" % (video, len(os.listdir(video)) / 3, classes[x]))

    # print out length of data
    for k in d:
        print "%s - %s" % (k, len(d[k]))
