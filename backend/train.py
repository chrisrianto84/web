import librosa

def trimSilence(x):
    x, index = librosa.effects.trim(x)
    return x, index

def librosaLoad(filename):
    x, sr = librosa.load(filename, mono=True)
    x, index = trimSilence(x)
    return x, sr, index

def librosaBeatTempo(x, sr):
    tempo, beats = librosa.beat.beat_track(x, sr=sr, start_bpm=60, units='time') 
    return tempo, beats

#Make txt based on Onset time
#==param==
#   code = 1 for wav and 2 for mp3
def getOnset(code):
    import os
    from backend.labelling import giveLabels

    path = 'app/static/user_input/input_audio/'
    print(path)
    files=[]
    for r, d, f in os.walk(path):
        #code 1 = .wav
        #code 2 = .mp3
        for file in f:
            if code == 1:
                if '.wav' in file:
                    print(file)
                    files.append(file)
            elif code == 2:
                if '.mp3' in file:
                    files.append(file)

    for i in files:
        print(i)

    print("Making beat .txt ")
    for filename in files:
        x, sr, index = librosaLoad(path+filename)
        #get tempo and beat
        tempo, beats = librosaBeatTempo(x, sr)

        pathBeat = 'app/static/user_input/beats/'
        tempoFile = open(pathBeat+filename+".txt", "w")
        
        beats[0]=0.0
        stringBeat = ""
        count=1
        index = 0
        for i in beats:
            # if count == 1:
            #     stringBeat = stringBeat+"0.0 "
            if count%2 == 1:
                if count != 1:
                    dataTemp = beats[index-1] + 60/tempo
                    stringBeat = stringBeat+str(dataTemp)+" "
                else:
                    stringBeat = stringBeat + str(i)+" "
            elif count%2 == 0:
                stringBeat = stringBeat+str(i)+"\n"
            count=count+1
            index = index + 1

        tempoFile.write(stringBeat)        
        tempoFile.close
        
