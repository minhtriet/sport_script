from itertools import islice
import numpy as np
import sys
import pdb
import os
import json
from subtitle import Subtitle
import random

FRAME_PATH = "/media/data/mtriet/dataset/scnn_%s_frames" % sys.argv[1]
SUB_PATH = "/media/data/mtriet/raw_video/%s" % sys.argv[1]
WINDOW_SIZE = [16,32,64,128,256,512] 
OVERLAP_RATE = 0.75
ZERO_OUPUT_PROBABILITY = 0.015
TRAIN_VAL_SPLIT = 0.7

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

def print_data(train_file, val_file, frame_root, folder, begin_pivot, klass, window_size):
  if klass != 0:
    if random.random() < TRAIN_VAL_SPLIT: 
      train_file.write("%s/%s/ %06d %d %d\n" % (frame_root, folder, begin_pivot, klass, window_size/16))
    else:
      val_file.write("%s/%s/ %06d %d %d\n" % (frame_root, folder, begin_pivot, klass, window_size/16))
  else:
    if random.random() < ZERO_OUPUT_PROBABILITY: 
      if random.random() < TRAIN_VAL_SPLIT:
        train_file.write("%s/%s/ %06d %d %d\n" % (frame_root, folder, begin_pivot, klass, window_size/16))
      else:
        val_file.write("%s/%s/ %06d %d %d\n" % (frame_root, folder, begin_pivot, klass, window_size/16))

with open('../%s_classes.json' % sys.argv[1], 'r') as f:
  classes = json.load(f)
  count = [0] * len(classes)

with open('scnn_%s_train_classification.lst' % sys.argv[1], 'w') as train_file:
  with open('scnn_%s_val_classification.lst' % sys.argv[1], 'w') as val_file:
    for window_size in WINDOW_SIZE:
      for frame_root, sub_folder, sub_files in os.walk(FRAME_PATH):
        for folder in sub_folder:       
          print folder
          subtitles = load_subtitle(folder) 
          frames = sorted(os.listdir(frame_root + '/' + folder))
          sub_index = 0
          sub_class = classes[subtitles[sub_index].klass]
          for begin_pivot in range(1, len(frames) - window_size, int(window_size*(1 - OVERLAP_RATE))):  # ignore last few frames

              if (begin_pivot > subtitles[sub_index].end) and (sub_index < len(subtitles) - 1):
                  sub_index += 1
                  sub_class = classes[subtitles[sub_index].klass]

              end_pivot = min(begin_pivot + window_size, len(frames))
              segment = range(begin_pivot, begin_pivot + window_size + 1)
              sub_range = subtitles[sub_index].get_range()
              intersection = np.intersect1d(segment, sub_range)
              if len(intersection) == len(segment):        # the subtitle contains the segment
                count[ sub_class ] += 1
                print_data(train_file, val_file, frame_root, folder, begin_pivot, sub_class, window_size)
              else:
                  union = len(segment) + len(sub_range) - len(intersection)
                  current_score = 1.0 * len(intersection) / union 
                  if current_score > 0.7:
                      count[ sub_class ] += 1
                      Event event = new Event(frame_root, folder, begin_pivot,
                      print_data(train_file, val_file, frame_root, folder, begin_pivot, sub_class, window_size)
                      continue
                  else:  # check if next segment has better score, if > 0.7, and if max of them > 0.5
                      if sub_index < len(subtitles) - 1: # already at last subtitle
                        sub_range = subtitles[sub_index+1].get_range()
                        intersection = np.intersect1d(segment, sub_range)
                        next_score = 1.0 * len(intersection) / union 
                        if max(current_score, next_score) > 0.5:
                          count[ sub_class ] += 1
                          print_data(train_file, val_file, frame_root, folder, begin_pivot, sub_class, window_size)
                          continue
                      count[ 0 ] += 1
                      print_data(train_file, val_file, frame_root, folder, begin_pivot, 0, window_size)

# post processing, to balance out the classes

