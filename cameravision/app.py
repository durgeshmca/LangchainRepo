import cv2

cap = cv2.VideoCapture("http://192.168.1.12:8080/video")
while True:
    ret, img = cap.read()
    cv2.imshow('Android_cam', img)
    k = cv2.waitKey(1)
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()