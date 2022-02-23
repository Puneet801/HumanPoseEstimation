from __future__ import print_function
import sys
import cv2
from random import randint
import matplotlib.pyplot as plt
import math
import collections 
from collections import Counter


trackerTypes = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']


def createTrackerByName(trackerType):
        # Create a tracker based on tracker name
        if trackerType == trackerTypes[0]:
            tracker = cv2.legacy.TrackerBoosting_create()
        elif trackerType == trackerTypes[1]:
            tracker = cv2.legacy.TrackerMIL_create()
        elif trackerType == trackerTypes[2]:
            tracker = cv2.legacy.TrackerKCF_create()
        elif trackerType == trackerTypes[3]:
            tracker = cv2.legacy.TrackerTLD_create()
        elif trackerType == trackerTypes[4]:
            tracker = cv2.legacy.TrackerMedianFlow_create()
        elif trackerType == trackerTypes[5]:
            tracker = cv2.legacy.TrackerGOTURN_create()
        elif trackerType == trackerTypes[6]:
            tracker = cv2.TrackerMOSSE_create()
        elif trackerType == trackerTypes[7]:
            tracker = cv2.legacy.TrackerCSRT_create()
        else:
            tracker = None
            print('Incorrect tracker name')
            print('Available trackers are:')
            for t in trackerTypes:
                print(t)

        return tracker





# Set video to load
videoPath = "filmAunty.mp4"

# Create a video capture object to read videos
cap = cv2.VideoCapture(videoPath)

# Read first frame
success, frame = cap.read()
# quit if unable to read the video file
if not success:
  print('Failed to read video')
  sys.exit(1)

  ## Select boxes
bboxes = []
colors = [] 

# OpenCV's selectROI function doesn't work for selecting multiple objects in Python
# So we will call this function in a loop till we are done selecting all objects
while True:
  # draw bounding boxes over objects
  # selectROI's default behaviour is to draw box starting from the center
  # when fromCenter is set to false, you can draw box starting from top left corner
  bbox = cv2.selectROI('MultiTracker', frame)
  bboxes.append(bbox)
  colors.append((randint(0, 255), randint(0, 255), randint(0, 255)))
  print("Press q to quit selecting boxes and start tracking")
  print("Press any other key to select next object")
  k = cv2.waitKey(0) & 0xFF
  print(k)
  if (k == 113):  # q is pressed
    break

print('Selected bounding boxes {}'.format(bboxes))

# Specify the tracker type
trackerType = "CSRT"
createTrackerByName(trackerType)

# Create MultiTracker object
multiTracker = cv2.legacy.MultiTracker_create()


# Initialize MultiTracker 
for bbox in bboxes:
  multiTracker.add(createTrackerByName(trackerType), frame, bbox)

left = []
right = []
temp = []
temp1 =[]
axis = []
axis1 = []
p = 0
q = 0
a=0
b=0
t=0
g =0
j=1
  # Process video and track objects
while cap.isOpened():
  t = t+1
  success, frame = cap.read()
  if not success:
    break

  (h1, w1) = frame.shape[:2] #w:image-width and h:image-height

  # get updated location of objects in subsequent frames
  success, boxes = multiTracker.update(frame)
  # draw tracked objects
  for i, newbox in enumerate(boxes):
    p1 = (int(newbox[0]), int(newbox[1]))
    p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
    cv2.rectangle(frame, p1, p2, colors[i], 2, 1)
    x=p1[0]
    y=p1[1]
    w=p2[0] - x
    h=p2[1] - y
    x2 = x + int(w/2)
    y2 = y + int(h/2)                                       
    cv2.circle(frame,(x2,y2),4,(0,255,0),-1)
    
    distance = int(math.sqrt(((x2-(w1//2))**2)+((y2-(h1//2))**2))) 
    if i == 0:
      temp.append(distance)
    if i ==1:
      temp1.append(distance)
    #LEFT
    if i==0:
      flag = 0
      count = 0 
      if len(temp)>7:     
        data = collections.Counter(temp[-7:])
        mode = data.most_common(1)
        for f in temp[-7:]:
          x = list(range(mode[0][0]-4,mode[0][0]+4))
          if f in x:
            count += 1
            flag = 1
          else:
            flag = 0
            break
        if count == 7 :
          left.append(0) 
      else:
        left.append(0)
      if flag==0 and len(temp)>7:
        left.append(distance)
    #RIGHT
    if i==1:
      flag1 = 0
      count1 = 0 
      if len(temp1)>7:     
        data = collections.Counter(temp1[-7:])
        mode = data.most_common(1)
        for f in temp1[-7:]:
          x = list(range(mode[0][0]-4,mode[0][0]+4))
          if f in x:
            count1 += 1
            flag1 = 1
          else:
            flag1 = 0
            break
        if count1 == 7 :
          right.append(0) 
      else:
        right.append(0)
      if flag1==0 and len(temp1)>7:
        right.append(distance)

    
    
    if i==0:
      if left[-1]==0:
        j+=1
        g += 1
      elif left[-1] != 0 and g < 20 :
        g=0
      if left[-1] !=0 and j < 20 :
        fix = t
      
      #XAXIS
      if len(left)>20:
        if left[-1] != 0 and g>=20:
          axis.append(t)
          g=0

        if left[-1] ==0:
          if j==20:
            axis1.append(fix)
        elif left[-1] !=0:       
          j = 0
          





    

  # show frame
  cv2.imshow('MultiTracker', frame)

# quit on ESC button
  if cv2.waitKey(1) & 0xFF == ord('d'):  # Esc pressed
    break

print(axis,axis1)


fig,ax = plt.subplots()
plt.plot(list(range(1,t)),left,label='Left Hand')
plt.plot(list(range(1,t)),right,label='Right Hand')
for i in range(len(axis)):  

  ax.annotate("("+str(axis[i])+","+str(axis1[i])+")",xy=(axis[i],0),xytext=(axis[i], -20),arrowprops = dict(facecolor = 'green',shrink=0.05),ha='left',rotation=45)
  
#ax.xaxis.set_major_formatter(plt.NullFormatter())
#plt.xticks(list(range(1,t)), )
plt.legend()
plt.grid(True)
ax.set_ylim(-30,200)
plt.show()

cv2.destroyAllWindows()
cap.release()