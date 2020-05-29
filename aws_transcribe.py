# -*- coding: utf-8 -*-
"""
Created on Wed May 13 10:21:37 2020

@author: 10812304
"""
import boto3
import re
import time
import json
import pandas as pd




def filename_to_time_order(x):
    y = re.sub(pattern=".wav", repl="", string=x)
    y = re.sub(pattern="meeting_", repl="", string=y)
    y = re.sub(pattern="-", repl="", string=y)
    return y


def get_last_file(s3):
    key_response = s3.list_objects(Bucket='mre500demo')
    transcribe_data = []
    for obj in key_response['Contents']:
        if obj['Key'][0:7] == 'rawData':
            transcribe_data.append(obj['Key'][8:])
    # transcribe_data = os.listdir("./data/transcribe")
    order = [filename_to_time_order(x=i) for i in transcribe_data]
    selected_transcribe_data = transcribe_data[order.index(max(order))]
    return selected_transcribe_data[:-4]


# Transcribe sample
def aws_transcribe(ID, KEY, count):
    s3 = boto3.client('s3',
                      region_name='us-east-1',
                      aws_access_key_id=ID,
                      aws_secret_access_key=KEY)

    transcribe = boto3.client('transcribe',
                              region_name='us-east-1',
                              aws_access_key_id=ID,
                              aws_secret_access_key=KEY)

    selected_transcribe_data = get_last_file(s3)
    # job_name = selected_transcribe_data
    job_name = 'transcribe' + selected_transcribe_data[7:]
    job_uri = "https://mre500demo.s3.amazonaws.com/rawData/" + selected_transcribe_data + '.wav'
    print('進行語音轉文字')
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat='wav',
        LanguageCode='en-US',  # 簡中 zh-CN, en-US
        Settings={
            'ShowSpeakerLabels': True,
            'MaxSpeakerLabels': count, # 之後成辨識
            'ShowAlternatives': False,
        },
        OutputBucketName='mre500demo'
    )

    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        print("transcribe not ready yet...")
        time.sleep(5)
    print(status)
    print('語音轉文字完成')

    # -------------------------------------------------
    # read json
    print('自s3下載json檔案')
    s3.download_file(
        Filename='data/transcribe/' + job_name + '.json',  ## local
        Bucket='mre500demo',
        Key=job_name + '.json')

    with open('data/transcribe/' + job_name + '.json', 'r', encoding='utf8') as reader:
        jf = json.loads(reader.read())

    transcripts = pd.DataFrame(jf['results']['transcripts'])
    transcripts.to_csv('data/csv/' + job_name + '.csv')
    print('上傳csv檔案')
    # 上傳全部文字的csv
    s3.upload_file(Filename='data/csv/' + job_name + '.csv',
                   Bucket='mre500demo',
                   Key='data2/' + job_name + '.csv')
    print('上傳csv檔案完成')


