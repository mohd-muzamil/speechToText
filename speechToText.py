from speechmatics.models import ConnectionSettings, BatchTranscriptionConfig
from speechmatics.batch_client import BatchClient

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