import numpy as np
import random
from sklearn import model_selection

def balance(arr):
  length = map(len, arr)
  print("Length of classes: %s" % length)
  min_classes = np.argmin(length)
  for i in range(len(arr)):
    if i != min_classes:
      arr[i] = random.sample(arr[i], len(arr[min_classes]))
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
