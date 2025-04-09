import pyautogui  # For controlling mouse and keyboard
import time       # For adding delays
import requests   # For sending API requests to Gemini
import pyperclip  # For clipboard access

# Gemini API setup
API_KEY = "AIzaSyDRq2qFtF6XzjMhqhxh6cERqqcKY03OSYk" # Generate your API_KEY HERE , # Can use Gemini for free api key's
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

# Prompt instruction for Gemini
prompt = '''
Read the following chat history between "Unknown" and "Jenish Surani". Generate only the next line from Unknown, with no formatting, no labels, and no explanation. Keep the tone casual and match the language used in the chat. also add relevant emojis.
'''

# Function to check if the last message in the chat is from the target sender

def is_last_msg_from_sender(chat_history: str, sender="Jenish Surani") -> bool:
    messages = chat_history.strip().split('\n')
    for msg in reversed(messages):
        if msg.strip():  # skip empty lines
            return sender in msg
    return False

# Open WhatsApp window (click on the taskbar icon)

pyautogui.click(x=743, y=1169)  # Click to open WhatsApp
time.sleep(1)

# # Loop to continuously monitor and respond to chats

while True:
    #  Select the chat window and copy recent messages
    pyautogui.moveTo(x=668, y=287) # Start coordinate of chat area
    pyautogui.dragTo(x=732, y=1071, duration=1, button='left') # Drag to select text
    pyautogui.hotkey('ctrl', 'c') # Copy selected chat
    time.sleep(1)

    chat_history = pyperclip.paste() # Paste copied chat in varible chat_history
    
    pyautogui.click(x=820,y=992) # Deselect the selected message by cliking on random point for cleanup

    # Check Whether last message is send by the sender or last message is yours?
    
    if is_last_msg_from_sender(chat_history):
        
        # Prepare full prompt with current chat
        full_input = prompt + chat_history
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "contents": [
                {
                    "parts": [
                        {"text": full_input}
                    ]
                }
            ]
        }

        # Send request to Gemini API
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            try:
                # Parse the response and get the generated message
                result = response.json()
                variable2 = result['candidates'][0]['content']['parts'][0]['text'].strip()
                print("Generated:", variable2)
            except Exception as e:
                variable2 = ""
                print("Error parsing response:", e)
        else:
            variable2 = ""
            
        # Paste the generated response into WhatsApp and send
        pyautogui.click(x=824, y=1068)  # Click message input box
        time.sleep(1) #Wait
        
        pyperclip.copy(variable2) # Copy the respond now
        time.sleep(0.5)
        pyautogui.hotkey('ctrl', 'v')  # Paste the message in the chatbox
        time.sleep(1)
        
        pyautogui.press('enter')  # Send the message

            
            
# Author : Jenis Surani
# Date   : 09-04-2025
# Topic  : CHATBOT (main.py)