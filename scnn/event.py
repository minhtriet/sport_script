class Event
  
  def __init__(self, frame_root, folder, begin_pivot):
    self.frame_root = frame_root
    self.folder = folder
    self.begin_pivot = begin_pivot

  def to_string(self, mirror=False)
    if mirror:
      return "%s/%s/ %06d %d %d\n" % (frame_root + "_augment", folder, begin_pivot, klass, window_size/16)
    else:
      return "%s/%s/ %06d %d %d\n" % (frame_root, folder, begin_pivot, klass, window_size/16)
