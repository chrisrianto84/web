from app_settings import settings
r = settings.get_redis_config()

def overwrite(filename, strChord):
    import os
    file = open(filename, 'w')
    file.write(strChord)
    file.close

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
    x, sr = librosa.load(data,offset=start,duration=end-start, mono=True)
    return x,sr

def make_mfcc(data, start_time, end_time, path, name):
    import numpy as np
    import librosa, librosa.display
    import sklearn
    import matplotlib.pyplot as plt
    x, sr = load_with_librosa_timed(data, start_time, end_time)
#     mfccs = librosa.feature.mfcc(x, sr=sr)
    
#     mfccs = sklearn.preprocessing.normalize(mfccs)
#     mfccs = sklearn.preprocessing.scale(mfccs, axis=1)
    print('c')
    print(start_time)
    print(end_time)
    print('c')
    chromagram = librosa.feature.chroma_cqt(x, sr=sr, hop_length=512)
    chromagram = librosa.decompose.nn_filter(chromagram, aggregate=np.average)
#     chromagram_preprocessing = sklearn.preprocessing.normalize(chromagram)
#     chromagram_preprocessing = sklearn.preprocessing.scale(chromagram, axis=1)
    
    path_full_name = path+name
#     mfccs = librosa.display.specshow(mfccs)
    chromagram = librosa.display.specshow(chromagram, y_axis='chroma')
#     plt.gray()
    plt.savefig(path_full_name,dpi=46)
    return chromagram

def make_df(filename):
    import pandas as pd
    from backend import train

    plt_path = "app/static/user_input/input_mfccs/"

    train.getOnset()

    dataPath = "app/static/user_input/beats/"+filename+".txt"
    print(dataPath)
    my_cols = ["start", "end"]
    df_data = pd.read_csv(dataPath,
                        sep="\s",
                        names=my_cols, 
                        header=None, 
                        engine="python")
    df_data = df_data[:-1]
    print(df_data)
    return df_data, plt_path

def make_visualization():
    filename=r.get('input_file:')
    df_data, plt_path = make_df(filename)
    data = 'app/static/user_input/input_audio/'+filename
    i = len(df_data)
    for j in range(i):
        mfccs = make_mfcc(data, df_data.loc[j, "start"], df_data.loc[j, "end"], plt_path, str(j)+".png")
    print("complete!")    

