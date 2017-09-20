import os
from collections import defaultdict
import pdb

INPUT = '/media/data/mtriet/dataset/fb_frames'
print INPUT
match_names = defaultdict(list)
names = sorted(os.listdir(INPUT), key=lambda x: int(x.split('_')[-2]))
for i in names:
    match_names['_'.join(i.split('_')[:-2])].append(i)

for match in match_names:
    with open(match + '.aqt', 'w') as f:
        for i in match_names[match]:
            print i
            names = sorted(os.listdir(INPUT + '/' + i), key=lambda x: os.path.basename(x))
            if len(names) == 0: # empty folder
                os.rmdir(INPUT + '/' + i)
                continue
            f.write("-->> %s\n%s\n-->> %s\n\n" % (names[0].split('.')[0], i.split('_')[-1], names[-1].split('.')[0]))


