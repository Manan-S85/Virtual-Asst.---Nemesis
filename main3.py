import pyttsx3
import speech_recognition as sr
import pyautogui
import datetime
import speedtest
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, ImageSequence
from threading import Thread
from news import fetch_news
import requests
from camera import capture_image
import subprocess
import os
from bs4 import BeautifulSoup
import webbrowser
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import time
from datetime import datetime
import platform
from playlist_player import play_playlist
from googletrans import Translator
from pathlib import Path
import shutil
#from calculator_module import perform_calculator_operation, retrieve_history, perform_advanced_calculations
from game import game_play
#from my_speech_module import speak
#from ipl_score import notify_ipl_score
from calc1 import launch_calculator
#import speedtest_cli
from tkinter import simpledialog






# Initialize pyttsx3 engine
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
rate = engine.setProperty("rate", 170)

# Define functions for voice assistant
stop_flag = False

# Define functions for voice assistant
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening.....")
        r.pause_threshold = 1
        r.energy_threshold = 300
        audio = r.listen(source, 0, 4)

    try:
        print("Understanding..")
        query = r.recognize_google(audio, language='en-in')
        print(f"You Said: {query}\n")
        return query.lower()
    except sr.UnknownValueError:
        print("Say that again")
        return "None"
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return "None"
    
NEWS_API_KEY = "a0e7243221fd4fc5bd414013288b8526"

def respond_to_time_query():
    current_time = datetime.now().strftime("%H:%M")
    speak(f"The current time is {current_time}.")
    
def parse_time_string(time_str):
    # Convert time string to datetime object
    try:
        return datetime.strptime(time_str, "%I:%M %p")
    except ValueError:
        pass
    try:
        return datetime.strptime(time_str, "%I %p")
    except ValueError:
        pass
    try:
        return datetime.strptime(time_str, "%H:%M")
    except ValueError:
        pass
    raise ValueError("Unrecognized time format")

def speak_news(news_headlines):
    speak("Fetching the news headlines. Please wait.")
    for headline in news_headlines:
        speak(headline)
        
def get_bbc_news():
    # Function to fetch and display top news from BBC News
    try:
        # 1. Construct API URL
        api_key = "a0e7243221fd4fc5bd414013288b8526"
        main_url = "https://newsapi.org/v1/articles"
        source = "bbc-news"
        sort_by = "top"
        api_url = f"{main_url}?source={source}&sortBy={sort_by}&apiKey={api_key}"

        # 2. Make API Request
        response = requests.get(api_url)

        # 3. Parse JSON Response
        data = response.json()

        # 4. Extract News Articles
        articles = data["articles"]

        # 5. Display and Speak News Titles
        for i, article in enumerate(articles, 1):
            title = article['title']
            print(f"{i}. {title}")
            speak(title)  # Speak out the news title
    except Exception as e:
        # Handle any errors that might occur during the process
        print(f"Error: {e}")

def get_temperature(location):
    search = f"temperature in {location}"
    url = f"https://www.google.com/search?q={search}"
    r = requests.get(url)
    data = BeautifulSoup(r.text, "html.parser")
    # Check if the data contains the temperature information
    temp_elem = data.find("div", class_="BNeawe")
    if temp_elem:
        temp = temp_elem.text
        speak(f"The current temperature in {location} is {temp}")
    else:
        speak("Sorry, I couldn't retrieve the temperature for that location.")

import requests

def speak(text):
    try:
        engine = pyttsx3.init()
    # Set properties (optional)
        engine.setProperty('rate', 150)  # Speed of speech
        engine.setProperty('volume', 1)   # Volume (0.0 to 1.0)
    # Speak the text
        engine.say(text)
        engine.runAndWait()
        pass
    except Exception as e:
        print("Error speaking:", e)

def get_weather_report(location):
    api_key = "YA577CLViXPXXPkGmCvJ5Ui3DCDjtoE7"
    forecast_url = f"https://api.tomorrow.io/v4/weather/forecast?location={location}&apikey={api_key}"
    realtime_url = f"https://api.tomorrow.io/v4/weather/realtime?location={location}&apikey={api_key}"

    try:
        # Fetch forecast data
        forecast_response = requests.get(forecast_url)
        forecast_data = forecast_response.json()

        # Fetch realtime data
        realtime_response = requests.get(realtime_url)
        realtime_data = realtime_response.json()

        # Debug prints
        print("Forecast data:", forecast_data)
        print("Realtime data:", realtime_data)

        # Extract relevant weather information
        forecast_summary = forecast_data.get("forecast", {}).get("daily", [])
        realtime_summary = realtime_data.get("data", {}).get("weather", {}).get("description")

        if forecast_summary:
            forecast_summary = forecast_summary[0].get("weather", {}).get("description")
        else:
            forecast_summary = "No forecast available"

        report = f"Forecast: {forecast_summary}. Realtime: {realtime_summary}"
        speak(report)  # Speak out the weather report
        return report
    except Exception as e:
        print("Error fetching weather:", e)
        return "Error: Failed to fetch weather report"


