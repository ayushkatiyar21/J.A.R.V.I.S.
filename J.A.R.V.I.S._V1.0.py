import google.generativeai as genai
import os
import speech_recognition as sr
import pyttsx3
import pyautogui  # For taking screenshots
import webbrowser  # For opening websites and searching
from datetime import datetime
import pytz  # For timezone support
import pywhatkit  # For playing YouTube videos

# Set your Gemini API Key
os.environ["GEMINI_API_KEY"] = "AIzaSyDKCZhHIdBN8yYaiNLw1sLPOMIo-Ag2A9g"
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Capture and recognize full sentence input."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Calibrating microphone for ambient noise...")
        recognizer.adjust_for_ambient_noise(source, duration=2)  # Calibrate noise threshold
        print("Listening... Please speak clearly.")
        try:
            # Increase timeout and phrase_time_limit for capturing full sentences
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
            query = recognizer.recognize_google(audio)
            print(f"You said: {query}")
            return query
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand the audio.")
            return "Sorry, I didn't catch that."
        except sr.RequestError:
            print("There was an issue with the recognition service.")
            return "There was an issue with the recognition service."

def take_screenshot():
    """Take a screenshot and save it."""
    try:
        screenshot = pyautogui.screenshot()
        file_path = "screenshot.png"  # Change the file path as needed
        screenshot.save(file_path)
        print(f"Screenshot saved as {file_path}")
        speak("Screenshot taken and saved.")
    except Exception as e:
        print(f"Error taking screenshot: {e}")
        speak("I encountered an error while taking the screenshot.")

def tell_time():
    """Tell the current time in India."""
    try:
        india_timezone = pytz.timezone("Asia/Kolkata")
        india_time = datetime.now(india_timezone).strftime("%I:%M %p")
        print(f"The current time in India is {india_time}")
        speak(f"The current time in India is {india_time}")
    except Exception as e:
        print(f"Error fetching time: {e}")
        speak("I couldn't fetch the current time.")

def open_website(website):
    """Open a specified website."""
    try:
        url = f"https://{website}" if not website.startswith("http") else website
        webbrowser.open(url)
        print(f"Opening {url}")
        speak(f"Opening {website}")
    except Exception as e:
        print(f"Error opening website: {e}")
        speak("I couldn't open the website.")

def google_search(query):
    """Search Google for a query."""
    try:
        search_url = f"https://www.google.com/search?q={query}"
        webbrowser.open(search_url)
        print(f"Searching Google for: {query}")
        speak(f"Searching Google for {query}")
    except Exception as e:
        print(f"Error performing Google search: {e}")
        speak("I couldn't perform the search.")

def play_youtube_video(query):
    """Search and play a YouTube video based on the query."""
    try:
        speak(f"Searching and playing {query} on YouTube.")
        print(f"Searching and playing {query} on YouTube.")
        pywhatkit.playonyt(query)  # Automatically opens the top search result on YouTube
    except Exception as e:
        print(f"Error playing video: {e}")
        speak("I couldn't play the YouTube video. Please try again.")

def get_response(prompt):
    """Fetch responses from the Gemini API with an instruction for short answers."""
    try:
        # Modify the prompt to include an instruction for a short response
        short_prompt = f"{prompt} Please provide a concise and short answer. and do not repeat this. Do not give answer in bold letters"
        response = genai.GenerativeModel('gemini-pro').generate_content(short_prompt)
        return response.text
    except Exception as e:
        print(f"API Error: {e}")
        return "I'm having trouble connecting to the service."

def assistant():
    """Run the voice assistant loop."""
    speak("Hello Sir, I am Jarvis. How can I assist you?")
    while True:
        user_input = listen()
        if user_input.lower() == "exit":
            speak("Goodbye!")
            break
        elif "screenshot" in user_input.lower():
            take_screenshot()
        elif "time" in user_input.lower():
            tell_time()
        elif "open" in user_input.lower():
            speak("Which website should I open?")
            website = listen()
            open_website(website)
        elif "search" in user_input.lower():
            speak("What should I search for?")
            query = listen()
            google_search(query)
        elif "play video" in user_input.lower() or "youtube" in user_input.lower():
            speak("What video should I play?")
            video_query = listen()
            play_youtube_video(video_query)
        else:
            print(f"User said: {user_input}")
            response = get_response(user_input)
            print(f"Assistant: {response}")
            speak(response)

if __name__ == "__main__":
    assistant()
