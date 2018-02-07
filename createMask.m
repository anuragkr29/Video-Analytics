function [BW] = createMask(HSV) 
% Convert RGB image to HSV image
I = HSV;
% Define thresholds for 'Hue'
channel1Min = 0.910;
channel1Max = 0.995;
% Define thresholds for 'Saturation'
channel2Min = 0.20;
channel2Max = 0.850;
% Define thresholds for 'Value'
channel3Min = 0.300;
channel3Max = 0.700;
% Create mask based on chosen histogram thresholds
BW = ( (I(:,:,1) >= channel1Min) | (I(:,:,1) <= channel1Max) ) & ...
    (I(:,:,2) >= channel2Min ) & (I(:,:,2) <= channel2Max) & ...
    (I(:,:,3) >= channel3Min ) & (I(:,:,3) <= channel3Max);
