import tkinter as tk
import threading
import math
import datetime
import os
import webbrowser
import pyttsx3
import speech_recognition as sr
import wikipedia
import requests

# -------------------- Gemini API --------------------
GEMINI_API_KEY = "AIzaSyCLoJzQ3jokNXjZKfmpig64BGSiXLkCvok"  # Replace with your actual key

def ask_gemini(question):
    """Send question to Gemini API and get response"""
    url = "https://api.gemini.com/v1/ask"  # Example endpoint, replace with actual Gemini API endpoint
    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": question,
        "max_tokens": 150
    }
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()
        return result.get("answer", "I couldn't get an answer from Gemini.")
    except Exception as e:
        return f"Error contacting Gemini API: {e}"

# -------------------- Voice Engine --------------------
engine = pyttsx3.init()
engine.setProperty('rate', 160)

def speak(message: str):
    """Speak and show message on GUI"""
    main_window.after(0, lambda: status_label.config(text=message))
    engine.say(message)
    engine.runAndWait()

# -------------------- Voice Recognition --------------------
recognizer = sr.Recognizer()

def listen():
    """Listen for wake word and commands"""
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language='en-IN')
        return text.lower()
    except:
        return ""

# -------------------- Assistant Commands --------------------
def handle_command(command):
    if "wikipedia" in command:
        speak("Searching Wikipedia...")
        topic = command.replace("wikipedia", "").strip()
        try:
            result = wikipedia.summary(topic, sentences=2)
            speak(result)
        except:
            speak("I could not find anything.")
    elif "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://google.com")
    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")
    elif "open instagram" in command:
        speak("Opening Instagram")
        webbrowser.open("https://instagram.com")
    elif "open notepad" in command:
        speak("Opening Notepad")
        os.system("notepad")
    elif "open calculator" in command:
        speak("Opening Calculator")
        os.system("calc")
    elif "exit" in command or "stop" in command:
        speak("Goodbye! Shutting down...")
        main_window.after(1000, main_window.destroy)
    else:
        # Fallback: ask Gemini API
        speak("Let me check that...")
        answer = ask_gemini(command)
        speak(answer)

# -------------------- Background Listening --------------------
def assistant_loop():
    while True:
        text = listen()
        if "hey jarvis" in text:  # Wake word
            speak("Yes, I am listening...")
            command = listen()
            if command:
                handle_command(command)

# -------------------- GUI Animation --------------------
angle = 0

def animate_circle():
    global angle
    canvas.delete("pulse")
    radius = 80 + 10 * math.sin(angle)
    canvas.create_oval(
        200 - radius, 200 - radius, 200 + radius, 200 + radius,
        outline="#00f6ff", width=4, tags="pulse"
    )
    angle += 0.15
    main_window.after(50, animate_circle)

# -------------------- GUI Setup --------------------
main_window = tk.Tk()
main_window.title("Jarvis - Personal Assistant")
main_window.geometry("400x500")
main_window.configure(bg="black")
main_window.resizable(False, False)

canvas = tk.Canvas(main_window, width=400, height=400, bg="black", highlightthickness=0)
canvas.pack()

status_label = tk.Label(
    main_window,
    text="Initializing...",
    fg="#00f6ff",
    bg="black",
    font=("Consolas", 12)
)
status_label.pack(pady=10)

# -------------------- Greeting --------------------
def greet_user():
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good morning")
    elif hour < 18:
        speak("Good afternoon")
    else:
        speak("Good evening")
    speak("I am Jarvis, your personal assistant. Say 'Hey Jarvis' to activate me.")

# -------------------- Launch Assistant --------------------
main_window.after(500, animate_circle)
main_window.after(1000, greet_user)
threading.Thread(target=assistant_loop, daemon=True).start()
main_window.mainloop()
