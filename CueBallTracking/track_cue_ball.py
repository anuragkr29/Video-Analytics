import numpy as np
import cv2
import time
import math
import sys
def track_cue_ball(videoFile):
    cap = cv2.VideoCapture(videoFile)
    # Parameters for lucas kanade optical flow
    lk_params = dict( winSize  = (13,13),
                      maxLevel = 5,
                      criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
    font                   = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (10,500)
    fontScale              = 1
    fontColor              = (255,255,255)
    lineType               = 2
    bottomLeftCornerOfText1 = (10,700)
    bottomLeftCornerOfText2 = (10,650)
    color = [[0 ,0 ,255],[220,150,124]]
    # Take first frame and find circle in it
    ret, old_frame = cap.read()
    old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
    p0,area = get_cue_coord(old_frame,old_gray,True)
    area_table = 356.9*177.8
    pixel_per_cm = (area_table)/area
    # Create a mask image for drawing
    mask = np.zeros_like(old_frame)
    count = 0
    start = time.time()
    while(1):
        ret,frame = cap.read()
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        count = count+1
        # calculate optical flow
        p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)

        # Select good points
        good_new = p1[st==1]
        good_old = p0[st==1]
        # draw the tracks
        for i,(new,old) in enumerate(zip(good_new,good_old)):
            a,b = new.ravel()
            c,d = old.ravel()
            mask = cv2.line(mask, (a,b),(c,d), color[1], 7)
            frame = cv2.circle(frame,(a,b),12,color[0],-1)
        end = time.time()
        seconds = end - start
        img = cv2.add(frame,mask)
        covered_area = max(abs(b-d) , abs(a-c))
        cv2.putText(img,'Velocity : {0:.2f} cm/sec'.format(math.sqrt(covered_area*pixel_per_cm)/seconds), 
            bottomLeftCornerOfText, 
            font, 
            fontScale,
            fontColor,
            lineType)
        cv2.putText(img,'fps : {}'.format(1/seconds), 
            bottomLeftCornerOfText1, 
            font, 
            fontScale,
            fontColor,
            lineType)
        cv2.putText(img,'Original fps : {}'.format(cap.get(cv2.CAP_PROP_FPS)), 
			bottomLeftCornerOfText2, 
			font, 
			fontScale,
			fontColor,
			lineType)
        cv2.namedWindow('frame',cv2.WINDOW_NORMAL)
        cv2.resizeWindow('frame', 900,800)
        cv2.imshow('frame',img)
        cv2.namedWindow('frame1',cv2.WINDOW_NORMAL)
        cv2.resizeWindow('frame1', 400,600)
        cv2.imshow('frame1',mask)
        start = time.time()
        fps = cap.get(cv2.CAP_PROP_FPS)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

        # Now update the previous frame and previous points
        old_gray = frame_gray.copy()

        if count %44==0 :
            p0 = get_cue_coord1(old_frame,old_gray)
        else:
            p0 = good_new.reshape(-1,1,2)
    cv2.destroyAllWindows()
    cap.release()



def get_cue_coord(image1,grayimg , flag = False):
    img1 = cv2.medianBlur(grayimg,5)
    hsv = cv2.cvtColor(image1, cv2.COLOR_BGR2HSV)
    lower_range = np.array([51, 63, 57], dtype=np.uint8)
    upper_range = np.array([84, 255, 255], dtype=np.uint8)
    mask = cv2.inRange(hsv, lower_range, upper_range)
    if flag:
        kernel = np.ones((53,53),np.uint8)
        opening = cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel, iterations = 2)
        area = cv2.countNonZero(mask)
    image, contours, hier = cv2.findContours(mask, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    areas = [cv2.contourArea(c) for c in contours]
    max_index = np.argmax(areas)
    cnt=contours[max_index]
    x, y, w, h = cv2.boundingRect(cnt)
    circles = cv2.HoughCircles(img1[y:y+h,x:x+w],cv2.HOUGH_GRADIENT,1,10,param1=10,param2=24,minRadius=10,maxRadius=25)
    p0 = []
    for i in circles[0,:]:
    # draw the outer circle
        p0.append(np.asarray([np.float32(i[0]+x),np.float32(i[1]+y)]))
    p0 = np.asarray(p0)
    p0 = p0.reshape(-1,1,2)
    if flag :
        return p0,area
    else:
        return p0


# In[79]:

def get_cue_coord1(image1,grayimg):
    img1 = cv2.medianBlur(grayimg,3)
    hsv = cv2.cvtColor(image1, cv2.COLOR_BGR2HSV)
    lower_range = np.array([51, 63, 57], dtype=np.uint8)
    upper_range = np.array([84, 255, 255], dtype=np.uint8)
    mask = cv2.inRange(hsv, lower_range, upper_range)
    t = cv2.bitwise_and(mask,img1)
    # noise removal
    p0 = []
    circles = cv2.HoughCircles(t,cv2.HOUGH_GRADIENT,1,10,param1=10,param2=19,minRadius=3,maxRadius=28)
    circles = np.uint16(np.around(circles))
    max_tuple0 = []
    max_tuple1 = []
    for i in circles[0,:]:
        # draw the outer circle
        if (img1[i[1]][i[0]]) > 100 :
            max_tuple0.append(i[0])
            max_tuple1.append(i[1])
            
    p0.append(np.asarray([np.float32((max_tuple0[0])),np.float32((max_tuple1[0]))]))
    p0 = np.asarray(p0)
    p0 = p0.reshape(-1,1,2)
    return p0
def main():
	args = (sys.argv)
	filename= str(args[1])
	try:
		track_cue_ball(filename)
	except :
		cv2.destroyAllWindows()
		cap.release()


if __name__ == "__main__":
	main()




