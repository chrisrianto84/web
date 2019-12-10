def overwrite(filename, strChord):
    import os
    file = open(filename, 'w')
    file.write(strChord)
    file.close

def overwriteUserInput(filename, strings):
    import os
    file = open(filename,'w')
    file.write(strings)
    file.close

def giveLabelsUserInput(filename):
    import os
    file = open(filename, "r")

    countArray=0
    strings = ""
    for line in file:
        strings = strings + line.replace("\n")
        countArray=countArray+1

    file.close
    overwriteUserInput(filename, strings)

def giveLabels(filename, chords):
    import os
    file = open(filename, "r")

    countArray=0
    strChord = ""
    for line in file:
        strChord = strChord + line.replace("\n"," "+ chords[countArray] + "\n")
        countArray=countArray+1

    file.close
    overwrite(filename, strChord)

def load_with_librosa_timed(data,start,end):
    import librosa
    import IPython.display as ipd

    x, sr = librosa.load(data,offset=start,duration=end-start, mono=True)

    ipd.Audio(x,rate=sr)


# load_with_librosa_timed("backend/train/raw/backC-D.wav", 0.7894784580498866, 1.6253968253968254)
# chords=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p"]
# giveLabels("backend/train/beat/138281933752428585295472828699521897438.wav.txt",chords)