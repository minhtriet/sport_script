from itertools import islice
import numpy as np
import sys
import pdb
import os
import json

FRAME_PATH = "/media/data/mtriet/dataset/fb_frames_scnn_localization"
SUB_PATH = "/media/data/mtriet/fb/"

WINDOW_SIZE = 8 

def read_next_lines(f, n):
    # read n lines from subtitle and pre-process
    while True: 
        next_n_lines = list(islice(f, n))
        if not next_n_lines:
            return False
        if next_n_lines[1] != 'bg\n':
            break
    next_n_lines[0] = int(next_n_lines[0].split(' ')[1])
    next_n_lines[1] = next_n_lines[1].strip()
    next_n_lines[2] = int(next_n_lines[2].split(' ')[1])
    if (next_n_lines[1] == 'fkwg') or (next_n_lines[1] == 'fkwog'):
        next_n_lines[1] = 'fk'
    return next_n_lines

def iou(begin_frame, subtitle_lines):
    frames = range(begin_frame, begin_frame + WINDOW_SIZE)
    subtitles = range(subtitle_lines[0], subtitle_lines[2])
    intersection = len(np.intersect1d(frames, subtitles))
    union = len(frames) + len(subtitles) - intersection
    return intersection * 1. / union     

with open('%s_classes.json' % sys.argv[1], 'r') as f:
    classes = json.load(f)

with open('%s_train_scnn_localization.lst' % sys.argv[1], 'w') as r:
    for frame_root, sub_folder, sub_files in os.walk(FRAME_PATH):
        for folder in sub_folder:       
            print folder 
            frames = sorted(os.listdir(frame_root + '/' + folder))
            with open('%s/%s.aqt' % (SUB_PATH, folder), 'r') as f:
                next_n_lines = read_next_lines(f, 4)
                for begin_pivot in range(1, len(frames), WINDOW_SIZE + 1):
                    if begin_pivot > next_n_lines[2]:
                        next_n_lines = read_next_lines(f, 4)
                        if not next_n_lines:
                            break

                    end_pivot = min(begin_pivot + WINDOW_SIZE, len(frames))
                    iou_score = iou(begin_pivot, next_n_lines)
                    if iou_score > 0:
                        r.write("%s/%s/%05d.jpg %d %d %f\n" % \
                        (frame_root, folder, begin_pivot, WINDOW_SIZE, classes[next_n_lines[1].strip()], iou_score))