def open_browser_and_search(query, browser):
    if platform.system() == "Darwin":  # macOS
        binary_location = f"/Applications/{browser.capitalize()} Browser.app/Contents/MacOS/{browser.capitalize()} Browser"
    else:  # Windows
        binary_location = f"C:/Program Files/{browser.capitalize()} Browser/{browser.capitalize()} Browser.exe"

    options = webdriver.ChromeOptions()
    options.binary_location = binary_location
    driver = webdriver.Chrome(options=options, service=ChromeService())

    try:
        search_url = f"https://www.google.com/search?q={query}"
        speak(f"Searching Google for {query} in {browser.capitalize()} browser.")
        driver.get(search_url)
        WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.CSS_SELECTOR, '.tF2Cxc')))
    finally:
        speak(f"Do you want to close {browser.capitalize()}? Say yes to close.")
        close_browser_command = takeCommand().lower()
        if "yes" in close_browser_command:
            if platform.system() == "Darwin":  # macOS
                pyautogui.hotkey('command', 'q')
            else:  # Windows
                driver.quit()  # Close the browser window
            speak(f"{browser.capitalize()} browser is now closed.")
        else:
            speak("Browser window will remain open. You can close it manually.")

def open_browser(browser):
    speak(f"Opening {browser.capitalize()} browser.")
    subprocess.run(["open", "-a", f"{browser.capitalize()} Browser"])

def speak_to_search_on_google():
    speak("Please speak your command to search on Google.")

def open_new_tab(browser):
    speak(f"Opening a new tab in {browser.capitalize()} browser.")
    subprocess.run(["open", "-na", f"{browser.capitalize()} Browser", "--args", "--new-tab"])
def search_google(query):
    search_url = f"https://www.google.com/search?q={query}"
    speak(f"Searching Google for {query}.")
    subprocess.run(["open", search_url])
def play_music():
    if os.name == 'posix':
        os.system("osascript -e 'tell app \"Music\" to play'")
    elif os.name == 'nt':
        subprocess.run(["powershell", "(New-Object -ComObject WMPlayer.OCX).controls.play()"])

def pause_music():
    if os.name == 'posix':
        os.system("osascript -e 'tell app \"Music\" to pause'")
    elif os.name == 'nt':
        subprocess.run(["powershell", "(New-Object -ComObject WMPlayer.OCX).controls.pause()"])

def next_track():
    if os.name == 'posix':
        os.system("osascript -e 'tell app \"Music\" to next track'")
    elif os.name == 'nt':
        subprocess.run(["powershell", "(New-Object -ComObject WMPlayer.OCX).controls.next()"])

def previous_track():
    if os.name == 'posix':
        os.system("osascript -e 'tell app \"Music\" to previous track'")
    elif os.name == 'nt':
        subprocess.run(["powershell", "(New-Object -ComObject WMPlayer.OCX).controls.previous()"])

def stop_motion_detector():
    speak("Stopping motion detector.")
    subprocess.run(["pkill", "-f", "VA/MAIN/motion_detector.py"])

def run_motion_detector():
    speak("Starting motion detector.")
    process = subprocess.Popen(["python", "VA/MAIN/motion.py"])  # Assuming motion_detector.py is your script name

    # Wait for 10 seconds
    time.sleep(10)

    # Ask to stop motion detector
    speak("Motion detector has been running for 10 seconds. Do you want to stop it?")
    response = takeCommand().lower()
    if "yes" in response:
        stop_motion_detector()

def volume_up():
    if os.name == 'posix':
        os.system("osascript -e 'set volume output volume (output volume of (get volume settings) + 10)'")
    elif os.name == 'nt':
        subprocess.run(["powershell", "$wmp = New-Object -ComObject WMPlayer.OCX; $wmp.settings.volume += 10"])

def volume_down():
    if os.name == 'posix':
        os.system("osascript -e 'set volume output volume (output volume of (get volume settings) - 10)'")
    elif os.name == 'nt':
        subprocess.run(["powershell", "$wmp = New-Object -ComObject WMPlayer.OCX; $wmp.settings.volume -= 10"])

