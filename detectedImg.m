function detectedImg(obj,event)

sample_frame = peekdata(obj,1);
tic
HSV = rgb2hsv(sample_frame);
[BW] = createMask(HSV);
SE = strel('rectangle',[35,25]);
BW3 = imerode(BW,SE);
BW4 = imdilate(BW3,SE);
sample_frame(repmat(BW4,[1 1 3])) = 0;
end_time = toc;
imagesc(sample_frame);
clear sample_frame;
Elapsed_time = [];
drawnow; % force an update of the figure window
Elapsed_time = [Elapsed_time  end_time];
if size(Elapsed_time,1) == 5
    Elapsed_time = [];
end
sprintf('%s %.2f','Average Time', mean(Elapsed_time))
