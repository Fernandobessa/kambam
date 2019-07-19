import cv2
import numpy as np

def nothing(x):
    # any operation
    pass

cap = cv2.VideoCapture(0)

#cv2.namedWindow("Trackbars")
#cv2.createTrackbar("L-H", "Trackbars", 0, 180, nothing)
#cv2.createTrackbar("L-S", "Trackbars", 66, 255, nothing)
#cv2.createTrackbar("L-V", "Trackbars", 134, 255, nothing)
#cv2.createTrackbar("U-H", "Trackbars", 180, 180, nothing)
#cv2.createTrackbar("U-S", "Trackbars", 255, 255, nothing)
#cv2.createTrackbar("U-V", "Trackbars", 243, 255, nothing)



font = cv2.FONT_HERSHEY_COMPLEX



_, frame = cap.read()    
toDo = cv2.selectROI(frame)
Doing = cv2.selectROI(frame)
Done = cv2.selectROI(frame)





while True:
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    cv2.rectangle(frame,(toDo[0],toDo[1]),(toDo[2]+toDo[0],toDo[3]+toDo[1]),(0,255,0),3)
    cv2.putText(frame, "To do", (toDo[0], toDo[1]), font, 1, (0, 0, 0))
    
    cv2.rectangle(frame,(Doing[0],Doing[1]),(Doing[2]+Doing[0],Doing[3]+Doing[1]),(0,255,0),3)
    cv2.putText(frame, "Doing", (Doing[0], Doing[1]), font, 1, (0, 0, 0))
    
    cv2.rectangle(frame,(Done[0],Done[1]),(Done[2]+Done[0],Done[3]+Done[1]),(0,255,0),3)
    cv2.putText(frame, "Done", (Done[0], Done[1]), font, 1, (0, 0, 0))
    
    #print (toDo[0],toDo[1])
    #print (toDo[2]+toDo[0],toDo[3]+toDo[1])
    #print('--------------------#------------------------------------#---------------------------')
    #l_h = cv2.getTrackbarPos("L-H", "Trackbars")
    #l_s = cv2.getTrackbarPos("L-S", "Trackbars")
    #l_v = cv2.getTrackbarPos("L-V", "Trackbars")
    #u_h = cv2.getTrackbarPos("U-H", "Trackbars")
    #u_s = cv2.getTrackbarPos("U-S", "Trackbars")
    #u_v = cv2.getTrackbarPos("U-V", "Trackbars")

    lower_blue = np.array([38, 86, 0])
    upper_blue = np.array([121, 255, 255])

    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
    
    lower_black = np.array([0,0,0])
    upper_black = np.array([100, 100, 100 ]) 
    
    black_mask = cv2.inRange(hsv, lower_black, upper_black)
    
    kernel = np.ones((5, 5), np.uint8)
    
    mask = blue_mask
    mask = cv2.erode(mask, kernel)
    

    # Contours detection
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
     
    for cnt in contours:
        rc = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rc)
        area = cv2.contourArea(cnt)
        approx = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True)
        x = approx.ravel()[0]
        y = approx.ravel()[1]
    for p in box:
            pt = (p[0],p[1])
            #print (pt)
            cv2.circle(frame,pt,5,(200,0,0),2) 
    if( (pt[0]>toDo[0]) and (pt[0]< toDo[2]+toDo[0])):
        print('Todo')   
    if( (pt[0]>Doing[0]) and (pt[0]< Doing[2]+Doing[0])):
        print('Doing') 
    if( (pt[0]>Done[0]) and (pt[0]< Done[2]+Done[0])):
        print('Done')     


        #print (approx.ravel())
        
        #if area > 3000:
            #cv2.drawContours(frame, [approx], 0, (0, 0, 0), 5)

         #   if len(approx) == 3:
          #      cv2.putText(frame, "Triangle", (x, y), font, 1, (0, 0, 0))
          #  elif len(approx) == 4:
           #     cv2.putText(frame, "Rectangle", (x, y), font, 1, (0, 0, 0))
            #elif 10 < len(approx) < 20:
             #   cv2.putText(frame, "Circle", (x, y), font, 1, (0, 0, 0))
    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()