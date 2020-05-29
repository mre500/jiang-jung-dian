
import numpy as np
import pandas as pd

import src.constants as c
from src.model import vggvox_model
from src.preprocess import build_buckets
from src.wav_reader import get_fft_spectrum

from pydub import AudioSegment
from scipy.spatial.distance import cdist
import os
model = vggvox_model()
model.load_weights(c.WEIGHTS_FILE)
buckets = build_buckets(c.MAX_SEC, c.BUCKET_STEP, c.FRAME_STEP)

enroll_embs = np.loadtxt(open("../enroll_data/csv/enroll_embs.csv", "rb"), delimiter = ",")
speakers = np.loadtxt(open("../enroll_data/csv/enroll_speakers.csv", "rb"), encoding = "BIG5", delimiter = ",", dtype = str)
speakers = pd.Series(speakers)

def test(filename): 
    
    result = pd.DataFrame([])
    result['features'] = [get_fft_spectrum(filename = filename, buckets = buckets)]
    result['embedding'] = result['features'].apply(lambda x: np.squeeze(model.predict(x.reshape(1, *x.shape, 1))))
    test_embs = np.array([emb.tolist() for emb in result['embedding']])
    
    distances = pd.DataFrame(cdist(test_embs, enroll_embs, metric = c.COST_METRIC), columns = speakers)
    speaker = str(distances[speakers].idxmin(axis = 1)[0])
    
    return speaker

def TEST(filename, window = 3): 
    
    wav = AudioSegment.from_wav(filename)
    prediction = []
    
    if len(wav) > (window * 1000): 
        for i in range(len(wav)//1000 - 3 + 1): 
            wavTemporary = wav[:(i + 3) * 1000]
            wavTemporary.export("./temp.wav", format = "wav")
            speaker = test(filename = "./temp.wav")
            prediction.append(speaker)
    else: 
        speaker = test(filename = filename)
        prediction.append(speaker)
        
    os.remove("./temp.wav")
    
    result = {i: prediction.count(i) / len(prediction) for i in np.unique(speakers).tolist()}
    highest = max(result, key= result.get) 
    return highest
