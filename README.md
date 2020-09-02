# What the script does?

**The functions of this script (voice assistant, text-reader, Gmail API) are hosted by Google.**

What the script does: when we say 'Read Gmail' the script will say the first 3 object and sender of the Gmail messages.

For doing this we use Google Speech-Recognition for translate the user audio in text, then with Gmail API we read the first 3 messages taking the object and the sender of every message.
Now we can translate the sender and the object in an mp3 audio using gtts library.

# Knowledge appreciated and modules to install
You only have to know how Gmail Api works the vocal assistant and the text reader are easy to learn.

Modules to install:
```
pip install SpeechRecognition
pip install google-api-python-client
pip install google-auth-oauthlib
pip install google-auth
pip install pikl
pip install gTTS
pip install playsound
```
