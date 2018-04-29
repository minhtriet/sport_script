function [ ] = gen_groundtruth(sport)
videodir = ['/media/data/mtriet/raw_video/', sport,'/eval/'];
framesdir = ['/media/data/mtriet/dataset/', sport, '_frames_eval/'];

subtitles = dir([videodir '*.aqt']);
no_classes = containers.Map({'fb', 'bb'}, {6, 8});

classes = containers.Map();
classes('fb') = {'bg', 'gs', 'sot', 'pkwg', 'fk', 'pkwog'};
classes('bb') = {'bg', 'ps', 'sd', 'bs', 'ao', 'fs', 'or', 'dr'};

for j = 1:length(subtitles)
  name = subtitles(j).name;
  if isempty(strfind(name, 'auto'))
    videoname = strrep(name, 'aqt', 'mp4');
    name = strsplit(name, '.')
    name = name{1};
    [class, time] = textread([videodir name '.aqt'],'%s%d');    
    len = time(end); 
    gt = cell(1, len);
    gt(:) = {'bg'};
    for line = 1:3:length(class)
      if ~( strcmp(strjoin(class(line+1)), 'bg') )
        if strcmp(strjoin(class(line+1)), 'fkwg') || strcmp(strjoin(class(line+1)), 'fkwog') 
          gt(time(line):time(line+2)) = {'fk'};
        else
          gt(time(line):time(line+2)) = class(line+1);
        end
      end        
    end

    true_len = size(dir([framesdir videoname(1:end-4) '/*.jpg']),1);
    for i=(1:true_len - size(gt,2))
      gt(end + 1) = {'bg'};
    end
    onehot_gt = zeros(length(classes(sport)), length(gt));
    for i = 1:length(gt)
      temp = zeros(1, no_classes(sport));
      position = find( ismember(classes(sport), gt(i)) );
      temp(1, position) = 1;
      onehot_gt(:, i) = temp;
    end
    gt = onehot_gt;
    save(['/media/data/mtriet/dataset/ground_truth/' sport '/' name '.mat'], 'gt');
  end
end
end
