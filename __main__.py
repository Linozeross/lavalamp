
# import opencv
import cv2
import numpy as np
import mido 
import camFeatureExtractor as cfe
import midiGenerator as mg

print("Welcome to the lavalamp 💡!")


print(mido.get_output_names())
#create a new output stream
outport = mido.open_output('IAC-Treiber lavalamp')


cap = cv2.VideoCapture(0)

while(True):
    ret, frame = cap.read()

    # Extract the brightness
    brightness = cfe.extractNormalizedBrightness(frame)
    print("Brightness: {}".format(brightness))
    mg.outputNote(outport, brightness)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



#close the output stream
outport.close()
cap.release()
cv2.destroyAllWindows()



