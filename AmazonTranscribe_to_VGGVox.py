import os
import re
import json
from pydub import AudioSegment

import shutil


def filename_to_time_order(x):
    y = re.sub(pattern=".wav", repl="", string=x)
    y = re.sub(pattern="meeting_", repl="", string=y)
    y = re.sub(pattern="transcribe_", repl="", string=y)
    y = re.sub(pattern="-", repl="", string=y)
    return (y)


def transcribe_result_to_vggvox_wav():
    # part 0: re-create
    if os.path.isdir("./data/vggvox"): shutil.rmtree("./data/vggvox")
    if not os.path.isdir("./data/vggvox"): os.mkdir("./data/vggvox")

    # part 1: aggregate transcribe result
    transcribe_data = os.listdir("./data/transcribe")
    order = [filename_to_time_order(x=i) for i in transcribe_data]
    selected_transcribe_data = transcribe_data[order.index(max(order))]
    with open("./data/transcribe/" + selected_transcribe_data, "r", encoding='utf-8') as fp:
        transcribe_data = json.load(fp)
    # object:
    #    jonName: ""
    #    accountId: ""
    #    result:
    #            transcripts: "all speech"
    #            speaker_labels: "spk & speech"
    #            item: "all words"
    #    status: "COMPLETED"

    number_of_speakers = transcribe_data["results"]["speaker_labels"].get("speakers")
    max_length_timestamp_of_speakers = {}
    for i in range(number_of_speakers):
        if(number_of_speakers == 1): 
            max_length_timestamp_of_speakers["spk_1"] = {
                "duration": 0,
                "start_time": 0,
                "end_time": 0}
        if(number_of_speakers != 1): 
            max_length_timestamp_of_speakers["spk_" + str(i)] = {
                "duration": 0,
                "start_time": 0,
                "end_time": 0}

    segments_of_speakers = transcribe_data["results"]["speaker_labels"].get("segments")
    for i in range(len(segments_of_speakers)):
        speaker_label = segments_of_speakers[i].get("speaker_label")
        start_time = float(segments_of_speakers[i].get("start_time"))
        end_time = float(segments_of_speakers[i].get("end_time"))
        duration = end_time - start_time
        if duration > max_length_timestamp_of_speakers[speaker_label].get("duration"):
            max_length_timestamp_of_speakers[speaker_label]["duration"] = duration
            max_length_timestamp_of_speakers[speaker_label]["start_time"] = start_time
            max_length_timestamp_of_speakers[speaker_label]["end_time"] = end_time

    # part 2: save split wav
    recog_data = os.listdir("./data/recog")
    order = [filename_to_time_order(x=i) for i in recog_data]
    selected_recog_data = recog_data[order.index(max(order))]
    audio_data = AudioSegment.from_wav("./data/recog/" + selected_recog_data)

    for i in range(len(max_length_timestamp_of_speakers)):
        speaker_label = "spk_" + str(i)
        duration = max_length_timestamp_of_speakers[speaker_label]["duration"]
        start_time = max_length_timestamp_of_speakers[speaker_label]["start_time"]
        end_time = max_length_timestamp_of_speakers[speaker_label]["end_time"]
        splited_audio_data = audio_data[(start_time * 1000):(end_time * 1000)]
        filename = "./data/vggvox/" + speaker_label + ".wav"
        splited_audio_data.export(filename, format="wav")

# transcribe_result_to_vggvox_wav() # 接在transcribe功能後面



