import pyttsx3 #through this we can make our assistant
import speech_recognition as sr #it helps Dobby to recognise user voice 
import webbrowser #enables to search on webbrowser
import pywhatkit#helps in searching in web browser
import os
import pyjokes
from PyDictionary import PyDictionary as Dict#used in dictionary 
from nltk.corpus import wordnet
import nltk
nltk.download('wordnet')
from googletrans import Translator, LANGUAGES
from datetime import datetime
from PyPDF2 import PdfReader

Assistant = pyttsx3.init('sapi5') #ide of microsoft for speech recognition
voices = Assistant.getProperty('voices')#to get property of voices from assiatant
Assistant.setProperty('voices', voices[0].id)
Assistant.setProperty('rate', 190)  #by default rate of speech is 200

flag = int(input('Speech to Text (1) or Text to Speech(0) : '))
if flag != 0 and flag != 1:
    print("Default Speech to text mode activated")
    flag = 1

def speak(audio): #to make our Dobby speak
    Assistant.say(audio)
    print(f"Dobby : {audio}")#whatever Dobby says it prints that message
    Assistant.runAndWait()
      
def takeCommand(): #Helps Dobby to take command from the user
    if flag == 0:
        print("Enter the command : ")
        query = input()
        return query
    else:
        command = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening........")
            command.pause_threshold = 1
            audio = command.listen(source)

            try:
                print("Recognizing.....")
                query = command.recognize_google(audio, language='en-id')
                print(f"You said : {query}")
                return query.lower()

            except Exception as error:
                return "none"
    
