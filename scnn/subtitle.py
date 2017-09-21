class Subtitle(object):

  def __init__(self, klass, start, end):
    self.klass = klass
    self.start = start
    self.end = end

  def get_range(self):
    return range(self.start, self.end+1)
