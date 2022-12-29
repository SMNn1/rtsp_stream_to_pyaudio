import pyaudio
import subprocess
from array import array
from datetime import datetime
import wave

#ffmpeg config and pipe
command = ['ffmpeg', '-i', 'rtsp://USERNAME:PASSWORD@IP_ADDRESS:PORT/stream1', '-vn', '-f', 's16le', '-']
ffmpeg = subprocess.Popen(command, stdout=subprocess.PIPE)

if __name__ == "__main__":
    audio_format=pyaudio.paInt16
    audio_channels=1
    audio_rate=8000
    audio_chunk=1024
    record_time=10
    noise_trigger = 1000
    audio=pyaudio.PyAudio()

    while True:
        #file name and preparation
        dt = datetime.now()
        timestamp = str(dt.strftime('%Y_%m_%d-%H%M%S'))
        file_name = "rec_" + timestamp + ".wav"
        wavfile=wave.open(file_name,'wb')
        wavfile.setnchannels(audio_channels)
        wavfile.setsampwidth(audio.get_sample_size(audio_format))
        wavfile.setframerate(audio_rate)
        #reading datastream and calculating volume
        data=ffmpeg.stdout.read(audio_chunk)
        data_chunk=array('h',data)
        vol=max(data_chunk)
        frames = []
        if(vol>= noise_trigger):
            print("noise level triggered with: %s" % vol)
            for i in range(0,int(audio_rate/audio_chunk*record_time)):
                data=ffmpeg.stdout.read(audio_chunk)
                frames.append(data)
            #appending frames to file
            wavfile.writeframes(b''.join(frames))
            wavfile.close()
            print("recording saved as %s" % file_name)
        else:
            print("vol level: %s " % vol)
