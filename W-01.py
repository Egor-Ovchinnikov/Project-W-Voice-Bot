import speech_recognition as sr
import pyaudio
import pyttsx3
import random as ra
import webbrowser as web

class User:
    user_name = ""
    user_language = ""

class VoiceAssisten:
    sp_language = "" #SPEECH
    re_language = "" #RECOGNITION
    name = ""
    gender = ""
    
#настройки синтезатора речи
def setup_voice():

    voices = tts.getProperty('voices')

    if VA.sp_language == "ru":
        VA.re_language = "ru-RU"
        if VA.gender == "femail":
            tts.setProperty('voices', voices[0].id)
        else:
            VA.re_language = "en-US"
            tts.setProperty('voices', voices[1].id)  
            
#функция проигрывания фраз            
def speech_play(text_speech):
    tts.say(str(text_speech))
    tts.runAndWait()      
    
#функция записи и анализа речи    
def zapis_and_analiz():
    data = ""
    with mic:
        rec.adjust_for_ambient_noise(mic, duration=0.5)
        #запись речи
        try:
            print("Слушаю...")
            audio = rec.listen(mic)
        except sr.WaitTimeoutError:
            #print("Проверьте микрофон")
            return
        #обработка речи
        try:
            print("Начанаю обработку...")
            data = rec.recognize_google(audio, language="ru")
        except sr.UnknownValueError:
            pass
        return data 
      
#функция приветствия
def start_speech(*args: tuple):
    st_sp = ["Привет" + US.user_name + "как ваши дела",
             "Здравствуйте" + US.user_name + "как настроение"]
    speech_play(ra.choice(st_sp))     
    
#функция прощания    
def finish_speech(*args: tuple):
    fi_sp = ["Пока" + US.user_name + "до новых встреч",
             "До свидания" + US.user_name]
    speech_play(ra.choice(fi_sp))
    tts.stop()
    quit()        
    
#Поиск в интернете
def internet_zapros(*args: tuple):

    speech_play("Выполняю поиск")

    zapros = " ".join(args[0])
    web.open('https://www.google.com/search?q=' + zapros)
    speech_play("Вот что было найдено по запросу"+zapros)          
    
#обработка команд
def moduls_start(command_name: str, *args: list):

    for key in commands.keys():
        if command_name in key:
            commands[key](*args)
        else:
            pass    

commands = {
    ("Привет", "день", "вечер", "Hi", "Здравствуй"): start_speech,
    ("стоп", "закончили", "конец"): finish_speech,
    ("найди", "скажи", "когда", "Почему"): internet_zapros,
}

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
    
    while True:
        fraza = zapis_and_analiz()
        print(fraza)
        self.fraza_label.text = fraza
        fraza = fraza.split(" ")
        command = fraza[0]
        command_options = [str(fraza_part) for fraza_part in fraza[1:len(fraza)]]
        moduls_start(command, command_options)
