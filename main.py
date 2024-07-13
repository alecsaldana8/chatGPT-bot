import speech_recognition as sr
import openai
from gtts import gTTS
import os
from playsound import playsound

openai.api_key = 'sk-proj-VCNcn65TdSQtGdA90FdZT3BlbkFJl5hGPU7gbjd4UVjziaGz'

def process_input(input_text):
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo-16k',
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": input_text},
        ]
    )
    return response['choices'][0]['message']['content'].strip()

r = sr.Recognizer()

first_run = True

while True:
    with sr.Microphone() as source:
        if first_run:
            tts = gTTS(text='Hello, Ace is listening, ask a question', lang='en')
            tts.save("listening.mp3")
            playsound("listening.mp3")
            os.remove("listening.mp3")
            first_run = False 

        try:
            audio = r.listen(source, timeout=10)
        except sr.WaitTimeoutError:
            tts = gTTS(text='Goodbye!', lang='en')
            tts.save("goodbye.mp3")
            playsound("goodbye.mp3")
            os.remove("goodbye.mp3")
            break

    try:
        user_input = r.recognize_google(audio)
    except sr.UnknownValueError:
        tts = gTTS(text='Sorry, I did not understand that. Goodbye!', lang='en')
        tts.save("sorry.mp3")
        playsound("sorry.mp3")
        os.remove("sorry.mp3")
        break

    print(user_input)

    if user_input.lower() in ['stop', 'no', 'no thank you', 'nope']:
        tts = gTTS(text='Okay, Goodbye!', lang='en')
        tts.save("goodbye.mp3")
        playsound("goodbye.mp3")
        os.remove("goodbye.mp3")
        break

    response_text = process_input(user_input)
    print('Ace: ' + response_text)

    tts = gTTS(text=response_text, lang='en')
    tts.save("response.mp3")
    playsound("response.mp3")
    os.remove("response.mp3")

    tts = gTTS(text='Do you have any other questions?', lang='en')
    tts.save("anything_else.mp3")
    playsound("anything_else.mp3")
    os.remove("anything_else.mp3")
