# check if a frame appears two times
# prompt the user to that frame

import os
from collections import defaultdict
import pdb
import glob
import subprocess
import sys

INPUT = '/media/data/mtriet/raw_video/%s/train/' % sys.argv[1]

for sub in glob.glob(INPUT + '*.aqt'):
  video_name = sub[:-3] + 'mp4'
  print video_name
  num_frm = subprocess.check_output('ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames -of default=nokey=1:noprint_wrappers=1 %s ' % video_name, shell=True)
  occupied = [False] * int(num_frm)
  with open(sub, 'r') as f:
    while True:
      start = f.readline()
      if not start:
        break
      start = start.split("-->>")[1].strip()
      start = int(start)
      text = f.readline().strip()
      end = f.readline()
      end = end.split("-->>")[1].strip()
      end = int(end)
      if any(occupied[start:end]):
        print "%d %d" % (start, end)
        pdb.set_trace()
        print "%s failed" % video_name
        break
      occupied[start:end] = [True] * (end - start + 1)
      f.readline()
