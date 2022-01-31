from flask import Flask, request, render_template
from flask_cors import cross_origin
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from summarization import result
import os
import nltk
nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)


app = Flask(__name__)

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
        
        apikey = "2Er2VM52mxifdyT1_ONwrivo9ABHqPd_v-mFzAB-ueH3"
        url = "https://api.eu-gb.speech-to-text.watson.cloud.ibm.com/instances/10975018-ddad-4aee-a868-acfa67bfc1ec"

        authenticator = IAMAuthenticator(apikey)
        stt = SpeechToTextV1(authenticator = authenticator)
        stt.set_service_url(url)

        with open("meta.mp3", mode="rb")  as mp3:
                response = stt.recognize(audio=mp3, model='en-IN_Telephony', content_type='audio/mp3', smart_formatting = True, inactivity_timeout=360)
                real_text = []
                confident = []
                for items in response.result["results"]:
                    for alternatives in items["alternatives"]:
                #print(alternatives["transcript"])
                        real_text.append(alternatives["transcript"])
                        confident.append(alternatives["confidence"])
#           for transcript in alternatives["transcript"]:

                real_text = '. '.join(real_text)
        with open("original_text.txt", "w") as text_file:
            text_file.write(real_text)
        # response_result = result_fun("meta.mp3")
        final_text, summary = result("original_text.txt")
        os.remove("meta.mp3")
        return render_template('home.html',prediction_probability="Orignal text . {}".format(final_text), prediction_emotion = "Summary. {}".format(summary))
    return render_template("home.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)