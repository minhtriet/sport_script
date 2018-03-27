function gt_to_proposal = (sport)

GT_PATH = ['/media/data/mtriet/dataset/ground_truth/' sport]

mat_files = dir(GT_PATH)
for file = mat_files(3:size(mat_files, 1))
  load(file.name)
  seg_swin = zeros(0,12)
  for x = gt
    if x(1) ~= 1    % not bg
    end  
  end
end

    
 
