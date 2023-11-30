from openai import OpenAI
import os
import pyaudio
import wave
import audioop
import time
from playsound import playsound
client = OpenAI(api_key='sess-AOgh8BnjxIv3XX1JuJm819w3BiXwLI0SpBWACkCB')

def answer(text):
    keywords = ["화장실", "학교", "도서관"]
    for i in keywords:
        if i in text:
            print(i)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            #{"role": "system", "content": "你是一个招待机器人.当有人和你打招呼时,你要进行回应."},
            {"role": "system", "content": "你是一个招待指路机器人.当有人说我要去哪或者寻找什么时,你不需要进行询问,只需要表示你会带领他前往."},
            {"role": "user", "content": text}
        ]
    )
    i = completion.choices[0].message.content
    if i != '':
        print("answer complete")
    return i
    

def voice_to_text():
    audio_file= open("/Users/shiyuhang/Desktop/code/output.wav", "rb")
    transcript = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
    )
    os.remove("/Users/shiyuhang/Desktop/code/output.wav")
    i = transcript.text
    if i != '':
        print('voice to text complete')
    return i

def speak(text):
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text,
    )
    response.stream_to_file("/Users/shiyuhang/Desktop/code/speak_output.mp3")
    print('speak start')
    playsound("/Users/shiyuhang/Desktop/code/speak_output.mp3")
    os.remove("/Users/shiyuhang/Desktop/code/speak_output.mp3")

def record_audio(threshold=500, silence_time=3):
    FORMAT = pyaudio.paInt16  # 数据格式
    CHANNELS = 1              # 单声道
    RATE = 44100              # 采样率
    CHUNK = 1024              # 数据块大小

    audio = pyaudio.PyAudio()

    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    print("Monitoring...")

    frames = []
    recording = False
    start_time = time.time()

    while True:
        data = stream.read(CHUNK)
        rms = audioop.rms(data, 2)

        if rms > threshold:
            if not recording:
                print("Recording started...")
                recording = True
                start_time = time.time()
            frames.append(data)
        elif recording:
            if time.time() - start_time > silence_time:
                print("Recording stopped.")
                break
            else:
                frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    if frames:
        wf = wave.open('/Users/shiyuhang/Desktop/code/output.wav', 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        print("File saved.")
    else:
        print("No audio recorded.")

record_audio()
text1 = voice_to_text()
text2 = answer(text1)
speak(text2)
