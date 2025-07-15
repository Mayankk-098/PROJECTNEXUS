from groq import Groq #Importing the Groq library to use its API.
from json import load, dump # Importing functions to read and write JSON files.
import datetime # Importing the datetime module for real-time date and time information.
from dotenv import dotenv_values # Importing dotenv_values to read environment variables from a .env file.
# Load environment variables from the .env file.
env_vars=dotenv_values(".env")
#Retrieve specific environment variables for username, assistant name, and API key.
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")
#Initialize the Groq client using the provided API key.
client = Groq(api_key=GroqAPIKey)
# Initialize an empty list to store chat messages.
messages = []
# Define a system message that provides context to the AI chatbot about its role and behavior. 
System=System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which has real-time up-to-date information from the internet. I created you.
*** Do not tell time until i ask, Do not talk too much, just answer the question. ***
*** Reply only in English, even if the question is in hindi, reply in English. ***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***

For writing requests, follow these guidelines:

1. Songs:
- Create actual song lyrics with verses, chorus, and bridge where appropriate
- Use appropriate song structure and rhyming patterns
- Make the lyrics emotional and engaging
- Include clear section markers (Verse 1, Chorus, etc.)

2. Poems:
- Use appropriate poetic forms and structures
- Include proper line breaks and stanzas
- Use literary devices like rhyme, meter, and imagery
- Maintain consistent style throughout

3. Letters:
- Use appropriate letter format (salutation, body, closing)
- Match the tone to the purpose (formal, informal, business)
- Include proper date and address if needed
- Maintain clear structure and organization

4. Essays:
- Follow proper essay structure (introduction, body paragraphs, conclusion)
- Include clear thesis statements
- Use appropriate transitions between paragraphs
- Support arguments with evidence and examples
- Maintain formal academic tone

5. Stories:
- Include clear narrative structure (beginning, middle, end)
- Develop characters and setting
- Use appropriate dialogue formatting
- Include descriptive language and imagery
- Maintain consistent point of view

6. General Writing:
- Match the style to the requested format
- Use appropriate language and tone
- Maintain proper grammar and punctuation
- Keep content focused on the requested theme
- Avoid mixing formats unless specifically requested
"""
# A list of system instructions for the chatbot.
SystemChatBot=[
{"role": "system", "content": System}
]
import os
#Attempt to load the chat log from a JSON file.
try:
    if os.path.exists(r"Data\ChatLog.json") and os.path.getsize(r"Data\ChatLog.json") > 0:
        with open(r"Data\ChatLog.json", "r") as f:
            messages = load(f)
    else:
        # If the file is empty, create an empty JSON file to store chat logs. 
        with open(r"Data\ChatLog.json", "w") as f:
            dump([], f)
        messages = []
except FileNotFoundError:
    # If the file doesn't exist, create an empty JSON file to store chat logs. 
    with open(r"Data\ChatLog.json", "w") as f:
        dump([], f)
    messages = []
# Function to get real-time date and time information.
def RealtimeInformation():
    current_date_time = datetime.datetime.now() # Get the current date and time.
    day = current_date_time.strftime("%A") 
    date = current_date_time.strftime("%d") 
    month = current_date_time.strftime("%B") 
    year = current_date_time.strftime("%Y") 
    hour = current_date_time.strftime("%H") 
    minute = current_date_time.strftime("%M") 
    second=current_date_time.strftime("%S")
    data = f"Please use this real-time information if needed, \n"
    data += f"Day: {day}\nDate: {date}\nMonth: {month}\nYear: {year}\n" 
    data += f"Time: {hour} hours : {minute} minutes : {second} seconds.\n" 
    return data


# Function to modify the chatbot's response for better formatting. 
def AnswerModifier (Answer):
    lines = Answer.split('\n') # Split the response into lines. 
    non_empty_lines=[line for line in lines if line.strip()] # Remove empty lines. 
    modified_answer = '\n'.join(non_empty_lines) # Join the cleaned lines back together. 
    return modified_answer
# Main chatbot function to handle user queries.
def ChatBot (Query):
    """ This function sends the user's query to the chatbot and returns the AI's response. """
    try:
        # Skip game-related queries entirely
        if any(game in Query.lower() for game in ["snake", "2048", "tictactoe", "kbc", "play game", "want to play"]):
            return None

        # Load the existing chat log from the JSON file. 
        with open(r"Data\ChatLog.json", "r") as f:
            messages = load(f)
        
        # Append the user's query to the messages list. 
        messages.append({"role": "user", "content": f" {Query}"})
        # Make a request to the Groq API for a response.

         # Check if the query asks for real-time information.
        if "time" in Query.lower() or "date" in Query.lower():
            # Add real-time information as a system message.
            messages.append({"role": "system", "content": RealtimeInformation()})


        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            # Specify the AI model to use.
            messages=SystemChatBot + [{"role": "system", "content": RealtimeInformation ()}] + messages, # Include system instructions, real-time info, 
            max_tokens=1024, # Limit the maximum tokens in the response.
            temperature=0.7, # Adjust response randomness (higher means more random).
            top_p=1, # Use nucleus sampling to control diversity.
            stream=True, # Enable streaming response.
            stop=None # Allow the model to determine when to stop.
        )
        Answer=""
        # Initialize an empty string to store the AI's response.
        # Process the streamed response chunks.
        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content
                # Check if there's content in the current chunk.
        

        Answer = Answer.replace("</s>", "") # Clean up any unwanted tokens from the response.
        # Append the chatbot's response to the messages list. 

        messages.append({"role": "assistant", "content": Answer})
        # Save the updated chat log to the JSON file. 

        with open(r"Data\ChatLog.json", "w") as f: 
            dump(messages, f, indent=4)
        # Return the formatted response.

        return AnswerModifier(Answer=Answer)
    except Exception as e:
        # Handle errors by printing the exception and resetting the chat log. 
        print(f"Error: {e}")
        with open(r"Data\ChatLog.json", "w") as f:
            dump([], f, indent=4)
        return ChatBot (Query) # Retry the query after resetting the log.

def handle_game_request(self, message):
    # Forward game requests to the automation system
    if any(game in message.lower() for game in ["snake", "2048", "tictactoe", "kbc"]):
        return None  # Let the automation system handle it
    return "I'm sorry, I don't understand that game command. Try asking to play snake, 2048, tictactoe, or kbc."

#Main program entry point.
if __name__=="__main__":
        while True:
            user_input = input("Enter Your Question: ") # Prompt the user for a question. 
            print(ChatBot(user_input)) # Call the chatbot function
        