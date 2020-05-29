import os
import numpy as np
import pandas as pd
import src.constants as c

from src.model import vggvox_model
from src.preprocess import build_buckets
from src.wav_reader import get_fft_spectrum
from pydub import AudioSegment

model = vggvox_model()
model.load_weights(c.WEIGHTS_FILE)
buckets = build_buckets(c.MAX_SEC, c.BUCKET_STEP, c.FRAME_STEP)


def enroll(filename, speaker):

    speaker = pd.DataFrame({"speaker": [str(speaker)]})
    
    result = pd.DataFrame([])
    result["features"] = [get_fft_spectrum(filename = filename, buckets = buckets)]
    result["embedding"] = result["features"].apply(lambda x: np.squeeze(model.predict(x.reshape(1, *x.shape, 1))))
    enroll_embs = np.array([emb.tolist() for emb in result["embedding"]])
    
    if os.path.isfile("data/enroll/csv/enroll_embs.csv"):
        with open("data/enroll/csv/enroll_embs.csv", "ab") as f:
            np.savetxt(f, enroll_embs, delimiter = ",")
    else:
        np.savetxt("data/enroll/csv/enroll_embs.csv", enroll_embs, delimiter = ",")
        
    if os.path.isfile("data/enroll/csv/enroll_speakers.csv"):
        with open("data/enroll/csv/enroll_speakers.csv", "a", encoding = "BIG5") as f:
            np.savetxt(f, speaker["speaker"], encoding = "BIG5", delimiter = ",",  fmt = "%s")
    else:
        np.savetxt("data/enroll/csv/enroll_speakers.csv", speaker["speaker"], encoding = "BIG5", delimiter = ",",  fmt = "%s")
    print('\n##################')
    print('\nFinish creating .csv files')
    print('\n##################')


def ENROLL(filename, speaker): 
    # wav = AudioSegment.from_wav(filename)
    enroll(filename = filename, speaker = speaker)
