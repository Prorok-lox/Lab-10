import json, time

import pyttsx3, pyaudio, vosk

import requests
from random import randint
from PIL import Image


class Speech:
    def __init__(self):
        self.speaker = 0
        self.tts = pyttsx3.init('sapi5')

    def set_voice(self, speaker):
        self.voices = self.tts.getProperty('voices')
        for count, voice in enumerate(self.voices):
            if count == 0:
                print('0')
                id = voice.id
            if speaker == count:
                id = voice.id
        return id

    def text2voice(self, speaker=0, text='Готов'):
        self.tts.setProperty('voice', self.set_voice(speaker))
        self.tts.say(text)
        self.tts.runAndWait()


class Recognize:
    def __init__(self):
        model = vosk.Model('vosk-model-small-ru-0.4')
        self.record = vosk.KaldiRecognizer(model, 16000)
        self.stream()

    def stream(self):
        pa = pyaudio.PyAudio()
        self.stream = pa.open(format=pyaudio.paInt16,
                              channels=1,
                              rate=16000,
                              input=True,
                              frames_per_buffer=8000)

    def listen(self):
        while True:
            data = self.stream.read(4000, exception_on_overflow=False)
            if self.record.AcceptWaveform(data) and len(data) > 0:
                answer = json.loads(self.record.Result())
                if answer['text']:
                    yield answer['text']


def speak(text):
    speech = Speech()
    speech.text2voice(speaker=1, text=text)


def rand():
    url = f"https://rickandmortyapi.com/api/character/{randint(1, 108)}"
    resp = requests.get(url).json()
    name = resp['name']
    return name


def download():
    global image_counter
    url = f"https://rickandmortyapi.com/api/character/{randint(1, 108)}"
    resp = requests.get(url).json()
    path = resp['image']
    data = requests.get(path).content
    with open(f'image{image_counter}.jpeg', 'wb') as f:
        f.write(data)
        f.close()
    image_counter += 1


def episode():
    url = f"https://rickandmortyapi.com/api/character/{randint(1, 108)}"
    resp = requests.get(url).json()
    name = resp['name']
    ep = requests.get(resp['episode'][0]).json()
    title = ep['name']
    return f"{name} first appearance was in episode \"{title}\""


def show_image():
    global image_counter
    download()
    image = Image.open(f'image{image_counter - 1}.jpeg')
    image.show()


def resolution():
    global image_counter
    download()
    image = Image.open(f'image{image_counter - 1}.jpeg')
    w, h = image.size
    return f'Resolution of image{image_counter - 1}.jpeg is {w} pixels by {h} pixels'


image_counter = 0
rec = Recognize()
text_gen = rec.listen()
rec.stream.stop_stream()
speak('Starting')
time.sleep(0.5)
rec.stream.start_stream()
for text in text_gen:
    if text == 'закрыть':
        speak('So long, ichthyander.')
        quit()
    elif text == 'случайный':
        speak(rand())
    elif text == 'сохранить':
        download()
        speak('Successfully downloaded picture of random character to image.jpeg file')
    elif text == 'эпизод':
        speak(episode())
    elif text == 'показать':
        speak('Now I show you the picture of random character')
        show_image()
    elif text == 'разрешение':
        speak(resolution())
    else:
        speak('Sorry, I don\'t know this command')
        print(text)
