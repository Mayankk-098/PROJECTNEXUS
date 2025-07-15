import subprocess
#Import required libraries
from AppOpener import close, open as appopen #Import functions to open and close apps.
from webbrowser import open as webopen #Import web browser functionality. 
from pywhatkit import search, playonyt
# Import functions for Google search and YouTube playback. 
from dotenv import dotenv_values #Import dotenv to manage environment variables. 
from bs4 import BeautifulSoup # Import BeautifulSoup for parsing HTML content. 
from rich import print #Import rich for styled console output.
from groq import Groq #Import Groq for AI chat functionalities.
import webbrowser # Import webbrowser for opening URLS.
import subprocess #Import subprocess for interacting with the system.
import requests # Import requests for making HTTP requests.
import keyboard # Import keyboard for keyboard related actions.
import asyncio # Import asyncio for asynchronous programming. 
import os #Import os for operating system functionalities.

from datetime import datetime, timedelta
import time
from playsound import playsound
import threading

import edge_tts
import pygame

from googlesearch import search
from Backend.game_runner import GameRunner

# Load environment variables from the .env file.
env_vars=dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey") # Retrieve the Groq API key.
# Define CSS classes for parsing specific elements in HTML content.
classes = ["zCubwf", "hgKElc", "LTKOO SY7ric", "ZOLCW", "gsrt vk_bk FzvWSb YwPhnf", "pclqee", "tw-Data-text tw-text-small tw-ta", "IZ6rdc", "05uR6d LTK00", "vlzY6d", "webanswers-webanswers_table_webanswers-table", "dDoNo ikb4Bb gsrt", "sXLa0e", "LWkfKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"]
# Define a user-agent for making web requests.
useragent = "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.2035442 Safari/537.36"
client=Groq(api_key=GroqAPIKey)
# Predefined professional responses for user interactions.
professional_responses = [
"Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
"I'm at your service for any additional questions or support you may need-don't hesitate to ask.",
]
#List to store chatbot messages.
messages=[]
# System message to provide context to the chatbot.
SystemChatBot = [{"role": "system", "content": f"Hello, I am {os.environ['Username']}, You're a content writer. You have to write content like letters, codes, applications, essays, notes, songs, poems etc."}] 
#Function to perform a Google search.
def GoogleSearch(Topic):
    try:
        # Construct the Google search URL
        search_url = f"https://www.google.com/search?q={Topic.replace(' ', '+')}"
        # Open the URL in the default browser
        webbrowser.open(search_url)
        return True  # Return True to indicate success
    except Exception as e:
        print(f"Error in GoogleSearch: {e}")
        return False  # Return False to indicate failure


def SetAlarm(alarm_time_str):
    def alarm_thread(alarm_time, stop_event):
        print(f"[bold yellow]Alarm set for: {alarm_time.strftime('%I:%M %p')}[/bold yellow]")
        while not stop_event.is_set():
            now = datetime.now()
            if now >= alarm_time:
                print("[bold green]⏰ Alarm ringing![/bold green]")
                try:
                    # Play a simple beep sound
                    import winsound
                    for _ in range(5):  # Beep 5 times
                        winsound.Beep(1000, 1000)  # 1000 Hz for 1 second
                        time.sleep(0.5)  # Wait 0.5 seconds between beeps
                except Exception as e:
                    print(f"[red]Error playing alarm: {e}[/red]")
                break
            time.sleep(1)

    try:
        alarm_time = datetime.strptime(alarm_time_str, "%I:%M %p")  # Format like "7:30 AM"
        now = datetime.now()
        alarm_time = alarm_time.replace(year=now.year, month=now.month, day=now.day)
        if alarm_time < now:
            alarm_time += timedelta(days=1)  # Set it for the next day if time passed
        
        # Create a stop event for the thread
        stop_event = threading.Event()
        # Create and start the thread
        alarm_thread = threading.Thread(target=alarm_thread, args=(alarm_time, stop_event), daemon=True)
        alarm_thread.start()
        
        # Store the stop event in a global dictionary for later access
        if not hasattr(SetAlarm, 'active_alarms'):
            SetAlarm.active_alarms = {}
        SetAlarm.active_alarms[alarm_time_str] = stop_event
        
        return True
    except ValueError:
        print("[red]Invalid time format. Use 'HH:MM AM/PM'[/red]")
        return False

