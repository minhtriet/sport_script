from itertools import islice

class Subtitle(object):

  def __init__(self, klass, start, end):
    self.klass = klass
    self.start = start
    self.end = end

  def get_range(self):
    return range(self.start, self.end+1)

  @staticmethod
  def load_subtitle(SUB_PATH, folder, pad):

    def read_next_lines(f, n):
      # read n lines from subtitle and pre-process
      while True:        
          next_n_lines = list(islice(f, n))
          if not next_n_lines:
              return False
          if next_n_lines[1] != 'bg\n':
              break
      next_n_lines[0] = int(next_n_lines[0].split(' ')[1])
      next_n_lines[1] = next_n_lines[1].strip()
      next_n_lines[2] = int(next_n_lines[2].split(' ')[1])
      if (next_n_lines[1] == 'fkwg') or (next_n_lines[1] == 'fkwog'):
          next_n_lines[1] = 'fk'
      if (next_n_lines[1] == 'pkwg') or (next_n_lines[1] == 'pkwog'):
          next_n_lines[1] = 'pk'
      return next_n_lines

    subtitles = []
    filename = '%s/%s_pad.aqt' % (SUB_PATH, folder) if pad else '%s/%s.aqt' % (SUB_PATH, folder)
    print(filename)
    with open(filename, 'r') as f:
        while True:
            lines = read_next_lines(f, 4)
            if lines:
                sub = Subtitle(lines[1], lines[0], lines[2])
                subtitles.append(sub)
            else:
                break
    return subtitles

  def to_string(self, front_pad, rear_pad):
    return "-->> %d \n %s \n-->> %d \n\n" % (max(0, int(self.start)-25*int(front_pad)), self.klass, int(self.end)+25*int(rear_pad))