def move_cursor_to_area(x, y, width, height):
    screen_width, screen_height = pyautogui.size()
    x = int((x / 100) * screen_width)
    y = int((y / 100) * screen_height)
    width = int((width / 100) * screen_width)
    height = int((height / 100) * screen_height)
    pyautogui.moveTo(x, y, duration=0.5)

def move_cursor_by_offset(x_offset, y_offset):
    current_x, current_y = pyautogui.position()
    new_x = current_x + x_offset
    new_y = current_y + y_offset
    pyautogui.moveTo(new_x, new_y, duration=0.5)

def click_at_cursor():
    pyautogui.click()
def change_cursor_speed(speed_factor):
    pyautogui.PAUSE = pyautogui.PAUSE / speed_factor

FILE_FORMATS = {
    '.txt': 'TextFiles',
    '.pdf': 'PDFs',
    '.doc': 'Documents',
    '.jpg': 'Images',
    '.png': 'Images',
    '.xlsx': 'Spreadsheets',
    '.mp3': 'Audio',
    '.mp4': 'Videos',
    '.zip': 'Archives',
    '.exe': 'Executables'
}

def organize():
    for entry in os.scandir():
        if entry.is_dir():
            continue
        file_path = Path(entry.name)
        file_format = file_path.suffix.lower()
        if file_format in FILE_FORMATS:
            directory_path = Path(FILE_FORMATS[file_format])
            directory_path.mkdir(exist_ok=True)
            shutil.move(file_path, directory_path)  # Move the file to the corresponding directory
    try:
        os.mkdir("OTHER")
    except FileExistsError:
        pass
    for file in os.listdir():
        try:
            if os.path.isdir(file):
                os.rmdir(file)
            else:
                shutil.move(file, "OTHER/" + file)  # Move the remaining files to the 'OTHER' directory
        except:
            pass

def shutdown_system():
    try:
        # Check if running on macOS
        if platform.system() != 'Darwin':
            raise OSError("This function is only supported on macOS.")

        # 1. Speak Notification
        speak("Hold On a Sec! Your system is on its way to shut down")

        # 2. Execute AppleScript command to shut down the system
        script = 'tell application "System Events" to shut down'
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)

        if result.returncode != 0:
            # Error occurred, print error message
            error_message = result.stderr.strip() if result.stderr else "Unknown error"
            raise RuntimeError(f"Error shutting down the system: {error_message}")

        # 3. Feedback
        speak("Your system is shutting down now. Goodbye!")

    except PermissionError:
        # Handle permission error
        speak("Sorry, I don't have the necessary permissions to shut down the system. Please run the script with elevated privileges.")
    except OSError as e:
        # Handle unsupported platform error
        speak(str(e))
    except Exception as e:
        # Handle any other exceptions
        speak(f"Sorry, I encountered an error while shutting down the system: {str(e)}")

def lock_screen():
    try:
        # Check if running on macOS
        if platform.system() != 'Darwin':
            raise OSError("This function is only supported on macOS.")

        # Prompt the user for confirmation
        speak("Are you sure you want to lock the screen?")
        confirmation = takeCommand().lower()  # Assuming takeCommand() is a function that listens for user input

        if "do it" in confirmation:
            # Lock the screen
            speak("Locking the screen now.")
            result = subprocess.run(['pmset', 'displaysleepnow'], capture_output=True, text=True)

            if result.returncode != 0:
                # Error occurred, print error message
                error_message = result.stderr.strip() if result.stderr else "Unknown error"
                raise RuntimeError(f"Error locking the screen: {error_message}")

        else:
            speak("Okay, I won't lock the screen.")

    except PermissionError:
        # Handle permission error
        speak("Sorry, I don't have the necessary permissions to lock the screen. Please run the script with elevated privileges.")
    except OSError as e:
        # Handle unsupported platform error
        speak(str(e))
    except Exception as e:
        # Handle any other exceptions
        speak(f"Sorry, I encountered an error while locking the screen: {str(e)}")

music_player = None

import subprocess
music_file = "VA/MAIN/playlist"
def play_n_music(music_file):
    """
    Play music using the 'afplay' command-line tool.

    Args:
        music_file (str): Path to the music file to be played.

    Returns:
        None
    """
    global music_player
    try:
        # If music is already playing, stop the previous playback
        stop_n_music()

        # Start playing the new music file
        music_player = subprocess.Popen(["afplay", music_file])
    except Exception as e:
        print(f"Error playing music: {e}")

def stop_n_music():
    """
    Stop the currently playing music.

    Returns:
        None
    """
    global music_player
    try:
        # If music is playing, terminate the playback
        if music_player and music_player.poll() is None:
            music_player.terminate()
            music_player.wait()
    except Exception as e:
        print(f"Error stopping music: {e}")

