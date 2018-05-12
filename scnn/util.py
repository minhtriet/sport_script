import random

import numpy as np
from sklearn import model_selection

def balance(arr):
  """
    balance based on a 2d array, exclude the [0] class
    and over sampling
  """
  length = map(len, arr)[1:]
  print("Length of classes: %s" % length)
  max_len = np.max(length)
  import pdb
  for i, _ in enumerate(arr):
    if len(arr[i]) < max_len:
      for j in range(max_len - len(arr[i])):
        try:
          arr[i].append( random.choice(arr[i]) )   # oversampling
        except:
          pdb.set_trace()
    else:
      arr[i] = random.sample(arr[i], max_len)
  length = map(len, arr)
  print("Length of classes: %s" % length)
  return arr

def print_data(train_file_addr, val_file_addr, x, y):

  def p_data(addr, arr):
    with open(addr, 'w') as f:
      for i in arr:
        f.write(str(i))

  cv = model_selection.StratifiedShuffleSplit(2)
  for train, val in cv.split(x, y):
    p_data(train_file_addr, x[train])
    p_data(val_file_addr, x[val])

def to_xy(arr):
  length = map(len, arr)
  y = []
  for index, l in enumerate(length):
    y.extend([index] * l)
  x = np.array(arr).flatten()
  return (x,y)
