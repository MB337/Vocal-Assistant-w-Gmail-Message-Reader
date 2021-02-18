# Modules to intsall

import speech_recognition as sr
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from gtts import gTTS
import os
from playsound import playsound

# Url for Gmail Api
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


# We initialize the base to read our Gmail messages (if you can't understand lines 18 to 34 watch a gmail api tutorial)
def read_gmail():
    global creds
    creds = None
    
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
            
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
            
    # We read Gmail message from our 'INBOX'
    service = build('gmail', 'v1', credentials=creds)
    results = service.users().messages().list(userId='me', labelIds=['INBOX']).execute()
    m = results.get('messages', [])
    
    # If there aren't any messages
    if not m:
        print("There aren't messages")
    
    # If there are some messages
    else:
        # We select the first 3
        for message in m[:3]:
            msg = service.users().messages().get(userId="me", id=message["id"], format="full", metadataHeaders=None).execute()
            
            # From the entire message we extract the object and the sender
            headers= msg["payload"]["headers"]
            object_= [i['value'] for i in headers if i["name"]=="Subject"]
            sender = (msg['payload']['headers'][17]['value'])
            
            # Now we read the text and put it in a mp3 file
            text = (object_[0], 'send from: ', sender)
            text = ''.join(text)
            tts = gTTS(text=text, lang='en')
            tts.save("text.mp3")
            
            # For every messages we play the mp3 file and we remove it
            playsound('text.mp3')
            os.remove("text.mp3")
            


    

# This is the start of our script: the vocal recognition --> when we say 'Read Gmail' it will say the gmail message sender and object
recognizer_instance = sr.Recognizer()

# Activate the microphone
with sr.Microphone() as source:
    recognizer_instance.adjust_for_ambient_noise(source)
    print("I'm listening...")
    # You can talk
    audio = recognizer_instance.listen(source)
    
# Translate the micophone audio in a 'en-En'(English) text
text = recognizer_instance.recognize_google(audio, language="en-En")
print("Your message:", text)

list_mail = ['Read Gmail', 'read Gmail']

# If you say somethings in list_mail it will speak thanks to read_gmail function.
if text in list_mail:
    read_gmail()
