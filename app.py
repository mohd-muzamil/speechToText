import requests
from flask import Flask, render_template, request, redirect, url_for,Response
from static import configFile
from speechmatics.models import ConnectionSettings, BatchTranscriptionConfig
from speechmatics.batch_client import BatchClient

def translateAudio(audio):
    """implemented using speechmatics api"""

    LANGUAGE = "en"
    PATH_TO_FILE = "./example.wav"
    CONNECTION_URL = f"wss://eu2.rt.speechmatics.com/v2/{LANGUAGE}"
    AUTH_TOKEN = "89REIkjm829i85FlIVG5UFCDYmvN43qa"

    settings = ConnectionSettings(
    url='https://asr.api.speechmatics.com/v2',
    auth_token=AUTH_TOKEN,
    )
    
    # Define transcription parameters
    conf = BatchTranscriptionConfig(
    language=LANGUAGE,
    )

    # Open the client using a context manager
    with BatchClient(settings) as client:
        job_id = client.submit_job(
            audio=PATH_TO_FILE,
            transcription_config=conf,
        )
        print(f'job {job_id} submitted successfully, waiting for transcript')
        
        # Note that in production, you should set up notifications instead of polling. 
        # Notifications are described here: https://docs.speechmatics.com/features-other/notifications
        transcript = client.wait_for_completion(job_id, transcription_format='txt')
        print(transcript)
        return transcript

app = Flask(__name__)

@app.route("/")
def index():
    response = requests.get("https://meowfacts.herokuapp.com/?count=1")
    data = response.json()
    print(data)
    return render_template("index.html", data=data)

@app.route("/audioToText", methods=["POST"])
def audioToText():
    if request.method == 'POST':
        print("-"*100, request.form['blob'])
        audio = request.form['blob']
        transcript = translateAudio(audio)
    else:
        print("file not recieved")
    # resp = transcript
    return "something from server"

if __name__ == '__main__':
    app.run(debug=True)