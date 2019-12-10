import pyaudio
import sys
sys.path.append('/Users/chris/Desktop/web/')
from app_settings import settings

r = settings.get_redis_config()

def audio():
    import wave
    # start Recording
    import pyaudio
    import time
    import wave

    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    CHUNK = 1024
    # RECORD_SECONDS = 5
    
    file_path = "app/static/user_input/input_audio/"

    ids = r.get("session_id:")
    r.set('input_file:', ids+'.wav')
    print('a')
    WAVE_OUTPUT_FILENAME = file_path + ids + ".wav"
    print(WAVE_OUTPUT_FILENAME)
    print('a')
    audio = pyaudio.PyAudio()

    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
    rate=RATE, input=True,
    frames_per_buffer=CHUNK)
    print ("recording...")
    frames = []

    try:
        while True:
            data = stream.read(CHUNK)
            frames.append(data)
    except KeyboardInterrupt:
        print('Finished Recording')


    # for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    #     data = stream.read(CHUNK)
    #     frames.append(data)
    # print ("finished recording")


    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()

    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

    # print(WAVE_OUTPUT_FILENAME)
    # r.set('input_file:',WAVE_OUTPUT_FILENAME)
    return ids+'.wav'

name = audio()
