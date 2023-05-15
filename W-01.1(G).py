from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.config import Config 
from kivy.properties import ObjectProperty
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.snackbar import Snackbar
import speech_recognition as sr
import pyaudio
import pyttsx3
import random as ra
from random import randint
import webbrowser as web
import time

Window.size = (320, 568) #разрешение экрана
Config.set('kivy', 'keyboard_mode', 'systemanddock') #экраная клавиатура

class User:
    user_name = ""
    user_language = ""

class VoiceAssisten:
    sp_language = "" #SPEECH
    re_language = "" #RECOGNITION
    name = ""
    gender = ""

def setup_voice():

    voices = tts.getProperty('voices')

    if VA.sp_language == "ru":
        VA.re_language = "ru-RU"
        if VA.gender == "femail":
            tts.setProperty('voices', voices[0].id)
        else:
            VA.re_language = "en-US"
            tts.setProperty('voices', voices[1].id)                                   #настройки синтезатора речи
            
def speech_play(text_speech):
    tts.say(str(text_speech))
    tts.runAndWait()                        #функция проигрывания фраз    

def zapis_and_analiz():
    data = ""
    with mic:
        rec.adjust_for_ambient_noise(mic, duration=0.5)
        #запись речи
        try:
            print("Слушаю...")
            audio = rec.listen(mic)
        except sr.WaitTimeoutError:
            print("Проверьте микрофон")
            return
        #обработка речи
        try:
            print("Начанаю обработку...")
            data = rec.recognize_google(audio, language="ru")
        except sr.UnknownValueError:
            pass
        return data                              #функция записи и анализа речи

def start_speech(*args: tuple):
    st_sp = ["Привет" + US.user_name + "как ваши дела",
             "Здравствуйте" + US.user_name + "как настроение"]
    speech_play(ra.choice(st_sp))                      #функция приветствия

def finish_speech(*args: tuple):
    fi_sp = ["Пока" + US.user_name + "до новых встреч",
             "До свидания" + US.user_name]
    speech_play(ra.choice(fi_sp))
    tts.stop()
    quit()                     #функция прощания 

def internet_zapros(*args: tuple):

    speech_play("Выполняю поиск")

    zapros = " ".join(args[0])
    web.open('https://www.google.com/search?q=' + zapros)
    speech_play("Вот что было найдено по запросу"+zapros)                   #Поиск в интернете      

def orel_and_reshka(*args: tuple):
    speech_play("Вы играете за орла, а я за решку ")
    y = 'Орёл'
    z = 'Решка'
    number = randint(0, 1)
    if number == 1:
        speech_play("Вы победили, выпал орёл")
    else:
        if number == 0:
            speech_play("Вы победили, выпала решка")                   #игра орел и решка

def go_speech(*args: tuple):
    go_sp = ["Меня зовут W bot и я являюсь голосовым помощником, который умеет осуществлять поиск в интернете, подбрасывать монету и устанавливать таймер",
             "Hi, вы обратились к голосовому помощнику W bot, в функции которого входит поиск по запросу, установка таймера и другое"]
    speech_play(ra.choice(go_sp))

def moduls_start(command_name: str, *args: list):

    for key in commands.keys():
        if command_name in key:
            commands[key](*args)
        else:
            pass    #обработка команд

#Напоминалка и таймер
def timer(*args: tuple):
    speech_play("О чём вам напомнить?")
    text = str(zapis_and_analiz())
    speech_play("Через сколько минут?")
    local_time = int(str(zapis_and_analiz()))
    local_time = local_time * 60
    time.sleep(local_time)
    speech_play(text)

commands = {
    ("Привет", "привет",  "День", "день", "Вечер", "вечер", "Hi", "Здравствуй", "Шалом", "шалом"): start_speech,
    ("стоп", "закончили", "конец", "Стоп", "Закончили", "Конец"): finish_speech,
    ("найди", "скажи", "когда", "почему", "Найди", "Скажи", "Когда", "Почему"): internet_zapros,
    ("Игра", "игра", "Подбрось","Орел", "орел", "Орёл", "орёл"): orel_and_reshka,
    ("Поставь", "Напомни", "Установи"): timer,
    ("Кто", "Что", "Какие"): go_speech,
}

class Container(BoxLayout):

    def say_assisten(self):

        fraza = zapis_and_analiz()
        fraza = fraza.split(" ")
        command = fraza[0]
        command_options = [str(fraza_part) for fraza_part in fraza[1:len(fraza)]]
        moduls_start(command, command_options)


class MyApp(MDApp):
    def build(self):
        return Container()

    def callback(self, button):
        Snackbar(text = "Доступные функции:").open()


if __name__ == '__main__':

    rec = sr.Recognizer()
    mic = sr.Microphone()
    tts = pyttsx3.init()

    VA = VoiceAssisten()
    VA.gender = "femail"
    VA.name = "NeitrotonBot"
    VA.sp_language = "ru"

    US = User()
    US.user_name = "Человек"

    setup_voice()

    MyApp().run()
