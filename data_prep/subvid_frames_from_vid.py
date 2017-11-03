# -*- coding: utf-8 -*-
"""
Created on Wed May 31 11:45:14 2017

@author: mtriet
"""

import sys
import os
import pdb

if len(sys.argv) < 2:
    sys.stderr.write('Enter video name ')
    sys.exit(1)
for i in sys.argv[1:]:
  file_name = i
  output = 0

  # split the video frame by frame
  with open(file_name.split('.')[0] + '_auto.aqt') as f:
      new_folder = os.path.basename(file_name).split('.')[0]
      if not os.path.exists(new_folder):
          os.makedirs(new_folder)

      while True:
          start = f.readline()
          if not start:
            break
          start = start.split("-->>")[1].strip()
          text = f.readline().strip()
          end = f.readline()
          end = end.split("-->>")[1].strip()
          new_subfolder = '%s_%s' % (new_folder, text)
          os.system('mkdir %s/%s' % (new_folder, new_subfolder))
          for k, v in enumerate(xrange(int(start), int(end))):
              os.system('mv %s/%05d.jpg %s/%s/%05d.jpg' % (new_folder, v+1, new_folder, new_subfolder, k+1))
          f.readline()

  f.close()
