import os
import shutil

# 建立資料夾
def make_dir():
    if os.path.isdir("./data"):
        shutil.rmtree("./data")
    if not os.path.isdir("./data"):
        os.mkdir("./data")
    if not os.path.isdir("./data/enroll"):
        os.mkdir("./data/enroll")
    if not os.path.isdir("./data/recog"):
        os.mkdir("./data/recog")
    if not os.path.isdir("./data/enroll/wav"):
        os.mkdir("./data/enroll/wav")
    if not os.path.isdir("./data/enroll/csv"):
        os.mkdir("./data/enroll/csv")
    if not os.path.isdir("./data/transcribe"):
        os.mkdir("./data/transcribe")
    if not os.path.isdir("./data/vggvox"):
        os.mkdir("./data/vggvox")
    if not os.path.isdir("./data/comph"):
        os.mkdir("./data/comph")
    if not os.path.isdir("./data/csv"):
        os.mkdir("./data/csv")
    if not os.path.isdir('./data/report'):
        os.mkdir('./data/report')