def CancelAlarm(alarm_time_str):
    if hasattr(SetAlarm, 'active_alarms') and alarm_time_str in SetAlarm.active_alarms:
        SetAlarm.active_alarms[alarm_time_str].set()
        del SetAlarm.active_alarms[alarm_time_str]
        print(f"[bold green]Alarm for {alarm_time_str} cancelled[/bold green]")
        return True
    print(f"[red]No active alarm found for {alarm_time_str}[/red]")
    return False

def SetReminder(reminder_str):
    def reminder_thread(reminder_time, message, stop_event):
        print(f"[bold yellow]Reminder set for: {reminder_time.strftime('%I:%M %p on %B %d')}[/bold yellow]")
        while not stop_event.is_set():
            now = datetime.now()
            if now >= reminder_time:
                print(f"[bold green]🔔 Reminder: {message}[/bold green]")
                try:
                    async def speak_reminder():
                        # Save the audio to a file first
                        communicate = edge_tts.Communicate(text=f"Reminder: {message}", voice="en-CA-LiamNeural")
                        await communicate.save("Data/reminder.mp3")
                        
                        # Play the audio using pygame
                        pygame.mixer.init()
                        pygame.mixer.music.load("Data/reminder.mp3")
                        pygame.mixer.music.play()
                        
                        # Wait for the audio to finish playing
                        while pygame.mixer.music.get_busy():
                            pygame.time.Clock().tick(10)
                        
                        pygame.mixer.quit()
                        
                    asyncio.run(speak_reminder())
                except Exception as e:
                    print(f"[red]Error playing reminder: {e}[/red]")
                break
            time.sleep(1)

    try:
        # Parse the reminder string (more flexible format)
        parts = reminder_str.split()
        time_str = parts[0]  # Get time part (e.g., "5:58am")
        
        # Convert time format (e.g., "5:58am" -> "5:58 AM")
        if 'am' in time_str.lower():
            time_str = time_str.lower().replace('am', ' AM')
        elif 'pm' in time_str.lower():
            time_str = time_str.lower().replace('pm', ' PM')
        else:
            time_str += ' AM'  # Default to AM if not specified
            
        # Get the message (everything after the time)
        message = ' '.join(parts[1:])
        
        # Parse the time
        reminder_time = datetime.strptime(time_str, "%I:%M %p")
        now = datetime.now()
        reminder_time = reminder_time.replace(year=now.year, month=now.month, day=now.day)
        
        # If the reminder time has passed, set it for the next day
        if reminder_time < now:
            reminder_time += timedelta(days=1)
        
        # Create a stop event for the thread
        stop_event = threading.Event()
        # Create and start the thread
        reminder_thread = threading.Thread(target=reminder_thread, args=(reminder_time, message, stop_event), daemon=True)
        reminder_thread.start()
        
        # Store the stop event in a global dictionary for later access
        if not hasattr(SetReminder, 'active_reminders'):
            SetReminder.active_reminders = {}
        SetReminder.active_reminders[reminder_str] = stop_event
        
        return True
    except Exception as e:
        print(f"[red]Error setting reminder: {e}[/red]")
        print("[red]Please use format: 'HH:MMam/pm message' (e.g., '5:58am eat lunch')[/red]")
        return False

def CancelReminder(reminder_str):
    if hasattr(SetReminder, 'active_reminders') and reminder_str in SetReminder.active_reminders:
        SetReminder.active_reminders[reminder_str].set()
        del SetReminder.active_reminders[reminder_str]
        print(f"[bold green]Reminder '{reminder_str}' cancelled[/bold green]")
        return True
    print(f"[red]No active reminder found for '{reminder_str}'[/red]")
    return False

