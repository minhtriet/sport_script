class Event(object):
  
  def __init__(self, frame_root, folder, begin_pivot, sub_class, window_size):
    self.frame_root = frame_root
    self.folder = folder
    self.begin_pivot = begin_pivot
    self.sub_class = sub_class
    self.window_size = window_size

  def to_string(self, mirror=False):
    if mirror:
      return "%s/%s/ %06d %d %d\n" % (self.frame_root + "_augment", self.folder, self.begin_pivot, self.sub_class, self.window_size/16)
    else:
      return "%s/%s/ %06d %d %d\n" % (self.frame_root, self.folder, self.begin_pivot, self.sub_class, self.window_size/16)
