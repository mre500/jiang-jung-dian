import boto3
import os
import re


def filename_to_time_order(x):
    y = re.sub(pattern=".wav", repl="", string=x)
    y = re.sub(pattern="meeting_", repl="", string=y)
    y = re.sub(pattern="-", repl="", string=y)
    return y


def load_lastest_recog_wav(ID, KEY, BUCKET="mre500demo"):
    recog_data = os.listdir("./data/recog")
    order = [filename_to_time_order(x=i) for i in recog_data]
    selected_data = recog_data[order.index(max(order))]

    filename = "./data/recog/" + selected_data
    keyname = "rawData/" + selected_data

    s3 = boto3.client("s3",
                      region_name="us-east-1",
                      aws_access_key_id=ID,
                      aws_secret_access_key=KEY)
    s3.upload_file(Filename=filename,
                   Bucket=BUCKET,
                   Key=keyname)



