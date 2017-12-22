# create a matfile whose elements is the prior of the class
import json
import sys
import scipy.io as sio
import pdb

# load classes
with open('/media/data/mtriet/dataset/script/%s_classes.json' % sys.argv[1], 'r') as f:
  maps = json.load(f)

count_map = [0]*len(maps)
 
# count each classes
with open('/media/data/mtriet/dataset/scnn_%s_train_localization.lst' % sys.argv[1]) as f:
  lines = f.readlines()
  for l in lines:
    l = int(l.split(' ')[2])
    count_map[l] += 1
sio.savemat('%s_freq.mat' % sys.argv[1], {'freq': count_map});