#Function to generate content using AI and save it to a file.
def Content(Topic):
    def OpenNotepad(File):
        default_text_editor = 'notepad.exe'
        subprocess.Popen([default_text_editor, File])

    def ContentWriterAI(prompt):
        messages.append({"role": "user", "content": f"Write content about: {prompt}. Do not include any greetings or introductions. Start directly with the content."})
        completion = client.chat.completions.create(
            model="mistral-saba-24b",
            messages=SystemChatBot + messages,
            max_tokens=2048,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )
        Answer = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content
        
        # Clean up the response
        Answer = Answer.replace("</s>", "").strip()
        
        # Remove any greeting lines or introductions
        lines = Answer.split('\n')
        cleaned_lines = []
        skip_line = False
        for line in lines:
            line = line.strip()
            # Skip empty lines at the start
            if not cleaned_lines and not line:
                continue
            # Skip lines that look like greetings or introductions
            if any(greeting in line.lower() for greeting in ["hello", "hi,", "dear", "greetings", "hey"]):
                skip_line = True
                continue
            if skip_line and line:
                skip_line = False
            if not skip_line:
                cleaned_lines.append(line)
        
        Answer = '\n'.join(cleaned_lines)
        messages.append({"role": "assistant", "content": Answer})
        return Answer

    Topic = Topic.replace("Content", "").strip()
    ContentByAI = ContentWriterAI(Topic)
    
    if not ContentByAI.strip():
        print("Error: AI did not generate any content.")
        return False

    # Create the Data directory if it doesn't exist
    data_dir = "Data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    file_path = os.path.join(data_dir, f"{Topic.lower().replace(' ', '_')}.txt")
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(ContentByAI)
    except Exception as e:
        print(f"Error writing to file: {e}")
        return False

    OpenNotepad(file_path)
    return True

# Function to search for a topic on YouTube.
def YouTubeSearch(Topic):
    Url4Search = f"https://www.youtube.com/results?search_query={Topic}" 
    webbrowser.open(Url4Search) # Open the search URL in a web browser.
    return True # Indicate success.
    # Construct the YouTube search URL.
# Function to play a video on YouTube.
def PlayYoutube(query):
    playonyt(query) # Use pywhatkit's playonyt function to play the video.
    return True # Indicate success.

