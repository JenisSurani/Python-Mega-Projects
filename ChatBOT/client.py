import requests 

API_KEY = "AIzaSyDRq2qFtF6XzjMhqhxh6cERqqcKY03OSYk"
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

# Construct input prompt
prompt = '''Read the following chat history between "Unknown" and "Jenish Surani". Generate only the next line from Unknown, with no formatting, no labels, and no explanation. Keep the tone casual and match the language used in the chat. also add relevant emojis.
'''

command = '''
[5:24 pm, 09/04/2025] Unknown: sab badhiya?
[5:24 pm, 09/04/2025] Jenish Surani: Ha bhai sab badhiya.
[5:24 pm, 09/04/2025] Jenish Surani: Tum batao tum kese ho?
[5:25 pm, 09/04/2025] Jenish Surani: Kesi chal rahi hai tumhari coding?
[5:25 pm, 09/04/2025] Unknown: ha bhai acchi chal rahi hai. me abhi project bana raha hu
[5:25 pm, 09/04/2025] Unknown: chatbot ka
[5:25 pm, 09/04/2025] Jenish Surani: Oh wow interesting
[5:25 pm, 09/04/2025] Jenish Surani: Complete ho jane ke baad muje dikhana
[5:25 pm, 09/04/2025] Unknown: ha bhaiya,sure.
[5:25 pm, 09/04/2025] Unknown: or batao aapka business kesa chal rha hai.
[5:26 pm, 09/04/2025] Jenish Surani: Chal raha hai bhagwan ki kripa se.
[5:26 pm, 09/04/2025] Jenish Surani: Ghar se sab badhiya? Nana nani kese hai
[5:26 pm, 09/04/2025] Unknown: sab badhiya hai aapko bahut yaad karte hai ☺️
[5:27 pm, 09/04/2025] Jenish Surani: Ohh unko meri yaad dena
[5:27 pm, 09/04/2025] Unknown: ha bhaiya sure.
'''

full_input = prompt + command

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

# Send request
response = requests.post(url, headers=headers, json=data)

# Hardcoded plain output without any label
if response.status_code == 200:
    try:
        result = response.json()
        raw_output = result['candidates'][0]['content']['parts'][0]['text']
        print(raw_output.strip())  # 👈 Print only raw text
    except Exception:
        print(result)  # fallback
else:
    print(response.text)


# Author : Jenis Surani
# Date   : 09-04-2025
# Topic  : Sample_to_generate_response