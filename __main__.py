
# import opencv
import cv2
import numpy as np
import mido 
import camFeatureExtractor as cfe
import midiGenerator as mg
import time

BPM = 60

print("Welcome to the lavalamp 💡!")

#print(mido.get_output_names())
#create a new output stream

outports = []

for port in mido.get_output_names():
    print(port)
    outports.append(mido.open_output(port))


sleepTime = 60.0/BPM




cap = cv2.VideoCapture(0)

#change resolution to 320x240
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)


#mg.startNoteOutput(outport)


# get current timestamp
lastTimeStamp = time.time()
print(lastTimeStamp)

lastNotes = None
lastBaseNote = None

minBrightness = None
maxBrightness = None

counter = 0






while(True):

    #if it's been long enough since the last note, play a new one
    
    timeJump = time.time() - lastTimeStamp
    if timeJump > sleepTime:
        
        counter += 1
        counter = counter % 2
        print(counter)

        ret, frame = cap.read()
        # Extract the brightness
        brightness = cfe.extractNormalizedBrightness(frame)

        if minBrightness is None or brightness < minBrightness:
            minBrightness = brightness
    
        if maxBrightness is None or brightness > maxBrightness:
            maxBrightness = brightness

        print("Brightness: {}; Min: {}; Max: {}".format(brightness, minBrightness, maxBrightness))


        if lastNotes is not None:
            mg.stopNotes(outports[0], lastNotes)
        
        lastNotes = mg.outputNote(outports[0], brightness)
        


        # #Base on 1
        # if counter == 0:
        #     if lastBaseNote is not None:
        #         mg.stopNote(outports[0], lastBaseNote)

        #     lastBaseNote = mg.playBase(outports[0])
        #     #mg.startNoteOutput(outport)
        
        
        
        lastTimeStamp = time.time()
        print(round((time.time() - lastTimeStamp) - sleepTime), 4)

   
    #mg.outputNote(outport, brightness)

    #mg.pitchNote(outport, brightness)


#close the output stream
for outport in outports:
    outport.close()
cap.release()
cv2.destroyAllWindows()



