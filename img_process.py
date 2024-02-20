import cv2

capture = cv2.VideoCapture(0)

while (True):
    ret, frame = capture.read()
    cv2.imgshow('frame', frame)