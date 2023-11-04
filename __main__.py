
# import opencv
import cv2
import numpy as np
import camFeatureExtractor as cfe

print("Welcome to the lavalamp 💡!")

cap = cv2.VideoCapture(0)

while(True):
    ret, frame = cap.read()

    # Extract the brightness
    brightness = cfe.extractNormalizedBrightness(frame)
    print("Brightness: {}".format(brightness))

    cv2.imshow('frame',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()



