# generate train.txt in imagenet train example
# n01440764/n01440764_10026.JPEG 0
# n01440764/n01440764_10027.JPEG 0 
# ...
# n01443537/n01443537_10007.JPEG 1
# n01443537/n01443537_10014.JPEG 1

import os
import random
import sys
import pdb
import glob

if __name__ == '__main__':
  if len(sys.argv) < 2:
    print 'gen_list_huawei <fb/bb>'
    sys.exit(-1)
        
  path = '/media/data/mtriet/dataset/%s_frames' % sys.argv[1]
  with open('%s_frames_list.txt' % sys.argv[1], 'w') as f:
    i = 0
    for sub_folder in glob.glob("%s/*" % path):
      print sub_folder 
      for img in glob.glob("%s/*.jpg" % sub_folder):
        f.write('%s %d\n' % (img, i))
      i += 1
      
