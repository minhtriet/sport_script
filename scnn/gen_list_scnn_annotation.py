from itertools import islice
import numpy as np
import sys
import pdb
import os
import json
from subtitle import Subtitle

FRAME_RATE = 25.0

def read_next_lines(f, n):
    # read n lines from subtitle and pre-process
    next_n_lines = list(islice(f, n))
    if not next_n_lines:
        return False
    next_n_lines[0] = int(next_n_lines[0].split(' ')[1])
    next_n_lines[1] = next_n_lines[1].strip()
    next_n_lines[2] = int(next_n_lines[2].split(' ')[1])
    # for football
    if (next_n_lines[1] == 'fkwg') or (next_n_lines[1] == 'fkwog'):
        next_n_lines[1] = 'fk'
    return next_n_lines

def load_subtitle(path, aqt_file):
    subtitles = []
    with open('%s%s' % (path, aqt_file), 'r') as f:
        while True:
            lines = read_next_lines(f, 4)
            if lines:
                sub = Subtitle(lines[1], lines[0], lines[2])
                subtitles.append(sub)
            else:
                break
    return subtitles

def generate_data(path):
    subtitles = [x for x in os.listdir(path) if x.endswith('aqt')]    
    for aqt_file in subtitles:
        text_file = aqt_file.split('.')[0]
        subtitle = load_subtitle(path, aqt_file)
        subtitle = sorted(subtitle, key = lambda x: x.klass)
        current_class = None
        current_line = 0 
        while current_line < len(subtitle):
            if current_class != subtitle[current_line].klass:
                current_class = subtitle[current_line].klass
            with open("%s.txt" % current_class, 'a') as f:
                while (current_line < len(subtitle)) and (current_class == subtitle[current_line].klass):
                    f.write('%s%s %f %f\n' % (path, text_file, subtitle[current_line].start / FRAME_RATE, subtitle[current_line].end / FRAME_RATE))
                    current_line += 1
                    

if __name__ == '__main__':
  if len(sys.argv) < 2:
    print "gen_list <fb/bb>"
    sys.exit(1)
  PATH = "/media/data/mtriet/raw_video/%s_eval/" % sys.argv[1]
  with open('../%s_classes.json' % sys.argv[1], 'r') as f:
    classes = json.load(f)

  generate_data(PATH)
