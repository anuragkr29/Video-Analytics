prompt = 'Press "C" to for live detection and press any key to stop after the dection starts : ';
str = input(prompt , 's');
if str == 'C'
    % Create video input object. 
    vid = videoinput('winvideo',2);
    % Set video input object properties for this application.
    set(vid, 'FramesPerTrigger', Inf);
    vid.FrameGrabInterval = 1;
    vid.LoggingMode = 'disk&memory'; %store the acquired image to disk
    aviObject = VideoWriter('myVideo1');% Create a new AVI file
    aviObject.FrameRate = 15; % set the framerate
    vid.DiskLogger = aviObject;
    set(vid, 'ReturnedColorspace', 'rgb'); % set this property to get the colorspace to rgb
    % Create a figure window.
    % figure; 
    vid.FramesAcquiredFcnCount = 2;
    vid.FramesAcquiredFcn = {'detectedImg'};
    % Start acquiring frames.
    start(vid)
w = waitforbuttonpress;
if w == 0
    
else
    close all;
    I = getdata(vid,1,'uint8'); %get the frames to write into the video
    F = im2frame(I); % Convert I to a movie frame
    writeVideo(aviObject,F); % Add the frame to the file
    stop(vid);
    delete(vid);
end
end

h = msgbox('Video Saved');

prompt = 'Press "G" to grab an video image and proceed : ';
str = input(prompt , 's');
if str == 'G'
    prompt = 'give a noise density value between 0 and 1 : ';
    num = input(prompt);
    v = VideoReader('myVideo1.avi');
    videoFrame = read(v,15);
    noiseImage = imnoise(videoFrame,'salt & pepper',num);
    imshow(noiseImage);
end
prompt = 'Press "D" to denoise the image and show results : ';
str = input(prompt , 's');
if str == 'D'
    deNoisedImage = medfilt3(noiseImage,[3 3 3]);
    figure;
    subplot(1,2,1);imshow(noiseImage);title('Noisy Image');
    subplot(1,2,2);imshow(deNoisedImage);title('Denoised Image');
end
try
   stop(vid);
   delete(vid);
   clear vid;
catch exception
   
end

% stop(vid)