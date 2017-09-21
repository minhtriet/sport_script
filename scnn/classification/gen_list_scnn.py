# walk through all file

import os
import json
import re
import random
import sys
import pdb

DEFAULT_WINDOW = 8

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'gen_list_scnn <fb/bb>'
        sys.exit(-1)
        
    path = '/media/data/mtriet/dataset/'

    with open('%s_classes.json' % sys.argv[1], 'r') as f:
        classes = json.load(f)

    d = dict.fromkeys(classes)
    for x in d:
        d[x] = []

    test_file = "scnn_test_%s.txt" % sys.argv[1]
    train_file = "scnn_train_%s.txt" % sys.argv[1]
    val_file = "scnn_val_%s.txt" % sys.argv[1]

    sub_path = os.path.join(path, "%s_frames" % sys.argv[1])
    for sub_r, sub_s, sub_files in os.walk(sub_path):
        for aVid in sub_s:
            class_name = re.split('_', aVid)[-1]
            d[class_name].append(os.path.join(sub_r, aVid))

    for x in d:
       random.shuffle(d[x])

    with open(test_file, 'w') as f:
        for x in d:
            for video in d[x][: len(d[x]) / 3]:
                frames = len(os.listdir(video))
                if frames < DEFAULT_WINDOW:
                    if x == 'bg':
                        continue
                    else:
                        print "%s is too short" % video
                for i in range(1, frames, DEFAULT_WINDOW):
                    if frames - i < DEFAULT_WINDOW:
                        break
                    f.write("%s %d %s %d\n" % (video, i, classes[x], DEFAULT_WINDOW))
    with open(train_file, 'w') as f:
        for x in d:
            for video in d[x][len(d[x]) / 3 : ]:
                frames = len(os.listdir(video))
                if frames < DEFAULT_WINDOW:
                    if x == 'bg':
                        continue
                    else:
                        print "%s is too short" % video
                for i in range(1, frames, DEFAULT_WINDOW):
                    if frames - i < DEFAULT_WINDOW:
                        break
                    f.write("%s %d %s %d\n" % (video, i, classes[x], DEFAULT_WINDOW))

    # print out length of data
    for k in d:
        print "%s - %s" % (k, len(d[k]))

