import json
import pyaudio
import requests
import vosk
import cv2
import random

character_number = str(random.randint(1, 800))
# print('https://rickandmortyapi.com/api/character/' + character_number)
model = vosk.Model('vosk-model-small-ru-0.22')
web = 'https://rickandmortyapi.com/api/character/' + character_number
response = requests.get(web)
data = json.loads(response.content)

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
    p = requests.get(image_url)
    out = open('img.jpeg', 'wb')
    out.write(p.content)
    out.close()
    print('Ваш персонаж сохранен')


def get_image():
    image_url = response.json()['image']
    p = requests.get(image_url)
    out = open('img.jpegg', 'wb')
    out.write(p.content)
    out.close()
    print('Ваш персонаж готов')
    img = cv2.imread('img.jpeg')
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def get_name():
    name = response.json()["name"]
    print('Имя вашего персонажа:', name)


def get_episode():
    episode1 = str(response.json()["episode"])[42:-2]
    print('Эпизод где встречался этот персонаж:', episode1)


def get_image_resolution():
    img = cv2.imread('img.jpeg')
    width, height, _ = img.shape
    resolution = str(width) + " x " + str(height)
    print(resolution)


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
        break
    else:
        print('Не удалось распознать команду')