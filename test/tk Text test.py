import tkinter as tk
import time
import threading

window = tk.Tk()
window.title("My Window")
window.geometry("400x400")
window.resizable(width=False, height=False)

text = tk.Text(window, width=40)
text.place(x=0, y=200)
num = 1


def hit_insert():
    content = entry.get()
    text.insert("insert", content)
    text_content()


def hit_end():
    content = entry.get()
    text.insert("end", content)
    text_content()


def text_content():
    global text, num
    # 從第一行，第0個字符開始，到最後
    content = text.get("{}.0".format(num), "end")
    # 簡單實現自己跟自己說話，insert插入只能再後，不然會亂行
    content = "\n機器人:" + content
    text.insert("end", content)
    # 換行讀取
    num += 2


def text_delete():
    global num
    # 清除文本裏面的所有內容
    text.delete("1.0".format(str(num)), "end")
    # 行數也要清楚
    num = 1


# 分別將兩個按鈕回調不用的函數
button_insert = tk.Button(window, text='insert point', command=hit_insert)
button_insert.pack()
button_end = tk.Button(window, text="insert end", command=hit_end)
# 將end按鈕置於insert按鈕後面
button_end.pack(after=button_insert)
# 創建清空text的按鈕
button_delete = tk.Button(window, text="text delete", command=text_delete)
# 將delete按鈕置於end按鈕後面
button_delete.pack(after=button_end)
# 創建編輯框，以便輸入的內容，放到文本框裏
entry = tk.Entry(window)
# 將entry編輯框置於insert前面
entry.pack(before=button_insert)
# 循環窗口
window.mainloop()
