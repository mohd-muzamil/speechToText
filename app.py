import requests
from flask import Flask, render_template, request, redirect, url_for,Response
from static import configFile
from speechmatics.models import ConnectionSettings, BatchTranscriptionConfig
from speechmatics.batch_client import BatchClient
import os
import soundfile
import numpy as np

def transcriptAudio(filepath):
    """implemented using speechmatics api"""

    LANGUAGE = "en"
    PATH_TO_FILE = filepath
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
        return transcript

app = Flask(__name__)

@app.route("/")
def index():
    response = requests.get("https://meowfacts.herokuapp.com/?count=1")
    data = response.json()
    return render_template("index.html", data=data)

@app.route("/audioToText", methods=["POST"])
def audioToText():
    if request.method == 'POST':
        blob = request.form['blob']
        filename = "audio.wav"
        filepath = os.path.join("../static/audio", filename)
        # data, samplerate = soundfile.read(blob)
        # soundfile.write('audio.wav', data, samplerate, subtype='PCM_16')

        # with open("audio.wav", 'rb') as fp:
            # audio = fp.read()
        # transcript = transcriptAudio(filepath)
    else:
        print("file not recieved")
    # resp = transcript
    transcript = str(np.random.randn(100))
    return transcript

if __name__ == '__main__':
    app.run(debug=True)