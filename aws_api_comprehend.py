# -*- coding: utf-8 -*-
"""
Created on Wed May 27 13:46:44 2020

@author: 10711304
"""
import boto3
import re
import time
import json
import pandas as pd
import os
import tarfile


def filename_to_time_order(x):
    y = re.sub(pattern = ".wav", repl = "", string = x)
    y = re.sub(pattern = "meeting_", repl = "", string = y)
    y = re.sub(pattern = "-", repl = "", string = y)
    return(y)


def comprehend(ID, KEY):
    s3 = boto3.client('s3',
                      region_name='us-west-1',
                      aws_access_key_id=ID,
                      aws_secret_access_key=KEY)

    key_response = s3.list_objects(Bucket='mre500demo')
    transcribe_data = []
    for obj in key_response['Contents']:
        if obj['Key'][0:5] == 'data2':
            transcribe_data.append(obj['Key'][6:])

    order = [filename_to_time_order(x = i) for i in transcribe_data]
    selected_transcribe_data = transcribe_data[order.index(max(order))][:-4]

    comprehend = boto3.client('comprehend',
                          region_name='us-east-1',
                          aws_access_key_id=ID,
                          aws_secret_access_key=KEY)

    a = comprehend.start_entities_detection_job(
        JobName=selected_transcribe_data,
        LanguageCode='en',  # zh,
        DataAccessRoleArn='arn:aws:iam::240089488493:role/service-role/AmazonComprehendServiceRole-mre500demo',
        InputDataConfig={
            'S3Uri': 's3://mre500demo/data2/' + selected_transcribe_data + '.csv',
            'InputFormat': 'ONE_DOC_PER_FILE'
        },
        OutputDataConfig={
            'S3Uri': 's3://mre500demo/data3/' + selected_transcribe_data,
        })

    print('run comprehend')

    while True:
        response = comprehend.describe_entities_detection_job(JobId=a['JobId'])
        if response['EntitiesDetectionJobProperties']['JobStatus'] in ['COMPLETED', 'FAILED']:
            break
        print("comprehend not ready yet...")
        time.sleep(5)

    # ------------------------------------------------------------------------------
    key_response2 = s3.list_objects(Bucket='mre500demo')
    transcribe2_data = []
    for obj in key_response2['Contents']:
        if obj['Key'][0:5] == 'data3':
            transcribe2_data.append(obj['Key'][6:])

    order2 = [filename_to_time_order(x = i) for i in transcribe2_data]
    selected_transcribe2_data = transcribe2_data[order2.index(max(order2))]
    print(selected_transcribe2_data)


    s3.download_file(
            Filename = './data/comph/' + selected_transcribe_data +'.tar.gz', ## local
            Bucket = 'mre500demo',
            Key = 'data3/'+selected_transcribe2_data)


    with tarfile.open('./data/comph/' + selected_transcribe_data +'.tar.gz') as tf:
      tf.extractall()

    os.rename('output','./data/comph/' + selected_transcribe_data +'.json')
    # ------------------------------------------------------------------------------
    ## choose topic words
    with open('./data/comph/' + selected_transcribe_data +'.json' , 'r') as reader:
        jf = json.loads(reader.read())

    topic_word = []
    score = []
    for text in jf['Entities']:
        if text['Text'] not in topic_word:
            topic_word.append(text['Text'])
            score.append(text['Score'])
    topic_word = pd.DataFrame({'topic_word': topic_word, 'score':score})
    topic_word = topic_word[['topic_word', 'score']]
    # selected_transcribe_data.replace('transcribe', 'keyword')
    topic_word.to_csv('./data/comph/' + selected_transcribe_data.replace('transcribe', 'keyword') + '.csv', header=False, index=False, encoding="utf-8")
    topic_word.to_csv('./data/report/' + selected_transcribe_data.replace('transcribe', 'keyword',) + '.csv', header=False, index=False, encoding="utf-8")
    print('comprehend done.')
# comprehend()