This matlab program performs the following functions :
1. Detects a fixed object color in real-time.
2. Saves the video of the live streaming.
3. Adds salt and pepper noise to a random videoframe.
4. Removes the noise using median filterning


-----------------------Object Detection---------------------
To detect an object , an RGB image is converted to HSV image.
Then , applying a particular threshold to Hue, Saturation and Value
a mask is obtained. The mask is then applied to the original
image detecting the object. Dilate and erode method is used for
better clarity and detection at the last , on the mask.

-----------------------Saving the Video---------------------
The original video that is streaming is saved and not the one
which has the detected object.

-----------------------Noise Addition-----------------------
Salt and Pepper noise is added using imnoise function in matlab.
I have also made a program to do the same(included in the zip) , 
but for better performance I have used the matlab function.

-----------------------Noise Removal-----------------------
Noise is removed using the matlab function medfilt , applying
a median filter on the rgb image.

To use the code , run the main_program.m in matlab and follow
the instructions.

The average time calculation is printed in the matlab console
calculated for each 5 frames and mean of the values.

The noise density can vary between 0 and 1 and the user can give
a manual input for the noise density to be added to the image.
