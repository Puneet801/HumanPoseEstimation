import cv2
import mediapipe as mp
import time
import math
import matplotlib.pyplot as plt
import collections 
from collections import Counter
from scipy.signal import savgol_filter

# Create Video object
cap = cv2.VideoCapture('0e.mp4')
# Formality we have to write before start
# using this model 
mpHands = mp.solutions.hands
# Creating an object from class Hands
hands = mpHands.Hands()
# creating an object to draw hand landmarks
mpDraw = mp.solutions.drawing_utils
# Previous time for frame rate
pTime = 0
# Current time for frame rate
cTime = 0
i=1
fin=[]
t=0
left=[0]
g=0
j=1
axis=[]
axis1=[]
while cap.isOpened():
    
    # Getting our Frame
    success, img = cap.read()
    if not success:
        break
    (h1, w1) = img.shape[:2]
    midx = w1//2
    midy = h1//2
    # Convert image into RGB
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # Calling the hands object to the getting results
    results = hands.process(imgRGB)
    indicator = 0
    # Checking something is detected or not
    if results.multi_hand_landmarks :
        # Extracting the multiple hands 
        # Go through each hand 
        mx = []
        my = []
        for handLms in results.multi_hand_landmarks:
            
            x= []
            y = []
            #print(handLms.landmark)
            # Getting id(index number) and landmark of each hand
            for id, lm in enumerate(handLms.landmark):
                #print(id,lm)
                # Height, width and channel of image
                h, w, c = img.shape
                # X and Y coordinate 
                # their values in decimal so 
                # we have to convert into pixel
                cx, cy = int(lm.x*w),int(lm.y*h)
                #print(id, cx, cy)
                
                x.append(cx)
                y.append(cy)
                
                #if id ==4:
            #print("end")
            cx = sum(x)//len(x)
            cy = sum(y)//len(y)
            cv2.circle(img, (cx, cy), 7, (255,0,255), cv2.FILLED)
            mx.append(cx)
            my.append(cy)
            



            # Draw the landmarks and line of the each hands
            #mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
        if(len(mx)==1 and len(my)==1):
            left.append(left[-1])
            t+=1
            
        if(len(mx)==2 and len(my)==2):
            t = t+1
            cx=(mx[0]+mx[1])//2
            cy=(my[0]+my[1])//2
            distance = int(math.sqrt(((cx-(w1//2))**2)+((cy-(h1//2))**2))) 
            fin.append(distance)
            cv2.circle(img,(cx,cy), 7, (255,255,255), cv2.FILLED)
            flag = 0
            count = 0 
            if len(fin)>20:
                data = collections.Counter(fin[-20:])
                mode = data.most_common(1)
                for f in fin[-20:]:
                    x = list(range(mode[0][0]-20,mode[0][0]+20))
                    if f in x:
                        count += 1
                        flag = 1
                    else:
                        flag = 0
                        break
                if count == 20 :
                    left.append(0) 
            else:
                left.append(0)
            if flag==0 and len(fin)>20:
                left.append(distance)
            
            # if left[-1]==0:
            #     j+=1
            #     g += 1
            # elif left[-1] != 0 and g < 20 :
            #     g=0
            # if left[-1] !=0 and j < 20 :
            #     fix = t
    
            # #XAXIS
            # if len(left)>50:
            #     if left[-1] != 0 and g>=20:
            #         axis.append(t)
            #         g=0

            #     if left[-1] ==0:
            #         if j==20:
            #             axis1.append(fix)
            #     elif left[-1] !=0:       
            #         j = 0
        # else:
        #     t=t+1
        #     fin.append(0)

        
    # Getting the current time
    cTime = time.time()
    # Getting frame per second 
    fps = 1/(cTime-pTime)
    # Previous time become current time
    pTime = cTime
    # Labeling the Frame rate 
    #cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
    cv2.putText(img,str(t),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)

    cv2.imshow("image",img) # Show the frame

    if cv2.waitKey(1) & 0xFF == ord('q'): # Wait for 1 millisecond
        break

# for i in range(len(left)-1,0,-1):
#   if left[i] !=0:
#     axis1.append(left.index(left[i]))
#     break



fig,ax = plt.subplots()
left = savgol_filter(left, 121, 2)
maxx = max(left)
# maxx = max(left)
# print(w)
for i in range(len(left)):
    left[i] = left[i] / maxx
    if left[i] <= 0.3:
        left[i] = 0
    
for i in range(len(left)):
    if left[i] < 0:
        left[i] = 0
for i in range(len(left)-1):
    if left[i] == 0 and left[i+1] !=0:
        axis.append(i+1)
    if left[i]!=0 and left[i+1] ==0:
        axis1.append(i+1)
if(len(axis)>len(axis1)):
    axis.pop()
print((axis),(axis1))# print(len(axis),len(axis1))
#plt.plot(list(range(0,t)),left[1:])

tim = []
ex=[0]
for i in range(len(axis)):
  s1 = '(' + str(axis[i]) + ',' + str(axis1[i]) + ')'
  b = axis[i]+1070.6
  for j in range(i,len(axis)):
    if (ex[-1]<axis[i]):
        if (axis1[j]>b):
            ex.append(axis1[j])
            print(axis1[j-1],axis[i])
            tim.append((axis1[j-1]-axis[i])/22)
            break
  ax.annotate(s1,xy=((axis1[i]+axis[i])//2,-0.3),xytext=((axis1[i]+axis[i])//2, -0.8),arrowprops = dict(facecolor = 'red', shrink = 0.05),ha='left',rotation=90)


print(tim)
yaxis= (len(tim))
#yaxis = [str(tim[0])]
#xaxis = list(range(0,int((sum(tim)/22))))
xaxis = [str((sum(tim)))]
plt.bar(xaxis , yaxis, color ='maroon')
plt.xlabel("Time taken ")
plt.ylabel("No. of activities")


a=0
for i in tim:
    a = a + i
a= a/len(tim)
print("Average time is: ", a)
#plt.legend()
#plt.grid(True)
# ax.set_ylim(-2,2)
plt.show()

cv2.destroyAllWindows()
cap.release()

# #INFO: Created TensorFlow Lite XNNPACK delegate for CPU.
# [32, 314, 641, 777, 1029, 1193, 1480, 1902, 2002, 2156, 2561, 2988, 3086, 3276, 3655, 4044, 4159, 4322, 4908, 4926, 5146, 5428, 6049, 6222, 6489] [255, 439, 727, 835, 1166, 1449, 1635, 1967, 2083, 2537, 2814, 3048, 3173, 3652, 3788, 4114, 4262, 4885, 4913, 4941, 5305, 5981, 6051, 6388, 6629]     
# 835 32
# 2083 1193
# 3173 2561
# 4262 3655
# 5305 4908
# [32.12, 35.6, 24.48, 24.28, 15.88]