def resume_n_music():
    """
    Resume the previously stopped music playback.

    Returns:
        None
    """
    global music_player
    try:
        # If music was previously stopped, resume playback
        if music_player and music_player.poll() is not None:
            music_player = subprocess.Popen(["afplay", music_file])
    except Exception as e:
        print(f"Error resuming music: {e}")


def translate_text():
    translator = Translator()
    speak("Sure! What text would you like to translate?")
    text = takeCommand()
    speak("Which language would you like to translate it to?")
    lang = takeCommand()

    try:
        translated_text = translator.translate(text, dest=lang)
        print(f"Translated text: {translated_text.text}")
        speak("Here is the translated text:")
        speak(translated_text.pronunciation)
    except Exception as e:
        print("Error translating text:", e)
        speak("Sorry, I couldn't translate the text at the moment. Please try again later.")

def run_camera():
    try:
        script_path = os.path.join(os.path.dirname(__file__), "cam_real_time.py")

        if platform.system() == "Windows":
            command = ["python", script_path]
        elif platform.system() == "Darwin":  # macOS
            command = ["python3", script_path]
        else:  # Linux
            command = ["python3", script_path]

        process = subprocess.Popen(command)
        speak("Camera is now running")
        return process

    except Exception as e:
        speak("Error running camera")
        return None

# Initialize process variable outside of any function
process = None

