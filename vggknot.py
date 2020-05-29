import os
import re
import sys
import time
import glob
import json
import tscribe
import shutil

import numpy as np
import soundfile as sf

from src.Enroll import ENROLL
from src.Test import TEST


def enrollWrapper(folderpath="data/enroll/wav/"):
    if len(os.listdir('data/enroll/csv/')) > 0:
        for f in os.listdir('data/enroll/csv'):
            os.remove(os.path.join('data/enroll/csv', f))
    name_list = os.listdir(folderpath)
    print(name_list)
    for i in range(len(name_list)):
        ENROLL(filename=folderpath + name_list[i], speaker=name_list[i])


def recognizer(spk_folder='data/vggvox/'):
    skp_file = [spk_folder + f for f in os.listdir(spk_folder)]  # spk 路徑
    Speaker_IDs = [os.path.splitext(f)[0] for f in os.listdir(spk_folder)]  # spk_0.wav -> spk_0 : 刪掉副檔名

    print(skp_file)
    speakers = [TEST(f) for f in skp_file]

    return Speaker_IDs, speakers


def replaceName(Speaker_IDs, speakers):
    # Obtain the latest json files
    json_files = glob.glob('data/transcribe/*.json')
    latest_json = max(json_files, key=os.path.getctime)

    # Replace speakers wiopenth Speaker_IDs in the json file
    with open(latest_json, 'r', encoding='utf-8') as f:
        json_file = json.load(f)
        txt = json.dumps(json_file,)
    for i in range(len(speakers)):
        txt = txt.replace(Speaker_IDs[i], speakers[i])
    print(txt)

    new_path = latest_json.replace('transcribe', 'report')
    with open(new_path, 'w') as f:
        f.write(txt)

    tscribe.write(new_path,
                  format="csv",
                  save_as=new_path.replace('.json', '.csv'))
    os.remove(new_path)









