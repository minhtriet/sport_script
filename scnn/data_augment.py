import os
import shutil
import pdb

DATA_PATH = '/media/data/mtriet/dataset'
src = os.path.join(DATA_PATH, 'scnn_fb_frames')
dst = os.path.join(DATA_PATH, 'scnn_fb_frames_augment')
if not os.path.isdir(dst):
  shutil.copytree(src, dst)
for directory in os.listdir(dst):
  print directory
  for root, dirs, files in os.walk(dst):
    for f in files:
      os.system('mogrify -flop %s/%s/%s' % (dst, directory, f))
      

