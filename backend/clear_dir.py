import os

def initiate_clear():
    beats_path = 'app/static/user_input/beats/'
    mfccs_path = 'app/static/user_input/input_mfccs/'
    audio_path = 'app/static/user_input/input_audio/'

    files = []
    
    print('Deleting beats...')
    for beats in os.listdir(beats_path):
        os.remove(beats_path+beats)
    
    print('Deleting MFCCs...')
    for mfccs in os.listdir(mfccs_path):
        os.remove(mfccs_path+mfccs)
    
    print('Deleting Audios...')
    for audio in os.listdir(audio_path):
        os.remove(audio_path+audio)
    
    print('Clear Memory Done :D')