# Function to handle voice assistant operations
def voice_assistant():
    global stop_flag
    while True:
        if stop_flag:
            break
        query = takeCommand()
        if "wake up" in query:
            from greet import greetMe
            greetMe()
            while True:
                if stop_flag:
                    break
                query = takeCommand()
                if "go to sleep" in query:
                    speak("Ok sir, You can call me anytime")
                    break
                elif "hello" in query:
                    speak("Hello sir, how are you?")
                elif "i am fine" in query:
                    speak("That's great, sir")
                elif "are you alright" in query:
                    speak("Perfect, sir")
                elif "thank you" in query:
                    speak("You are welcome, sir")
                elif "google" in query:
                    from search import searchGoogle
                    searchGoogle(query)
                elif "youtube" in query:
                    from search import searchYoutube
                    searchYoutube(query)
                elif "wikipedia" in query:
                    from search import searchWikipedia
                    searchWikipedia(query)
                elif "sleep" in query:
                    speak("Going to sleep, sir")
                    exit()
                elif "office" in query:
                    from Dictapp import openappweb
                    openappweb(query)
                elif "close" in query:
                    from Dictapp import closeappweb
                    closeappweb(query)
                elif "pause" in query:
                    pyautogui.press("k")
                    speak("video paused")
                elif "resume" in query:
                    pyautogui.press("k")
                    speak("video played")
                elif "mute" in query:
                    pyautogui.press("m")
                    speak("video muted")
                elif "remember that" in query:
                    rememberMessage = query.replace("remember that", "")
                    rememberMessage = rememberMessage.replace("NEMESIS", "")  # Corrected line
                    speak("You told me to remember that" + rememberMessage)
                    remember = open("VA/MAIN/Remember.txt", "a")
                    remember.write(rememberMessage + "\n")  # Added newline character for separation
                    remember.close()
                elif "what do you remember" in query:
                    remember = open("VA/MAIN/Remember.txt", "r")  # Corrected line
                    speak("You told me to remember that" + remember.read())
                #elif "ipl score" in query:
                    #notify_ipl_score()

                elif "whatsapp" in query:
                    from Whatsapp import sendMessage
                    sendMessage()
                elif "play a game" in query:
                    game_play()
                elif "change password" in query:
                    speak("What's the new password")
                    new_pw = input("Enter the new password\n")
                    new_password = open("VA/MAIN/password.txt","w")
                    new_password.write(new_pw)
                    new_password.close()
                    speak("Done sir")
                    speak(f"Your new password is{new_pw}")
                elif "open" in query:   #EASY METHOD
                    query = query.replace("open","")
                    query = query.replace("jarvis","")
                    pyautogui.press("super")
                    pyautogui.typewrite(query)
                    pyautogui.sleep(2)
                    pyautogui.press("enter") 
                #elif "internet speed" in query:
                    #try:
                      #wifi = speedtest_cli.Speedtest()
                      #wifi.get_best_server()
                      #download_speed = wifi.download() / 1024 / 1024  # Convert to Mbps
                      #upload_speed = wifi.upload() / 1024 / 1024  # Convert to Mbps
                      #print("Download Speed:", download_speed, "Mbps")
                      #print("Upload Speed:", upload_speed, "Mbps")
                      #speak(f"Wi-Fi download speed is {download_speed:.2f} megabits per second.")
                      #speak(f"Wi-Fi upload speed is {upload_speed:.2f} megabits per second.")
                    #except Exception as e:
                      #print("Error:", e)
                      #speak("Error occurred while measuring internet speed.")
                elif "news" in query:
                    news_headlines = fetch_news(NEWS_API_KEY)
                    speak_news(news_headlines)
                elif "bbc news" in query:
                    get_bbc_news()
                elif "detect motion" in query:
                    run_motion_detector()
                elif "detect emotion" in query:
                    from scorecard import start_webcam
                    start_webcam()
                elif "stop camera" in query:
                    pyautogui.press("esc")
                    speak("detection paused")
                elif "temperature" in query:
                    speak("Sure! Please specify the location.")
                    location = takeCommand()
                    get_temperature(location)
                elif "weather" in query:
                    speak("Sure! Please specify the location.")
                    location = takeCommand()
                    weather_report = get_weather_report(location)
                    if weather_report != "error":
                        speak(f"The weather report for {location} is {weather_report}")
                    else:
                        speak("Sorry, I couldn't fetch the weather report.")   
                elif "open calculator" in query:
                    launch_calculator()
                
                elif "brave browser" in query:
                    open_browser_and_search(query, 'brave')

                elif "chrome" in query:
                    open_browser_and_search(query, 'chrome')

                elif "search on google" in query:
                    search_query = query.replace("search on google", "")
                    search_google(search_query)
                elif "new tab in chrome" in query:
                    open_new_tab('chrome')
                elif "new tab in brave" in query:
                    open_new_tab('brave')
                elif 'search on stack overflow' in query:
                    query = query.replace("search on stack overflow", "")
                    search_url = f"https://stackoverflow.com/search?q={query}"
                    speak(f"Searching Stack Overflow for {query}.")
                    webbrowser.open(search_url)

                elif 'search on bing' in query:
                    query = query.replace("search on bing", "")
                    search_url = f"https://www.bing.com/search?q={query}"
                    speak(f"Searching Bing for {query}.")
                    webbrowser.open(search_url)
                elif 'search on yahoo' in query:
                    query = query.replace("search on yahoo", "")
                    search_url = f"https://search.yahoo.com/search?p={query}"
                    speak(f"Searching Yahoo for {query}.")
                    webbrowser.open(search_url)

                elif 'search on ask' in query:
                    query = query.replace("search on ask", "")
                    search_url = f"https://www.ask.com/web?q={query}"
                    speak(f"Searching Ask.com for {query}.")
                    webbrowser.open(search_url)

                elif 'search on github' in query:
                    query = query.replace("search on github", "")
                    search_url = f"https://github.com/search?q={query}"
                    speak(f"Searching GitHub for {query}.")
                    webbrowser.open(search_url)
                elif 'search on reddit' in query:
                    query = query.replace("search on reddit", "")
                    search_url = f"https://www.reddit.com/search/?q={query}"
                    speak(f"Searching Reddit for {query}.")
                    webbrowser.open(search_url)
                elif 'search on quora' in query:
                    query = query.replace("search on quora", "")
                    search_url = f"https://www.quora.com/search?q={query}"
                    speak(f"Searching Quora for {query}.")
                    webbrowser.open(search_url)
                elif 'search on facebook' in query:
                    query = query.replace("search on facebook", "")
                    search_url = f"https://www.facebook.com/search/top/?q={query}"
                    speak(f"Searching Facebook for {query}.")
                    webbrowser.open(search_url)
                elif 'search on twitter' in query:
                    query = query.replace("search on twitter", "")
                    search_url = f"https://twitter.com/search?q={query}"
                    speak(f"Searching Twitter for {query}.")
                    webbrowser.open(search_url)
                elif 'search on instagram' in query:
                    query = query.replace("search on instagram", "")
                    search_url = f"https://www.instagram.com/explore/tags/{query}/"
                    speak(f"Searching Instagram for #{query}.")
                    webbrowser.open(search_url)
                elif 'search on pinterest' in query:
                    query = query.replace("search on pinterest", "")
                    search_url = f"https://www.pinterest.com/search/pins/?q={query}"
                    speak(f"Searching Pinterest for {query}.")
                    webbrowser.open(search_url)
                elif 'search on linkedin' in query:
                    query = query.replace("search on linkedin", "")
                    search_url = f"https://www.linkedin.com/search/results/all/?keywords={query}"
                    speak(f"Searching LinkedIn for {query}.")
                    webbrowser.open(search_url)
                elif 'search on snapchat' in query:
                    query = query.replace("search on snapchat", "")
                    search_url = f"https://www.snapchat.com/search?q={query}"
                    speak(f"Searching Snapchat for {query}.")
                    webbrowser.open(search_url)

                elif 'search on whatsapp' in query:
                    query = query.replace("search on whatsapp", "")
                    search_url = f"https://api.whatsapp.com/send?phone={query}"
                    speak(f"Searching WhatsApp for {query}.")
                    webbrowser.open(search_url)



                elif 'search on zoom' in query:
                    query = query.replace("search on zoom", "")
                    search_url = f"https://zoom.us/search?q={query}"
                    speak(f"Searching Zoom for {query}.")
                    webbrowser.open(search_url)
                elif 'search on teams' in query:
                    query = query.replace("search on teams", "")
                    search_url = f"https://www.microsoft.com/en-us/microsoft-365/microsoft-teams/group-chat-software?market=en-US&rtc=1&activetab=pivot%3aoverviewtab&q={query}"
                    speak(f"Searching Microsoft Teams for {query}.")
                    webbrowser.open(search_url)


                elif 'search on slack' in query:
                    query = query.replace("search on slack", "")
                    search_url = f"https://slack.com/intl/en-sg/help/articles/218095017-Find-your-way-around-Slack#search"
                    speak(f"Searching Slack for {query}.")
                    webbrowser.open(search_url)


                elif 'search on booking' in query:
                    query = query.replace("search on booking", "")
                    search_url = f"https://www.booking.com/searchresults.en-gb.html?label=gen173nr-1DCAEoggI46AdIM1gEaFCIAQGYAQm4ARfIAQzYAQPoAQGIAgGoAgO4AvS3ofkFwAIB&sid=29a0590486320624d6011e82e5edf982&sb=1&src=index&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Findex.en-gb.html%3Flabel%3Dgen173nr-1DCAEoggI46AdIM1gEaFCIAQGYAQm4ARfIAQzYAQPoAQGIAgGoAgO4AvS3ofkFwAIB%3Bsid%3D29a0590486320624d6011e82e5edf982%3Bsb_price_type%3Dtotal%26%3B&ss={query}"
                    speak(f"Searching Booking.com for {query}.")
                    webbrowser.open(search_url)
                elif 'search on airbnb' in query:
                    query = query.replace("search on airbnb", "")
                    search_url = f"https://www.airbnb.com/s/{query}"
                    speak(f"Searching Airbnb for {query}.")
                    webbrowser.open(search_url)
                elif 'search on expedia' in query:
                    query = query.replace("search on expedia", "")
                    search_url = f"https://www.expedia.com/Hotel-Search?destination={query}&tab=home"
                    speak(f"Searching Expedia for {query}.")
                    webbrowser.open(search_url)
                elif "pause music" in query:
                    pause_music()
                elif "next track" in query:
                    next_track()
                elif "previous track" in query:
                    previous_track()
                elif "volume up" in query:
                    volume_up()
                elif "volume down" in query:
                    volume_down()
                elif "move cursor to area" in query:
                    _, x, y, width, height = query.split()
                    move_cursor_to_area(int(x), int(y), int(width), int(height))
                elif "move cursor by offset" in query:
                    _, x_offset, y_offset = query.split()
                    move_cursor_by_offset(int(x_offset), int(y_offset))
                elif "single click" in query:
                    click_at_cursor()
                elif "double click" in query:
                    time.sleep(0)
                    pyautogui.doubleClick()
                    speak("Performed a double click at the current cursor position.")
                elif "right click " in query:
                    pyautogui.rightClick()
                elif "scroll up" in query:
                    pyautogui.scroll(10)
                elif "scroll down" in query:
                    pyautogui.scroll(-10)
                elif "go to top left corner" in query:
                    pyautogui.moveTo(0, 0, duration=0.5)
                elif "go to bottom right corner" in query:
                    screen_width, screen_height = pyautogui.size()
                    pyautogui.moveTo(screen_width, screen_height, duration=0.5)
                elif "go to centre" in query:
                    screen_width, screen_height = pyautogui.size()
                    pyautogui.moveTo(screen_width // 2, screen_height // 2, duration=0.5)
                    speak("Cursor has been moved to the center of the screen.")
                elif "click and hold" in query:
                    speak("Please specify the duration for clicking and holding in seconds.")
                    duration = float(takeCommand())
                    pyautogui.mouseDown()
                    time.sleep(duration)
                    pyautogui.mouseUp()
                    speak(f"Click and hold for {duration} seconds completed.")
                elif "release click" in query:
                    pyautogui.mouseUp()
                    speak("The click has been released.")

                elif "start drawing" in query:
                    pyautogui.mouseDown()
                    speak("Drawing mode activated. You can start drawing.")

                elif "click at specific position" in query:
                    speak("Please specify the X and Y coordinates for clicking.")
                    coordinates = takeCommand().split()[-2:]
                    if len(coordinates) == 2:
                        x, y = map(int, coordinates)
                        pyautogui.moveTo(x, y, duration=0.5)
                        pyautogui.click()
                        speak(f"Clicked at position {x}, {y}.")
                    else:
                        speak("Invalid coordinates. Please provide both X and Y coordinates.")
                elif "undo last action" in query:
                    pyautogui.hotkey('ctrl', 'z') if os.name == 'posix' else pyautogui.hotkey('ctrl', 'z')
                    speak("Undo action performed.")
                elif "scroll left" in query:
                    pyautogui.hscroll(3)
                    speak("Scrolled left.")
                elif "scroll right" in query:
                    pyautogui.hscroll(-3)
                    speak("Scrolled right.")

                elif "minimise all windows" in query:
                    pyautogui.hotkey('command', 'mission_control')
                    speak("All windows have been minimized.")
                elif "restore all windows" in query:
                    pyautogui.hotkey('command', 'option', 'm')
                    speak("Restored all minimized windows.")
                elif "right click" in query:
                    pyautogui.rightClick()
                    speak("Performed a right-click.")
                elif "left click" in query:
                    pyautogui.click()
                    speak("Performed a left-click.")
                elif "double right click" in query:
                    pyautogui.rightClick()
                    pyautogui.rightClick()
                    speak("Performed a double right-click.")
                elif "double left click" in query:
                    pyautogui.doubleClick()
                    speak("Performed a double left-click at the current cursor position.")
                elif "middle click" in query:
                    pyautogui.middleClick()
                elif "double middle click" in query:
                    pyautogui.middleClick()
                    pyautogui.middleClick()
                elif "move cursor to top" in query:
                    pyautogui.moveTo(pyautogui.position()[0], 0, duration=0.5)
                elif "move cursor to bottom" in query:
                    screen_width, screen_height = pyautogui.size()
                    pyautogui.moveTo(pyautogui.position()[0], screen_height, duration=0.5)
                elif "move cursor to left" in query:
                    pyautogui.moveTo(0, pyautogui.position()[1], duration=0.5)
                elif "move cursor to right" in query:
                    screen_width, _ = pyautogui.size()
                    pyautogui.moveTo(screen_width, pyautogui.position()[1], duration=0.5)
                elif "change cursor speed" in query:
                    speed_factor = 2.0  # Adjust this value as needed
                    change_cursor_speed(speed_factor)
                elif "what's the time" in query:
                    respond_to_time_query()
                elif 'shutdown system' in query:
                    shutdown_system()
                elif 'lock window' in query or "system ko lock Karen" in query:
                    lock_screen()
                elif "play music" in query or "play playlist" in query:
                    play_playlist("VA/MAIN/playlist")
                elif"play song" in query or "gaana" in query or "song" in query:

                    speak("Sure, please provide the path to your music directory.")

                    speak("For example, it could be '/Users/your_username/Music'")

                    speak("What is the path to your music directory?")

                    music_dir = input("VA/MAIN/playlist").strip()  # Get the music directory path from the user

                    if os.path.isdir(music_dir):

                        songs = os.listdir(music_dir)

                        if songs:

                            speak("Playing a random song for you.")

                            random_song = os.path.join(music_dir, songs[0])

                            play_n_music(random_song)  # Play the music file

                        else:

                            speak("Sorry, I couldn't find any music files in the specified directory.")

                    else:

                        speak("Sorry, the specified directory does not exist.")


                elif 'stop music' in query or 'pause music' in query:

                    stop_n_music()

                    speak("Music playback stopped.")


                elif 'resume music' in query or 'play music' in query:

                    resume_n_music()

                    speak("Resuming music playback.")
                elif "organised files" in query:
                    organize()
                    speak("Files have been organized successfully.")
                elif "translate" in query:
                    translate_text()

                
                
                

from tkinter import Tk, Label, Entry, Button
from tkinter import ttk
from PIL import Image, ImageTk
import tkinter as tk

def start_voice_assistant():
    global stop_flag
    stop_flag = False
    Thread(target=voice_assistant).start()
    
def stop_voice_assistant():
    global stop_flag
    stop_flag = True
    
def shutdown():
    stop_voice_assistant()
    root = tk.Tk()
    root.destroy()

def verify_password():
    password = password_entry.get()
    with open("VA/MAIN/password.txt", "r") as f:
        correct_password = f.read().strip()
    if password == correct_password:
        speak("Password correct")
        change_password_button.config(state="normal")  # Enable the Change Password button
        start_button.config(state="normal")  # Enable the Start button
        stop_button.config(state="normal")  # Enable the Stop button
        shutdown_button.config(state="normal")  # Enable the Shutdown button
    else:
        messagebox.showerror("Incorrect Password", "Incorrect password. Please try again.")
        password_entry.delete(0, tk.END)

def animation(current_frame=0):
    image = gif_frames[current_frame]
    gif_label.configure(image=image)
    current_frame = (current_frame + 1) % len(gif_frames)
    gif_label.image = image  # Keep a reference to prevent garbage collection
    gif_label.after(20, lambda: animation(current_frame))

def change_password():
    new_password = simpledialog.askstring("Change Password", "Enter new password:")
    if new_password:
        with open("VA/MAIN/password.txt", "w") as f:
            f.write(new_password)

def speak(text):
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()
    # Set properties (optional)
    engine.setProperty('rate', 150)  # Speed of speech
    engine.setProperty('volume', 1)   # Volume (0.0 to 1.0)
    # Speak the text
    engine.say(text)
    engine.runAndWait()

def initialize_gui():
    global gif_label, gif_frames, gif_image, password_entry, start_button, stop_button, shutdown_button, change_password_button
    root = Tk()
    root.title("N.E.M.E.S.I.S")
    
    # Get the screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Set the window dimensions to leave space for the taskbar
    window_width = int(screen_width * 0.9)  # 90% of screen width
    window_height = int(screen_height * 0.9)  # 90% of screen height
    window_position_x = (screen_width - window_width) // 2
    window_position_y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{window_position_x}+{window_position_y}")

    # Load and display the background image
    background_image = Image.open("VA/MAIN/imgs/bg21.jpg")
    background_photo = ImageTk.PhotoImage(background_image)
    background_label = Label(root, image=background_photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Add additional images and resize them
    image1 = Image.open("VA/MAIN/imgs/n1.png")
    image1_resized = image1.resize((600, 200))
    top_left_photo2 = ImageTk.PhotoImage(image1_resized)
    top_left_label2 = Label(root, image=top_left_photo2,  borderwidth=0, highlightthickness=0)
    top_left_label2.place(relx=0.5, rely=0.5, anchor="center")
  
    # Create and place the password entry field and submit button in a frame
    password_frame = ttk.Frame(root)
    password_frame.place(relx=0.05, rely=0.92, anchor="sw")  # Positioned at the left bottom corner

    password_label = ttk.Label(password_frame, text="Enter Password:")
    password_label.pack(side="left", padx=10, pady=10)

    password_entry = ttk.Entry(password_frame, show="*")
    password_entry.pack(side="left", padx=10, pady=10)

    submit_button = ttk.Button(password_frame, text="Submit", command=verify_password)
    submit_button.pack(side="left", padx=10, pady=10)

    change_password_button = ttk.Button(password_frame, text="Change Password", command=change_password)
    change_password_button.pack(side="left", padx=10, pady=10)
    change_password_button.config(state="disabled") 

    # Create and place the start, stop, and shutdown buttons in a frame
    button_frame = ttk.Frame(root)
    button_frame.place(relx=0.05, rely=0.85, anchor="sw")  # Positioned at the left bottom corner

    global start_button, stop_button, shutdown_button
    start_button = ttk.Button(button_frame, text="Start N.E.M.E.S.I.S", command=start_voice_assistant, state="disabled")
    start_button.pack(side="left", padx=10, pady=10)

    stop_button = ttk.Button(button_frame, text="Stop N.E.M.E.S.I.S", command=stop_voice_assistant, state="disabled")
    stop_button.pack(side="left", padx=10, pady=10)

    shutdown_button = ttk.Button(button_frame, text="Shutdown", command=shutdown, state="disabled")
    shutdown_button.pack(side="left", padx=10, pady=10)

    # Load and display the animated GIF
    gif_frame = ttk.Frame(root)
    gif_frame.place(relx=0.85, rely=0.3, anchor="center")  # Positioned at the center
    
    gif_file = "VA/MAIN/imgs/bg4.gif"
    gif_image = Image.open(gif_file)
    gif_frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(gif_image)]
    
    gif_label = Label(gif_frame, image=gif_frames[0], borderwidth=0, highlightthickness=0)
    gif_label.pack()

    animation(0)
    
    # Configure font style and size
    style = ttk.Style()
    style.configure("TButton", font=("Rockwell", 16))  # Set button font and size
    style.configure("TLabel", font=("Rockwell", 16))   # Set label font and size

    root.mainloop()

if __name__ == "__main__":
    initialize_gui()





