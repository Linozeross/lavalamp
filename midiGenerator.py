import mido
import math
import time

def clampBrightness(brightness):
    #clamp brightness to 0.2 - 1
    if brightness < 0.2:
        brightness = 0.2
    
    # scale to 0 - 1
    brightness = (brightness - 0.2) / 0.8
    return brightness


def toCDur(input):
    #3 octaves
    possibleNotes = [0, 2, 4, 5, 7, 9, 11, 12, 14, 16, 17, 19, 21, 23, 24, 26, 28, 29, 31, 33, 35, 36]
    note = math.floor(input * len(possibleNotes))
    return 36 + possibleNotes[note]


#plays a note for 1 second depending on a number between 0 and 1; 
# 0 is low, 1 is high (in a given range) and outputs to stream
def outputNote(stream, input):

    input = clampBrightness(input)

    #convert to C-Dur
    note = toCDur(input)

    grTerz = note + 4
    klTerz = note + 7

    #create a note on message
    on = mido.Message('note_on', note=note, channel=0, velocity=20)
    on2 = mido.Message('note_on', note=grTerz, channel=0, velocity=20)
    on3 = mido.Message('note_on', note=klTerz, channel=0, velocity=20)
    #send the note on message
    stream.send(on)
    stream.send(on2)
    stream.send(on3)

    print(note)

    return [note, grTerz, klTerz]
  
def startNoteOutput(stream):
    #create a note on message
    on = mido.Message('note_on', note=60, velocity=127)
    #send the note on message
    stream.send(on)

def pitchNote(stream, input):
    pitch = int(16000*input - 8000)
    note = 60
    #create a pitchwheel message
    pitch = mido.Message('pitchwheel', pitch=pitch)
    #send the pitchwheel message
    stream.send(pitch)

   
def stopNotes(stream, notes):
    for note in notes:
        #create a note off message
        off = mido.Message('note_off', note=note, velocity=20)
        #send the note off message
        stream.send(off)


def playBase(stream):
    #create a note on message
    note = 39

    on = mido.Message('note_on', note = note, velocity=127, time=0.5, channel=1)
    #send the note on message
    stream.send(on)
    return note


def playDrums(stream, hits):

    note = 30
    notes = []


    for hit in range(hits):
        on = mido.Message('note_on', note = note+hit, velocity=127, time=hit, channel=1)
        #send the note on message
        stream.send(on)
        notes.append(note+hit)
        time.sleep(0.05)

    return notes
   