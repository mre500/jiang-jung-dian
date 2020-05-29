# -*- coding: UTF-8 -*-
import subprocess


def call_shiny():
    process = subprocess.Popen(r"shiny.bat", stderr=subprocess.PIPE)
    print("call shiny to show result")
    if process.stderr:  # 把 exe 執行出來的結果讀回來
        print("**************************************************************")
        print(process.stderr.readlines())
        print("**************************************************************")
    print("End of program")