# Function to open an application or a relevant webpage.
def OpenApp(app, sess=requests.session()):
    import re
    import os
    import sys
    import shlex

    # Special case for games
    if "game" in app.lower() or "play" in app.lower():
        try:
            # Get absolute paths - handle spaces in paths correctly
            current_dir = os.path.dirname(os.path.abspath(__file__))  # Gets the Backend directory
            c_games_path = os.path.join(current_dir, "c_games")
            print(f"Looking for c_games at: {c_games_path}")
            
            if not os.path.exists(c_games_path):
                print(f"Error: Directory not found: {c_games_path}")
                return False

            # List available games
            available_games = {
                "2048": {"c": "2048.c", "exe": "2048.exe"},
                "kbc": {"c": "kbc.c", "exe": "kbc.exe"},
                "tictactoe": {"c": "tictactoe.c", "exe": "tictactoe.exe"},
                "snake": {"c": "snake.c", "exe": "snake.exe"}
            }

            # If no specific game is mentioned, list available games
            if app.lower() in ["game", "play", "play game"]:
                print("[bold yellow]Available games:[/bold yellow]")
                for game_name in available_games.keys():
                    print(f"- {game_name}")
                return True

            # Find the requested game
            game_files = None
            game_name = None
            for name, files in available_games.items():
                if name.lower() in app.lower():
                    game_files = files
                    game_name = name
                    break

            if not game_files:
                print(f"[red]Game not found. Available games are: {', '.join(available_games.keys())}[/red]")
                return False

            game_c = os.path.join(c_games_path, game_files["c"])
            game_exe = os.path.join(c_games_path, game_files["exe"])

            print(f"Looking for game files at:")
            print(f"Source: {game_c}")
            print(f"Executable: {game_exe}")

            if not os.path.exists(game_exe):
                print(f"Error: Game executable not found: {game_exe}")
                return False

            # Open the source code in VS Code
            try:
                print(f"Opening {game_name} source code in VS Code...")
                code_cmd = ["code", f'"{game_c}"']
                subprocess.run(" ".join(code_cmd), shell=True)
            except Exception as e:
                print(f"Error opening VS Code: {str(e)}")
                return False
            
            # Change to the c_games directory
            print(f"Changing directory to: {c_games_path}")
            os.chdir(c_games_path)
            print(f"Current directory is now: {os.getcwd()}")
            
            # Run the game executable in a new window
            print(f"Starting {game_name}...")
            cmd = f'start cmd /k "{os.path.basename(game_exe)}"'
            subprocess.run(cmd, shell=True, cwd=c_games_path)
            print(f"Game {game_name} started in a new window")
            return True
            
        except Exception as e:
            print(f"Error opening/running game: {str(e)}")
            import traceback
            print(f"Stack trace: {traceback.format_exc()}")
            return False

    # Special case for bank management system
    if "bank management system" in app.lower() or "banking system" in app.lower():
        try:
            # Get absolute paths - handle spaces in paths correctly
            workspace_root = os.path.abspath(os.getcwd())
            print(f"Current workspace root: {workspace_root}")
            
            c_modules_path = os.path.join(workspace_root, "Backend", "C_modules")
            print(f"Looking for C_modules at: {c_modules_path}")
            
            if not os.path.exists(c_modules_path):
                print(f"Error: Directory not found: {c_modules_path}")
                return False

            banking_c = os.path.join(c_modules_path, "banking.c")
            print(f"Looking for banking.c at: {banking_c}")
            
            if not os.path.exists(banking_c):
                print(f"Error: Source file not found: {banking_c}")
                return False

            # Try to open VS Code (but don't fail if it's not available)
            try:
                print("Opening VS Code...")
                code_cmd = ["code", f'"{banking_c}"']
                subprocess.run(" ".join(code_cmd), shell=True)
            except Exception as e:
                print(f"Note: Could not open VS Code (this is optional): {str(e)}")
            
            # Change to the C_modules directory
            print(f"Changing directory to: {c_modules_path}")
            os.chdir(c_modules_path)
            print(f"Current directory is now: {os.getcwd()}")
            
            # Check for GCC
            try:
                print("Checking GCC installation...")
                gcc_check = subprocess.run("gcc --version", shell=True, capture_output=True, text=True)
                if gcc_check.returncode != 0:
                    print("Error: GCC is not installed or not in PATH")
                    return False
                print("GCC is available")
            except Exception as e:
                print(f"Error: GCC check failed: {str(e)}")
                return False
            
            # Compile the C file if needed
            banking_exe = os.path.join(c_modules_path, "banking.exe")
            if not os.path.exists(banking_exe) or os.path.getmtime(banking_c) > os.path.getmtime(banking_exe):
                print("Compiling banking.c...")
                compile_cmd = f'gcc "{banking_c}" -o "{banking_exe}"'
                compile_process = subprocess.run(compile_cmd, shell=True, capture_output=True, text=True)
                if compile_process.returncode != 0:
                    print(f"Compilation error: {compile_process.stderr}")
                    return False
                print("Compilation successful")
            
            # Run the executable from the correct directory with proper console handling
            print("Running banking.exe...")
            
            # Create a new command prompt window and run the banking system in it
            cmd = f'start cmd /k "{banking_exe}"'
            subprocess.run(cmd, shell=True, cwd=c_modules_path)
            print("Banking system started in a new window")
            return True
            
        except Exception as e:
            print(f"Error opening/running banking system: {str(e)}")
            import traceback
            print(f"Stack trace: {traceback.format_exc()}")
            return False
        
    # Special case for hospital management system
    if "hospital management system" in app.lower() or "hospital system" in app.lower():
        try:
            # Get absolute paths - handle spaces in paths correctly
            workspace_root = os.path.abspath(os.getcwd())
            print(f"Current workspace root: {workspace_root}")
            
            c_modules_path = os.path.join(workspace_root, "Backend", "C_modules")
            print(f"Looking for C_modules at: {c_modules_path}")
            
            if not os.path.exists(c_modules_path):
                print(f"Error: Directory not found: {c_modules_path}")
                return False

            hospital_c = os.path.join(c_modules_path, "hospital.c")
            print(f"Looking for hospital.c at: {hospital_c}")
            
            if not os.path.exists(hospital_c):
                print(f"Error: Source file not found: {hospital_c}")
                return False

            # Try to open VS Code (but don't fail if it's not available)
            try:
                print("Opening VS Code...")
                code_cmd = ["code", f'"{hospital_c}"']
                subprocess.run(" ".join(code_cmd), shell=True)
            except Exception as e:
                print(f"Note: Could not open VS Code (this is optional): {str(e)}")
            
            # Change to the C_modules directory
            print(f"Changing directory to: {c_modules_path}")
            os.chdir(c_modules_path)
            print(f"Current directory is now: {os.getcwd()}")
            
            # Check for GCC
            try:
                print("Checking GCC installation...")
                gcc_check = subprocess.run("gcc --version", shell=True, capture_output=True, text=True)
                if gcc_check.returncode != 0:
                    print("Error: GCC is not installed or not in PATH")
                    return False
                print("GCC is available")
            except Exception as e:
                print(f"Error: GCC check failed: {str(e)}")
                return False
            
            # Compile the C file if needed
            hospital_exe = os.path.join(c_modules_path, "hospital.exe")
            if not os.path.exists(hospital_exe) or os.path.getmtime(hospital_c) > os.path.getmtime(hospital_exe):
                print("Compiling hospital.c...")
                compile_cmd = f'gcc "{hospital_c}" -o "{hospital_exe}"'
                compile_process = subprocess.run(compile_cmd, shell=True, capture_output=True, text=True)
                if compile_process.returncode != 0:
                    print(f"Compilation error: {compile_process.stderr}")
                    return False
                print("Compilation successful")
            
            # Run the executable from the correct directory with proper console handling
            print("Running hospital.exe...")
            
            # Create a new command prompt window and run the hospital system in it
            cmd = f'start cmd /k "{hospital_exe}"'
            subprocess.run(cmd, shell=True, cwd=c_modules_path)
            print("Hospital system started in a new window")
            return True
            
        except Exception as e:
            print(f"Error opening/running hospital system: {str(e)}")
            import traceback
            print(f"Stack trace: {traceback.format_exc()}")
            return False
        
     # Special case for hostel management system
    if "hostel management system" in app.lower() or "hostel system" in app.lower():
        try:
            # Get absolute paths - handle spaces in paths correctly
            workspace_root = os.path.abspath(os.getcwd())
            print(f"Current workspace root: {workspace_root}")
            
            c_modules_path = os.path.join(workspace_root, "Backend", "C_modules")
            print(f"Looking for C_modules at: {c_modules_path}")
            
            if not os.path.exists(c_modules_path):
                print(f"Error: Directory not found: {c_modules_path}")
                return False

            hostel_c = os.path.join(c_modules_path, "hostel.c")
            print(f"Looking for hostel.c at: {hostel_c}")
            
            if not os.path.exists(hostel_c):
                print(f"Error: Source file not found: {hostel_c}")
                return False

            # Try to open VS Code (but don't fail if it's not available)
            try:
                print("Opening VS Code...")
                code_cmd = ["code", f'"{hostel_c}"']
                subprocess.run(" ".join(code_cmd), shell=True)
            except Exception as e:
                print(f"Note: Could not open VS Code (this is optional): {str(e)}")
            
            # Change to the C_modules directory
            print(f"Changing directory to: {c_modules_path}")
            os.chdir(c_modules_path)
            print(f"Current directory is now: {os.getcwd()}")
            
            # Check for GCC
            try:
                print("Checking GCC installation...")
                gcc_check = subprocess.run("gcc --version", shell=True, capture_output=True, text=True)
                if gcc_check.returncode != 0:
                    print("Error: GCC is not installed or not in PATH")
                    return False
                print("GCC is available")
            except Exception as e:
                print(f"Error: GCC check failed: {str(e)}")
                return False
            
            # Compile the C file if needed
            hostel_exe = os.path.join(c_modules_path, "hostel.exe")
            if not os.path.exists(hostel_exe) or os.path.getmtime(hostel_c) > os.path.getmtime(hostel_exe):
                print("Compiling hostel.c...")
                compile_cmd = f'gcc "{hostel_c}" -o "{hostel_exe}"'
                compile_process = subprocess.run(compile_cmd, shell=True, capture_output=True, text=True)
                if compile_process.returncode != 0:
                    print(f"Compilation error: {compile_process.stderr}")
                    return False
                print("Compilation successful")
            
            # Run the executable from the correct directory with proper console handling
            print("Running hostel.exe...")
            
            # Create a new command prompt window and run the hostel system in it
            cmd = f'start cmd /k "{hostel_exe}"'
            subprocess.run(cmd, shell=True, cwd=c_modules_path)
            print("Hostel system started in a new window")
            return True
            
        except Exception as e:
            print(f"Error opening/running hostel system: {str(e)}")
            import traceback
            print(f"Stack trace: {traceback.format_exc()}")
            return False
        
     # Special case for library management system
    if "library management system" in app.lower() or "library system" in app.lower():
        try:
            # Get absolute paths - handle spaces in paths correctly
            workspace_root = os.path.abspath(os.getcwd())
            print(f"Current workspace root: {workspace_root}")
            
            c_modules_path = os.path.join(workspace_root, "Backend", "C_modules")
            print(f"Looking for C_modules at: {c_modules_path}")
            
            if not os.path.exists(c_modules_path):
                print(f"Error: Directory not found: {c_modules_path}")
                return False

            library_c = os.path.join(c_modules_path, "library.c")
            print(f"Looking for library.c at: {library_c}")
            
            if not os.path.exists(library_c):
                print(f"Error: Source file not found: {library_c}")
                return False

            # Try to open VS Code (but don't fail if it's not available)
            try:
                print("Opening VS Code...")
                code_cmd = ["code", f'"{library_c}"']
                subprocess.run(" ".join(code_cmd), shell=True)
            except Exception as e:
                print(f"Note: Could not open VS Code (this is optional): {str(e)}")
            
            # Change to the C_modules directory
            print(f"Changing directory to: {c_modules_path}")
            os.chdir(c_modules_path)
            print(f"Current directory is now: {os.getcwd()}")
            
            # Check for GCC
            try:
                print("Checking GCC installation...")
                gcc_check = subprocess.run("gcc --version", shell=True, capture_output=True, text=True)
                if gcc_check.returncode != 0:
                    print("Error: GCC is not installed or not in PATH")
                    return False
                print("GCC is available")
            except Exception as e:
                print(f"Error: GCC check failed: {str(e)}")
                return False
            
            # Compile the C file if needed
            library_exe = os.path.join(c_modules_path, "library.exe")
            if not os.path.exists(library_exe) or os.path.getmtime(library_c) > os.path.getmtime(library_exe):
                print("Compiling library.c...")
                compile_cmd = f'gcc "{library_c}" -o "{library_exe}"'
                compile_process = subprocess.run(compile_cmd, shell=True, capture_output=True, text=True)
                if compile_process.returncode != 0:
                    print(f"Compilation error: {compile_process.stderr}")
                    return False
                print("Compilation successful")
            
            # Run the executable from the correct directory with proper console handling
            print("Running library.exe...")
            
            # Create a new command prompt window and run the library system in it
            cmd = f'start cmd /k "{library_exe}"'
            subprocess.run(cmd, shell=True, cwd=c_modules_path)
            print("Library system started in a new window")
            return True
            
        except Exception as e:
            print(f"Error opening/running library system: {str(e)}")
            import traceback
            print(f"Stack trace: {traceback.format_exc()}")
            return False
        
     # Special case for ticket management system
    if "ticket management system" in app.lower() or "ticket system" in app.lower():
        try:
            # Get absolute paths - handle spaces in paths correctly
            workspace_root = os.path.abspath(os.getcwd())
            print(f"Current workspace root: {workspace_root}")
            
            c_modules_path = os.path.join(workspace_root, "Backend", "C_modules")
            print(f"Looking for C_modules at: {c_modules_path}")
            
            if not os.path.exists(c_modules_path):
                print(f"Error: Directory not found: {c_modules_path}")
                return False

            ticket_c = os.path.join(c_modules_path, "ticket.c")
            print(f"Looking for ticket.c at: {ticket_c}")
            
            if not os.path.exists(ticket_c):
                print(f"Error: Source file not found: {ticket_c}")
                return False

            # Try to open VS Code (but don't fail if it's not available)
            try:
                print("Opening VS Code...")
                code_cmd = ["code", f'"{ticket_c}"']
                subprocess.run(" ".join(code_cmd), shell=True)
            except Exception as e:
                print(f"Note: Could not open VS Code (this is optional): {str(e)}")
            
            # Change to the C_modules directory
            print(f"Changing directory to: {c_modules_path}")
            os.chdir(c_modules_path)
            print(f"Current directory is now: {os.getcwd()}")
            
            # Check for GCC
            try:
                print("Checking GCC installation...")
                gcc_check = subprocess.run("gcc --version", shell=True, capture_output=True, text=True)
                if gcc_check.returncode != 0:
                    print("Error: GCC is not installed or not in PATH")
                    return False
                print("GCC is available")
            except Exception as e:
                print(f"Error: GCC check failed: {str(e)}")
                return False
            
            # Compile the C file if needed
            ticket_exe = os.path.join(c_modules_path, "ticket.exe")
            if not os.path.exists(ticket_exe) or os.path.getmtime(ticket_c) > os.path.getmtime(ticket_exe):
                print("Compiling ticket.c...")
                compile_cmd = f'gcc "{ticket_c}" -o "{ticket_exe}"'
                compile_process = subprocess.run(compile_cmd, shell=True, capture_output=True, text=True)
                if compile_process.returncode != 0:
                    print(f"Compilation error: {compile_process.stderr}")
                    return False
                print("Compilation successful")
            
            # Run the executable from the correct directory with proper console handling
            print("Running ticket.exe...")
            
            # Create a new command prompt window and run the ticket system in it
            cmd = f'start cmd /k "{ticket_exe}"'
            subprocess.run(cmd, shell=True, cwd=c_modules_path)
            print("Ticket system started in a new window")
            return True
            
        except Exception as e:
            print(f"Error opening/running ticket system: {str(e)}")
            import traceback
            print(f"Stack trace: {traceback.format_exc()}")
            return False

    # Known web apps
    web_apps = {
        "reddit": "https://www.reddit.com",
        "instagram": "https://www.instagram.com",
        "facebook": "https://www.facebook.com",
        "twitter": "https://www.twitter.com",
        "youtube": "https://www.youtube.com",
        "gmail": "https://mail.google.com",
        "google": "https://www.google.com",
      
        "linkedin": "https://www.linkedin.com",
        "netflix": "https://www.netflix.com",
        "amazon": "https://www.amazon.com",
        "pinterest": "https://www.pinterest.com",
        "tiktok": "https://www.tiktok.com",
        "twitch": "https://www.twitch.tv",
        "discord": "https://www.discord.com",
        "spotify": "https://www.spotify.com",
        "steam": "https://store.steampowered.com",
        "github": "https://www.github.com",
        "stackoverflow": "https://stackoverflow.com",
        "quora": "https://www.quora.com",
        "chatgpt": "https://chat.openai.com",
        "notion": "https://www.notion.so",
        "canva": "https://www.canva.com",
        "figma": "https://www.figma.com",
        "smvdu": "https://smvdu.ac.in",
        "alibaba": "https://www.alibaba.com",
        "apple": "https://www.apple.com",
        "microsoft": "https://www.microsoft.com",
        
    }
    app = app.lower().strip()

    # Step 1: Open directly if it's a known web app
    for name, url in web_apps.items():
        if name in app:
            print(f"Opening known web app: {name}")
            webopen(url)
            return True
    

    # Step 2: Try to open the app installed on the system
    try:
        print(f"Attempting to open app: {app}")
        appopen(app, match_closest=True, output=True, throw_error=True)
        return True
    except:
        print(f"App '{app}' not found. Searching online...")

        # Nested function to extract clean, relevant links
        def extract_links(html):
            soup = BeautifulSoup(html, 'html.parser')
            anchors = soup.find_all('a', href=True)
            links = []
            for tag in anchors:
                href = tag['href']
                if (
                    href.startswith("http")
                    and "support.google.com" not in href
                    and "accounts.google.com" not in href
                    and "policies.google.com" not in href
                    and not re.search(r'/settings|/preferences', href)
                    and app.split()[0] in href.lower()  # link must contain app name
                ):
                    links.append(href)
            return links

        # Google Search Fallback
        def search_google(query):
            url = f"https://www.google.com/search?q={query}"
            headers = {"User-Agent": useragent}
            response = sess.get(url, headers=headers)
            return response.text if response.status_code == 200 else None

        html = search_google(app)
        if html:
            links = extract_links(html)
            if links:
                print(f"Opening top relevant link: {links[0]}")
                webopen(links[0])
                return True

    return False  # Complete failure


