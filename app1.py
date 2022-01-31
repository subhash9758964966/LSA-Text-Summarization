from flask import Flask, request, render_template
from flask_cors import cross_origin
from summarization import result
import os
import nltk
from pydub import AudioSegment
import azure.cognitiveservices.speech as speechsdk
import time
import datetime

nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)


app = Flask(__name__)


import azure.cognitiveservices.speech as speechsdk
import time
import datetime

def speech_to_text(audio_filename ):
    
    # Creates an instance of a speech config with specified subscription key and service region.
    # Replace with your own subscription key and region identifier from here: https://aka.ms/speech/sdkregion
    speech_key, service_region = "4b73fedba5bf4049a6582a399123d50d", "centralus"
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

    # Creates an audio configuration that points to an audio file.
    # Replace with your own audio filename.
    # audio_filename = "5.wav"
    audio_input = speechsdk.audio.AudioConfig(filename=audio_filename)

    # Creates a recognizer with the given settings
    speech_config.speech_recognition_language="en-US"
    speech_config.request_word_level_timestamps()
    speech_config.enable_dictation()
    speech_config.output_format = speechsdk.OutputFormat(1)

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)

    #result = speech_recognizer.recognize_once()
    all_results = []



    #https://docs.microsoft.com/en-us/python/api/azure-cognitiveservices-speech/azure.cognitiveservices.speech.recognitionresult?view=azure-python
    def handle_final_result(evt):
        all_results.append(evt.result.text) 
    
    
    done = False

    def stop_cb(evt):
        print('CLOSING on {}'.format(evt))
        speech_recognizer.stop_continuous_recognition()
        nonlocal done
        done= True

    #Appends the recognized text to the all_results variable. 
    speech_recognizer.recognized.connect(handle_final_result) 

    #Connect callbacks to the events fired by the speech recognizer & displays the info/status
    #Ref:https://docs.microsoft.com/en-us/python/api/azure-cognitiveservices-speech/azure.cognitiveservices.speech.eventsignal?view=azure-python   
    speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))
    speech_recognizer.recognized.connect(lambda evt: print('RECOGNIZED: {}'.format(evt)))
    speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
    # stop continuous recognition on either session stopped or canceled events
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    speech_recognizer.start_continuous_recognition()

    while not done:
        time.sleep(.5)
            
    print("Printing all results:")
    print(all_results)
    return all_results

#calling the conversion through a function    
 

@app.route("/")
@cross_origin()
def home():
    FILE_DIR = os.path.dirname(os.path.abspath(__file__))
    # absolute path to this file's root directory
    PARENT_DIR = os.path.join(FILE_DIR, os.pardir) 
    print("File Directory is ", FILE_DIR)
    print("Parent directory is ", PARENT_DIR)
    print("Yes this is Subhash 1")
    return render_template("home.html")
    # return "Subhash"




    

@app.route("/predict", methods = ["GET", "POST"])
@cross_origin()
def predict():
    if request.method == "POST":
        print("Yes this is Subhash 2")
        # Date_of_Journey
        file = request.files["file"]
        path = "meta.mp3"
        file.save(path)
        
        output_file = "test.wav"
        sound = AudioSegment.from_mp3("meta.mp3")
        sound.export(output_file, format="wav")
        
        
        result_file = speech_to_text("test.wav")
        with open("original_text.txt", "w") as text_file:
            text_file.write(result_file[0])
        # response_result = result_fun("meta.mp3")
        final_text, summary = result("original_text.txt")
        os.remove("meta.mp3")
        return render_template('home.html',prediction_probability="Orignal text . {}".format(final_text), prediction_emotion = "Summary. {}".format(summary))
    return render_template("home.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)