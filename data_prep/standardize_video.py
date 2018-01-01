import sys
import os
import subprocess
import math
import pdb
import shutil

def get_frame_rate(filename):
    if not os.path.exists(filename):
        sys.stderr.write("ERROR: filename %r was not found!" % (filename,))
        return -1         
    out = subprocess.check_output(["ffprobe",filename,"-v","0","-select_streams","v","-print_format","flat","-show_entries","stream=r_frame_rate"])
    rate = out.split('=')[1].strip()[1:-1].split('/')
    if len(rate)==1:
        return float(rate[0])
    if len(rate)==2:
        return float(rate[0])/float(rate[1])

for i in range(1, len(sys.argv)):
  if int(math.ceil(get_frame_rate(sys.argv[i]))) == 30:
    base = os.path.dirname(sys.argv[i]) + '/output/'
    try:
      shutil.rmtree(base)
    except:
      pass
    os.mkdir(base)
    filename = os.path.basename(sys.argv[i])
    subprocess.check_call("ffmpeg -i %s -r 25 -strict -2 %s/%s" % (sys.argv[i], base, filename), shell=True)
    

