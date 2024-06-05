import json
import pyaudio
import requests
import vosk
import cv2
import random
import pyttsx3


character_number = str(random.randint(1, 800))
# print('https://rickandmortyapi.com/api/character/' + character_number)
model = vosk.Model('vosk-model-small-ru-0.22')
web = 'https://rickandmortyapi.com/api/character/' + character_number
response = requests.get(web)
data = json.loads(response.content)


engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


record = vosk.KaldiRecognizer(model, 16000)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=16000)
stream.start_stream()


def listen():
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if record.AcceptWaveform(data) and len(data) > 0:
            answer = json.loads(record.Result())
            if answer['text']:
                yield answer['text']


def save_image():
    image_url = response.json()['image']
    out = open('img.jpeg', 'wb')
    out.write(requests.get(image_url).content)
    out.close()
    engine.say('g Ваш персонаж сохранен')
    engine.runAndWait()


def get_image():
    image_url = response.json()['image']
    out = open('img.jpeg', 'wb')
    out.write(requests.get(image_url).content)
    out.close()
    engine.say('g Ваш персонаж готов')
    engine.runAndWait()
    img = cv2.imread('img.jpeg')
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def get_name():
    name = response.json()["name"]
    engine.say(f'g Имя вашего персонажа: {name}')
    engine.runAndWait()


def get_episode():
    episode1 = str(response.json()["episode"])[42:-2]
    engine.say(f'g Эпизод где встречался этот персонаж: {episode1}')
    engine.runAndWait()


def get_image_resolution():
    img = cv2.imread('img.jpeg')
    width, height, _ = img.shape
    resolution = str(width) + " x " + str(height)
    resolution = resolution.replace('x', 'на')
    engine.say(f'g Разрешение вашей картинки {resolution}')
    engine.runAndWait()


for text in listen():
    if 'показать' in text:
        get_image()
    elif 'сохранить' in text:
        save_image()
    elif 'имя' in text:
        get_name()
    elif 'эпизод' in text:
        get_episode()
    elif 'разрешение' in text:
        get_image_resolution()
    elif 'выход' in text:
        engine.say(f'g До свидания ')
        engine.runAndWait()
        break
    else:
        engine.say('g Не удалось распознать команду')
        engine.runAndWait()
