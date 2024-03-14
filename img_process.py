import numpy as np
import cv2 as cv
 
cap = cv.VideoCapture(0, cv.CAP_DSHOW)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    
    ret, frame = cap.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    edged = cv.Canny(gray, 30, 200) 
    cv.waitKey(0)
    contours, hierarchy = cv.findContours(edged,  
    cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE) 
 
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray,(5,5),0)
    ret, thresh_img = cv.threshold(blur,91,255, cv.THRESH_BINARY)

    contours =  cv.findContours(thresh_img,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)[-2]
    contours, hierarchy = cv.findContours(edged,  
    cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE) 
    for c in contours:
        cv.drawContours(frame, [c], -1, (0,255,0), 3)
    
    cv.imshow('frame',frame,edged)
    cv.waitKey(0) 
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()