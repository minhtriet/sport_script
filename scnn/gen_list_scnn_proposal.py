from itertools import islice
import numpy as np
import sys
import pdb
import os
import json
from subtitle import Subtitle

FRAME_PATH = "/media/data/mtriet/dataset/scnn_%s_frames" % sys.argv[1]
SUB_PATH = "/media/data/mtriet/%s/" % sys.argv[1]
WINDOW_SIZE = [8, 16, 32, 64, 128] 

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

def load_subtitle(folder):
    subtitles = []
    with open('%s/%s.aqt' % (SUB_PATH, folder), 'r') as f:
        while True:
            lines = read_next_lines(f, 4)
            if lines:
                sub = Subtitle(lines[1], lines[0], lines[2])
                subtitles.append(sub)
            else:
                break
    return subtitles

with open('../%s_classes.json' % sys.argv[1], 'r') as f:
    classes = json.load(f)

with open('scnn_%s_train_proposal.lst' % sys.argv[1], 'w') as r:
    for window_size in WINDOW_SIZE:
        for frame_root, sub_folder, sub_files in os.walk(FRAME_PATH):
            for folder in sub_folder:       
                print folder
                subtitles = load_subtitle(folder) 
                frames = sorted(os.listdir(frame_root + '/' + folder))
                sub_index = 0
                for begin_pivot in range(1, len(frames) - window_size, window_size + 1):  # ignore last few frames
#                    if (folder == "M_GBR-KOR") and (begin_pivot > 157640) and (window_size == 16):
 #                       pdb.set_trace()

                    if begin_pivot > subtitles[sub_index].end:
                        if sub_index < len(subtitles) - 1:
                            sub_index += 1 

                    end_pivot = min(begin_pivot + window_size, len(frames))
                    # if window is in the segment, assign as 1                    
                    segment = range(begin_pivot, begin_pivot + window_size + 1)
                    sub_range = subtitles[sub_index].get_range()
                    intersection = np.intersect1d(segment, sub_range)

                    if len(intersection) == len(segment):        # the subtitle contains the segment
                        r.write("%s/%s/ %06d %d %d\n" % (frame_root, folder, begin_pivot, 1, window_size))
                    elif len(intersection) == 0:        # not contains at all, and frame.start < subtitle.start 
                        r.write("%s/%s/ %06d %d %d\n" % (frame_root, folder, begin_pivot, 0, window_size))
                    else:
                        union = len(segment) + len(sub_range) - len(intersection)
                        current_score = 1.0 * len(intersection) / union 
                        if current_score > 0.7:
                            r.write("%s/%s/ %06d %d %d\n" % (frame_root, folder, begin_pivot, 1, window_size))
                        else:  # check if next segment has better score, if > 0.7, and if max of them > 0.5
                            if (sub_index == len(subtitles) - 1) or (subtitles[sub_index+1].klass == 'bg'):
                                r.write("%s/%s/ %06d %d %d\n" % (frame_root, folder, begin_pivot, 0, window_size))
                            else:
                                sub_range = subtitles[sub_index+1].get_range()
                                intersection = np.intersect1d(segment, sub_range)
                                next_score = 1.0 * len(intersection) / union 
                                if max(current_score, next_score) > 0.5:
                                    r.write("%s/%s/ %06d %d %d\n" % (frame_root, folder, begin_pivot, 1, window_size))
                                else:
                                    r.write("%s/%s/ %06d %d %d\n" % (frame_root, folder, begin_pivot, 1, window_size)) 
