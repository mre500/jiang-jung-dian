from tkinter import ttk
from tkinter import filedialog
from pyaudio import PyAudio, paInt16
from tkinter import messagebox
from build_folder import make_dir
from upload_s3 import load_lastest_recog_wav
from aws_transcribe import aws_transcribe
from AmazonTranscribe_to_VGGVox import transcribe_result_to_vggvox_wav
from vggknot import enrollWrapper, recognizer, replaceName
from aws_api_comprehend import comprehend
import os
import time
import tkinter as tk
import threading
import wave
import subprocess

# 錄音相關參數
framerate = 8000
NUM_SAMPLES = 2000
channels = 1
sampwidth = 2
TIME = 2

# 建立資料夾
make_dir()

# 控制執行續事件
stop_event = threading.Event()

# amzon 金鑰
ID = ""
KEY = ""

class Threader(threading.Thread):
    def __init__(self, u, language, text, action, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        self.daemon = True
        self.user = u
        self.language = 'cn' if language == '中文' else 'en'
        self.text = text
        self.action = action

        self.start()

    def save_wave_file(self, filename, data):
        '''
            save the data to the wav file
        '''
        wf = wave.open(filename, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(sampwidth)
        wf.setframerate(framerate)
        wf.writeframes(b"".join(data))
        wf.close()

    def run(self):
        stop_event.clear()  # reset event
        if self.user == '':
            messagebox.showinfo("提示", "請輸入使用者名稱")
            return

        messagebox.showinfo("提示", "點選結束錄製可終止錄音")
        pa = PyAudio()
        stream = pa.open(format=paInt16, channels=1,
                         rate=framerate, input=True,
                         frames_per_buffer=NUM_SAMPLES)
        my_buf = []
        while True:
            if stop_event.is_set():
                break
            string_audio_data = stream.read(NUM_SAMPLES)
            my_buf.append(string_audio_data)
            print('錄製中...')
        print('已儲存檔案')
        file_name = None
        if self.action == 'enroll':
            file_name = 'data/enroll/wav/{}_{}.wav'.format(self.user, self.language)
        elif self.action == 'recog':
            file_name = 'data/recog/meeting_' + time.strftime("%Y-%m%d-%H%M%S", time.localtime()) + '.wav'

        get_user_information(self.user, file_name, self.text)  # text 顯示註冊畫面
        self.save_wave_file(file_name, my_buf)  # 寫入音訊檔案

        if self.action == 'recog':
            # 將會議影片上傳至s3
            print('將會議影片上傳至s3')
            load_lastest_recog_wav(ID=ID, KEY=KEY, BUCKET="mre500demo")

            # 進行transcribe，計算會議人數

            # count = max(len(os.listdir('data/enroll/wav')),
            #             len([x for x in self.text.get('1.0', 'end').split('\n') if x != '']))
            count = len(os.listdir('data/enroll/wav'))
            print('會議人數', count)
            aws_transcribe(ID, KEY, count)

            # 前處理，切音檔
            transcribe_result_to_vggvox_wav()

            # 語者辨識
            print('開始進行語音辨識')
            Speaker_IDs, speakers = recognizer()

            # 把speak id 取代成名子
            print('把speak id 取代成名子')
            replaceName(Speaker_IDs, speakers)

            # 執行關鍵詞擷取
            comprehend(ID, KEY)

            # 製作報告
            call_shiny()

        stream.close()


def click():
    # enrollWrapper(folderpath="data/enroll/wav/")
    # 將會議影片上傳至s3
    # ID = "AKIATPZTS3RW53DJBFDU"
    # KEY = "XbbEKJRHSWpy0sdRD5vfhzRpkdA+j3DGYxxkJtlV"
    # load_lastest_recog_wav(ID=ID, KEY=KEY, BUCKET="mre500demo")

    # 進行transcribe，計算會議人數

    # print('會議人數', 2)
    # aws_transcribe(ID, KEY, 2)
    #
    # 前處理，切音檔
    # transcribe_result_to_vggvox_wav()

    # 語者辨識
    print('開始進行語音辨識')
    Speaker_IDs, speakers = recognizer()

    # 把speak id 取代成名子
    print('把speak id 取代成名子')
    replaceName(Speaker_IDs, speakers)

    # 執行關鍵詞擷取
    comprehend(ID, KEY)

    # 製作報告
    call_shiny()


def UploadAction(entry_text, event=None):
    filename = filedialog.askopenfilename()
    print('Selected:', filename)
    entry_text.set(filename)


def get_user_information(user_text, entey_text, text):
    text.insert('end', '{} {}\n'.format(user_text, entey_text))


def setTextInput(text):
    print(enroll_text_list)
    print(text)
    enroll_text_list.insert(1.0, text)


def call_shiny():
    process = subprocess.Popen(r"shiny.bat", stderr=subprocess.PIPE)
    print("call shiny to show result")
    if process.stderr:  # 把 exe 執行出來的結果讀回來
        print("**************************************************************")
        print(process.stderr.readlines())
        print("**************************************************************")
    print("End of program")


if __name__ == '__main__':
    window = tk.Tk()
    window.title('講重點')
    window.geometry('500x350')
    window.resizable(0, 0)

    # 輸入使用者名稱
    user = tk.Label(window, text='使用者名稱').place(x=0, y=0)
    user_text = tk.StringVar()  # 記錄使用者的名稱
    user_entry = tk.Entry(window, bd=1, width=10, textvariable=user_text,).place(x=80, y=0)



    # 建立註冊元件
    enroll = tk.Label(window, text='選擇語言').place(x=0, y=30)
    combo = ttk.Combobox(window, values=['中文', '英文'],
                         state="readonly")
    combo.place(x=80, y=30)


    # 瀏覽檔案
    # entry_text = tk.StringVar()  # 用來控制entry顯示上傳檔案的路徑
    # file_entry = tk.Entry(window, bd=1, width=20, textvariable=entry_text,
    #                       state='readonly').place(x=160, y=50)
    # browse_button = tk.Button(window, text='瀏覽', command=partial(UploadAction, entry_text)).place(x=320, y=45)

    # 顯示出註冊的名單
    enroll_user_label = tk.Label(window, text='已註冊語者清單').place(x=0, y=75)
    enroll_text_list = tk.Text(window, height=10, width=50)
    enroll_text_list.place(x=50, y=100)
    # upload_file = tk.Button(window, text='上傳', command=partial(get_user_information,
    #                                                             user_text,
    #                                                             entry_text,
    #                                                             enroll_text_list)).place(x=370, y=45)

    # 插入水平線
    line1 = ttk.Separator(window,).place(x=0, y=250, relwidth=1)

    # 開始錄製按鈕
    # record_label = tk.Label(window, text='Record').place(x=150, y=260)
    record_button = tk.Button(window, text='開始錄音', command=lambda: Threader(user_text.get(),
                                                                            combo.get(),
                                                                            enroll_text_list,
                                                                            action='enroll')).place(x=250, y=25)
    record_stop_button = tk.Button(window, text='結束錄音', command=stop_event.set).place(x=320, y=25)
    test_button = tk.Button(window, text='開始辨識', command=click).place(x=390, y=25)

    # 插入水平線
    # line2 = ttk.Separator(window,).place(x=0, y=290, relwidth=1)

    # 開始辨識
    recognition_label = tk.Label(window, text='Recognition').place(x=0, y=260)
    recognition_button = tk.Button(window, text='會議錄音', command=lambda: Threader(user_text.get(),
                                                                            combo.get(),
                                                                            enroll_text_list,
                                                                            action='recog'))
    recognition_button.place(x=80, y=255)
    recognition_stop_button = tk.Button(window, text='結束會議', command=stop_event.set).place(x=165, y=255)

    window.mainloop()