def takeExecution():
    global flag
    
    app_paths = {
    'youtube': r"C:\\Users\ACER\\OneDrive\Desktop\\YouTube.lnk",
    'vs code': r'C:\\Users\ACER\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe',
    'chrome': r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    'edge': r"C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
    'teams': r"C:\\Users\ACER\\OneDrive\\Desktop\\Microsoft Teams classic (work or school).lnk",
    
    }
    
    while True:#logic behind this while loop is to make listen us every time when we want to
        
        query = takeCommand()
        
        def read_pdf(pdf_path):
            try:
                pdf_reader = PdfReader(pdf_path)
                '''
                This line creates an instance of the PdfReader class, initializing it with the path to the PDF file (pdf_path).
                This instance is used to read and extract information from the PDF.
                '''
                num_pages = len(pdf_reader.pages)

                for page_num in range(num_pages):
                    page = pdf_reader.pages[page_num]
                    text = page.extract_text()
                    speak(text)

            except Exception as e:
                print(f"An error occurred while reading the PDF: {e}")
                
        def get_date():
            current_date = datetime.now().strftime("%Y-%m-%d")
            return current_date
        
        def get_current_time():
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            return current_time
        
        def get_synonyms(word):
            synonyms = []
            for syn in wordnet.synsets(word):#getting the list of all synonyms irrespective of word
                for lemma in syn.lemmas():#collecting the word related to the given word
                    synonyms.append(lemma.name())
            return list(set(synonyms))  # Removing duplicates

        def get_antonyms(word):
            antonyms = []
            for syn in wordnet.synsets(word):
                for lemma in syn.lemmas():
                    if lemma.antonyms():
                        antonyms.append(lemma.antonyms()[0].name())
            return list(set(antonyms))  # Removing duplicates

        def dictionary_function(prob):
            prob = prob.replace("Dobby ", "") 
            prob = prob.replace('what is the ',"")
            prob = prob.replace('tell me the ',"")

            if 'meaning' in prob:
                prob = prob.replace('meaning of ', "")
                result = Dict.meaning(prob)
                speak(f"The meaning of {prob} is {result}")

            elif 'synonym' in prob:
                prob = prob.replace('synonym of ', "")
                result = get_synonyms(prob)
                speak(f"The synonym of {prob} is {result}")

            elif 'antonym' in prob:
                prob = prob.replace('antonym of ', "")
                result = get_antonyms(prob)
                speak(f"The antonym of {prob} is {result}")
        
        def close_app(app_name):
            try:
                os.system(f'TASKKILL /IM {app_name}.exe /F > nul')
                speak(f"Closed {app_name}")
            except Exception as e:
                print(f"Error closing app: {e}")
        
        def email():
            speak('For talking to authority please email the issue in the following email')
            speak('mohitchamyal58@gmail.com')
            
        def trans():
            speak("Select the language you want to translate to:")
            
            for code, lang in LANGUAGES.items():
                print(f"{code}: {lang}")

            target_lang_code = input("Enter the language code: ").lower().strip()  #.lower() change all letter to lower case and .strip() removes the whitespaces
            
            if target_lang_code in LANGUAGES:
                target_lang = LANGUAGES[target_lang_code]
                
                speak(f"Speak in any language : ")
                command = sr.Recognizer()
                
                with sr.Microphone() as source:
                    print("Listening........")
                    command.pause_threshold = 1
                    audio = command.listen(source)
                    
                    try:
                        print("Recognizing.....")
                        query = command.recognize_google(audio, language='en-in')
                        print(f"You said: {query}")
                        
                        translator = Translator()
                        result = translator.translate(query, dest=target_lang)
                        
                        speak(f"The translation to {target_lang} is: {result.text}")

                    except Exception as error:
                        print(error)
                        speak("Sorry, I couldn't understand the language.")

            else:
                speak("Invalid language code. Please try again.")
            
        def open_app(app_name):
            try:
                os.startfile(app_paths.get(app_name, ""))
            except Exception as e:
                print(f"Error opening app: {e}")
    
        if 'hello' in query:
            speak("Hello sir, I am Dobby")
            speak("Your Personal AI assistant!")
            speak("How may I help you ? ")
        
        elif 'music' in query:
            speak("Ok sir")
            speak("Here is what I have found")
            #replaces Dobby and search on youtube with empty string in query
            query = query.replace("dobby", "")
            query = query.replace("search music","")
            query = query.replace('music ', "")
            query = query.replace('play ',"")
            #after replacing dobby and search on youtube query is added to browerlink so that it can search on youtube  
            web = "https://www.youtube.com/results?search_query=" + query
            webbrowser.open(web)
            speak("Done sir")
        
        elif 'how are you' in query:
            speak("I am fine sir!")
            speak("How are you?")
        
        elif 'search on youtube' in query:
            speak("Ok sir")
            speak("Here is what I have found")
            #replaces Dobby and search on youtube with empty string in query
            query = query.replace("dobby", "")
            query = query.replace("search on youtube","")
            #after replacing dobby and search on youtube query is added to browerlink so that it can search on youtube  
            web = "https://www.youtube.com/results?search_query=" + query
            webbrowser.open(web)
            speak("Done sir")
            
        elif 'search on google' in query:
            speak("Ok sir")
            speak("Here is what I have found")
            #replace Dobby and google search with empty string in query
            query = query.replace("dobby","")
            query = query.replace("search on google","")
            pywhatkit.search(query)
            speak("Done Sir")
            
        elif 'website' in query:
            speak("Ok sir")
            speak("Here is what I have found")
            #replace Dobby and open website with empty string in query
            query = query.replace("dobby ","")
            query = query.replace("open ", "")
            web1 = query.replace("launch ","")
            web1 = query.replace("website ","")
            web2 = "https://www." + web1 + '.com'
            webbrowser.open(web2)
            speak("Done Sir")
            
        elif 'open app' in query:
            speak("Sure, which app would you like to open?")
            app_name = takeCommand().lower()

            if app_name in app_paths:
                speak(f"Opening {app_name}. Please wait.")
                open_app(app_name)
                speak(f"{app_name} is now open.")
            else:
                speak(f"Sorry, I don't have information about {app_name}.")
        
        elif 'close app' in query:
            speak("Sure, which app would you like to close?")
            app_name = takeCommand().lower()

            if app_name in app_paths:
                speak(f"Closing {app_name}. Please wait.")
                close_app(app_name)
            else:
                speak(f"Sorry, I don't have information about {app_name}.")
                    
        elif 'contact authority' in query:
            email()
        
        elif 'thank you' in query or 'thank' in query or 'bye' in query:
            speak("Thank you sir")
            speak("You can call me any time")
            speak("Your personal AI Assistant - Dobby")
            break
        
        elif 'joke' in query:
            get = pyjokes.get_joke()
            speak(get)
        
        elif 'repeat my words' in query:
            speak('speak sir')
            while True:
                repeat = takeCommand()
                if 'exit' in repeat:
                    speak('Exiting the repeat mode')
                    break
                speak(repeat)
        
        elif 'dictionary' in query:
            
            speak("Dictionary Activated!")  
            while True:
                speak("Tell me the problem")
                prob = takeCommand()

                if 'exit dictionary' in prob:
                    speak('Exiting Dictionary mode')
                    break

                dictionary_function(prob)
        
        elif 'translater' in query or 'translator' in query:
            trans()
        
        elif 'date and time' in query or 'time and date' in query:
            date = get_date()
            current_time = get_current_time()
            speak(f"Today's date is {date} and current time is {current_time}")
        
        elif 'time' in query:
            current_time = get_current_time()
            speak(f"The current time is {current_time}")
        
        elif 'date' in query:
            date = get_date()
            speak(f"Today's date is {date}")
        
        elif 'g e h u e r p' in query or 'gehu erp' in query:
            speak("Ok sir")
            speak("Here is what I have found")
            #replace Dobby and google search with empty string in query
            query = query.replace("dobby","")
            query = query.replace("open","")
            webbrowser.open('https://student.gehu.ac.in/')
            speak("Done Sir")
            
        elif 'g e u e r p' in query or 'geu erp' in query:
            speak("Ok sir")
            speak("Here is what I have found")
            #replace Dobby and google search with empty string in query
            query = query.replace("dobby","")
            query = query.replace("open","")
            webbrowser.open('https://student.geu.ac.in/')
            speak("Done Sir")
        
        elif 'read pdf' in query or 'pdf reader' in  query:
            speak("Please enter the path of PDF.")
            pdf_path = input(r"Enter the pdf path : ")
            read_pdf(pdf_path)
        
        elif 'speech to text' in query:
            if flag == 1:
                speak('Already in speech to text mode')
            else:
                flag = 1
                speak("Speech to text mode activated")

        elif 'text to speech' in query:
            if flag == 0:
                speak('Already in text to speech mode')
            else:
                flag = 0
                speak("Text to speech mode activated")        
        
        else:
           speak("Sorry, I couldn't recognize")
           speak("Can you speak again")
        
takeExecution()