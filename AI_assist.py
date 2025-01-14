import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
import datetime
import pyaudio

r = sr.Recognizer()
phone_numbers = {'manju': '+916305378355', 'mom': '+9105388355', 'dad': '+9190000000', 'akka': '+9177134667'}

# Initialize the voice engine globally
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(command):
    engine.say(command)
    engine.runAndWait()

def commands():
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)  
            print('Listening... Now ask')
            audioin = r.listen(source)
            my_text = r.recognize_google(audioin).lower()  
            print(my_text)

            if 'play' in my_text:
                my_text = my_text.replace('play', '')
                speak('Playing ' + my_text)
                pywhatkit.playonyt(my_text)
                
            elif 'message' in my_text:
                parts = my_text.split('message')
                if len(parts) > 1:
                    message = parts[0].strip().replace('send', '')
                    name_number = parts[1].strip().replace('to', '').strip()
                    if name_number in phone_numbers:
                        pywhatkit.sendwhatmsg_instantly(phone_numbers[name_number], message)
                        speak("Message sent.")
                    else:
                        speak("Sorry, no contact found.")
                else:
                    speak("Message format not understood.")

            elif 'search' in my_text:
                topic = my_text.replace('search', '').strip()
                pywhatkit.search(topic)
                speak(f"Searching for {topic}.")

            elif 'date' in my_text:
                today = datetime.date.today().strftime('%B %d, %Y')  
                speak(f"Today's date is {today}")

            elif 'time' in my_text:
                timenow = datetime.datetime.now().strftime('%H:%M %p')  
                speak(f"The time now is {timenow}")

            elif 'who is' in my_text:
                person = my_text.replace('who is', '').strip()
                info = wikipedia.summary(person, sentences=1)  
                speak(info)

            elif "phone number" in my_text:
                for name in phone_numbers:
                    if name in my_text:
                        speak(f"{name}'s phone number is {phone_numbers[name]}")
                        break  
                else:
                    speak("No matching contact found.")

            elif 'stop' in my_text or 'exit' in my_text:
                speak("Goodbye!")
                return False

            else:
                speak("Sorry, I don't know that command.")
        return True

    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
    except Exception as e:
        print(f"Error: {e}")
        speak("An error occurred.")
    return True

while commands():
    pass