# Function to close an application. 
def CloseApp(app):
    if "chrome" in app:
        pass # Skip if the app is Chrome.
    else:
        try:
            close(app, match_closest =True, output=True, throw_error=True) # Attempt to close return True # Indicate success.
        except:
            return False #Indicate failure.

#Function to execute system level commands.
def System(command):
    #Nested function to mute the system volume. 
    def mute():
        keyboard.press_and_release("volume mute") # Simulate the mute, key press.
    #Nested function to unmute the system volume. 
    def unmute():
        keyboard.press_and_release("volume mute") # Simulate the unmute key press.
    # Nested function to increase the system volume.
    def volume_up():
        keyboard.press_and_release("volume up") # Simulate the volume up key press.
    # Nested function to decrease the system volume.
    def volume_down():
        keyboard.press_and_release("volume down") # Simulate the volume down key press.
    # Execute the appropriate command.
    if command == "mute":
        mute()
    elif command == "unmute":
        unmute()
    elif command == "volume up":
        volume_up()
    
    elif command == "volume down":
        volume_down()
    return True # Indicate success.
    # Asynchronous function to translate and execute user commands.

async def TranslateAndExecute(commands: list[str]):
    for command in commands:
        print(f"Processing command: {command}")  # Debugging
        
        # Handle game commands first
        if any(game in command.lower() for game in ["snake", "2048", "tictactoe", "kbc"]):
            result = await asyncio.to_thread(OpenApp, f"play {command}")
            yield result
            continue
            
        if command.startswith("open "):  # Handle "open" commands
            if "open it" in command:  # Ignore "open it" commands
                continue
            elif "open file" == command:
                continue
            else:
                result = await asyncio.to_thread(OpenApp, command.removeprefix("open "))
                yield result
                
        elif command.startswith("play "):
            # Check if it's a game command
            if any(game in command.lower() for game in ["snake", "2048", "tictactoe", "kbc"]):
                result = await asyncio.to_thread(OpenApp, command)
                yield result
            else:
                result = await asyncio.to_thread(PlayYoutube, command.removeprefix("play "))
                yield result
            
        elif command.startswith("content "):
            result = await asyncio.to_thread(Content, command.removeprefix("content "))
            yield result
            
        elif command.startswith("google search "):
            result = await asyncio.to_thread(GoogleSearch, command.removeprefix("google search "))
            yield result
            
        elif command.startswith("youtube search "):
            result = await asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search "))
            yield result
            
        elif command.startswith("system "):
            result = await asyncio.to_thread(System, command.removeprefix("system "))
            yield result
            
        elif command.startswith("alarm "):  # Changed from "set alarm" to "alarm"
            result = await asyncio.to_thread(SetAlarm, command.removeprefix("alarm "))
            yield result
            
        elif command.startswith("cancel alarm "):
            result = await asyncio.to_thread(CancelAlarm, command.removeprefix("cancel alarm "))
            yield result
            
        elif command.startswith("reminder "):
            result = await asyncio.to_thread(SetReminder, command.removeprefix("reminder "))
            yield result
            
        elif command.startswith("cancel reminder "):
            result = await asyncio.to_thread(CancelReminder, command.removeprefix("cancel reminder "))
            yield result

async def Automation(commands: list[str]):
    results = []
    async for result in TranslateAndExecute(commands):
        results.append(result)
        print(f"Command result: {result}")  # Debugging
    return results  # Return the list of results instead of converting to boolean

