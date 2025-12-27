import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
import pyttsx3
import requests
import webbrowser
import pyjokes
import os
from datetime import datetime

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def record_audio(duration=5, fs=44100, filename="input.wav"):
    print("Listening...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    wav.write(filename, fs, audio)
    return filename

def recognize_speech(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio_data = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio_data)
        print(f"You said: {text}")
        return text.lower()
    except sr.UnknownValueError:
        return "error: Could not understand"
    except sr.RequestError:
        return "error: API failure"

def get_weather(city):
    API_KEY = "211553a70acef1c96679640b66fc473b"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        return f"The temperature in {city} is {temp}°C with {desc}."
    else:
        return "Sorry, I couldn’t fetch the weather."

def process_command(command):
    if "weather" in command:
        speak("Which city?")
        filename = record_audio()
        city = recognize_speech(filename)
        if "error" in city:
            return "Couldn't understand the city name."
        return get_weather(city)

    elif "time" in command:
        now = datetime.now().strftime("%H:%M")
        return f"The time is {now}."

    elif "joke" in command:
        return pyjokes.get_joke()

    elif "youtube" in command:
        webbrowser.open("https://youtube.com")
        return "Opening YouTube."

    elif "music" in command:
        try:
            os.startfile("spotify")
            return "Playing music."
        except:
            return "Could not open Spotify."

    else:
        return "Sorry, I don't know how to handle that yet."

def main():
    speak("Hello, I am Jarvis. What can I do for you?")
    filename = record_audio()
    command = recognize_speech(filename)

    if "error" in command:
        speak("Sorry, I couldn't understand you.")
    else:
        response = process_command(command)
        print(f"Jarvis: {response}")
        speak(response)

if __name__ == "__main__":
    main()
