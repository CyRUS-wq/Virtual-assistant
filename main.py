import speech_recognition as srec
import webbrowser
import pyttsx3  # for text to speech
import musiclib
import requests
import client
from openai import OpenAI

recognizer = srec.Recognizer()
engine = pyttsx3.init()
news_api = "key"

def speak(text):
    engine.say(text)
    engine.runAndWait()

def aiProcess(command):
    client = OpenAI(
    api_key="key",
)
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a voice assistant."},
        {
            "role": "user",
            "content": "what is one piece."
        }
    ]
)


def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
        print("Opening Google...")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
        print("Opening Youtube...")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musiclib.music[song]
        webbrowser.open(link)
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/everything?q=Apple&from=2024-09-14&sortBy=popularity&apiKey={news_api}")
        if r.status_code == 200:
            # Parsing the json response
            data = r.json()

            # Extracting the articles
            articles = data.get('articles', [])
            
            for article in articles:
                speak(article['title'])
        else:
            speak("I couldn't fetch the news. Please try again later.")

    else:
        #using OpenAI's API 
        output = aiProcess(c)
        speak(output)

if __name__ == "__main__":
    speak("Initializing Assistant....")
  
    while True:
        recognizer = srec.Recognizer()
        print("Recognizing...")
        # Listening for a wakeup call ->"jarvis" or you can use whatever call you want.
        try:
            with srec.Microphone() as source:
                print("Listening...")
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=5)
                recognizer.energy_threshold = 30
            word = recognizer.recognize_google(audio)
            if word.lower() == "jarvis": # or you can use whatever call you want, Just replace it.
                speak("Yes")
                print("Activated...")
                # Listen for command
                with srec.Microphone() as source:  # obtaining audio from microphone
                    print("Listening for command...")
                    command_audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    command = recognizer.recognize_google(command_audio)

                    print(f"Command: {command}")
                    processCommand(command)

        except Exception as e:
            print(f"Error: {e}")
