# Read non-bg data, assume the rest is bg

import sys
import pdb
import os
import json

import numpy as np

from subtitle import Subtitle
from event import Event
import util

FRAME_PATH = "/media/data/mtriet/dataset/scnn_%s_frames" % sys.argv[1]
SUB_PATH = "/media/data/mtriet/raw_video/%s/train" % sys.argv[1]
WINDOW_SIZE = [16, 32, 64, 128, 256, 512]
OVERLAP_RATE = 0.75
TRAIN_VAL_SPLIT = 0.7

with open('../%s_classes.json' % sys.argv[1], 'r') as f:
  classes = json.load(f)
  events = [[] for _ in range(len(classes))] 

for window_size in WINDOW_SIZE:
  for frame_root, sub_folder, sub_files in os.walk(FRAME_PATH):
    for folder in sub_folder:
      print folder
      subtitles = Subtitle.load_subtitle(SUB_PATH, folder, sys.argv[2])
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
          event = Event(frame_root, folder, begin_pivot, sub_class, window_size)
          events[sub_class].append(event)
        else:
          union = len(segment) + len(sub_range) - len(intersection)
          current_score = 1.0 * len(intersection) / union 
          if current_score > 0.7:
            event = Event(frame_root, folder, begin_pivot, sub_class, window_size)
            events[sub_class].append(event)
            continue
          else:  # check if next segment has better score, if > 0.7, and if max of them > 0.5
            if sub_index < len(subtitles) - 1: # not at last subtitle
              sub_range = subtitles[sub_index+1].get_range()
              intersection = np.intersect1d(segment, sub_range)
              next_score = 1.0 * len(intersection) / union 
              if max(current_score, next_score) > 0.5:
                event = Event(frame_root, folder, begin_pivot, sub_class, window_size)
                events[sub_class].append(event)
                continue
            event = Event(frame_root, folder, begin_pivot, 0, window_size)
            events[0].append(event)

# post processing, to balance out the classes
events= util.balance(events)
(x, y) = util.to_xy(events)
util.print_data('scnn_%s_train_classification.lst' % sys.argv[1], 'scnn_%s_val_classification.lst' % sys.argv[1], x, y)

