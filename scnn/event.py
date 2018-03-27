import pdb

class Event(object):
  
  def __init__(self, frame_root, folder, begin_pivot, sub_class, window_size, score=None):
    self.frame_root = frame_root
    self.folder = folder
    self.begin_pivot = begin_pivot
    self.sub_class = sub_class
    self.window_size = window_size
    if not score is None:
      self.score = score 

  def to_string(self, mirror=False):
    if mirror:
      try:
        return "%s/%s/ %06d %d %d %f\n" % (self.frame_root + "_augment", self.folder, self.begin_pivot, self.sub_class, self.window_size/16, self.score)
      except:
        return "%s/%s/ %06d %d %d\n" % (self.frame_root + "_augment", self.folder, self.begin_pivot, self.sub_class, self.window_size/16)
    else:
      try:
        return "%s/%s/ %06d %d %d %f\n" % (self.frame_root, self.folder, self.begin_pivot, self.sub_class, self.window_size/16, self.score)
      except:
        return "%s/%s/ %06d %d %d\n" % (self.frame_root, self.folder, self.begin_pivot, self.sub_class, self.window_size/16)
