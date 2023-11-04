import mido
import time


#plays a note for 1 second depending on a number between 0 and 1; 
# 0 is low, 1 is high (in a given range) and outputs to stream
def outputNote(stream, input):

    note = int(100*input)
    print(note)
    #create a note on message
    on = mido.Message('note_on', note=note)
    #create a note off message
    off = mido.Message('note_off', note=note)
    #send the note on message
    stream.send(on)
    #wait for the given amount of time
    time.sleep(0.1)
    #send the note off message
    stream.send(off)
    #close the output stream
  