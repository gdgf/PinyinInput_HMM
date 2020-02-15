from tkinter import *

from src.hmm.hmm_implement import DefaultHmmParams
from src.hmm.viterbi import viterbi

window = Tk()
window.title("拼音输入法")

strnow=''
pinyin = Entry(window, font=('times', 20, 'bold'))  # 输入框，输入时显示
pinyin.grid(row=0, column=0, sticky=W)

hanzi = Text(window, font=('times', 10, 'bold'))
hanzi.grid(row=1, column=0, sticky=W)

def show():
    # print(type(pinyin.get()))
    str1 = pinyin.get()
    s = str1.split()
    obs = tuple(list(s))
    #print(len(obs))
    hmmparams = DefaultHmmParams()
    result = viterbi(hmm_params=hmmparams, observations=obs, path_num=6)
    hanzi.delete(1.0, END)
    for item in result:
        hanzi.insert(END, str(item.score) + "  " + "".join(item.path) + "\n")

def tick():
    global strnow
    strnext = pinyin.get()
    if strnext:
        if strnext!=strnow:
            strnow=strnext
            s = strnow.split()
            obs = tuple(list(s))
            # print(obs)
            hmmparams = DefaultHmmParams()
            result = viterbi(hmm_params=hmmparams, observations=obs, path_num=6)
            hanzi.delete(1.0, END)
            for item in result:
                hanzi.insert(END, str(item.score) + "  " + "".join(item.path) + "\n")
            hanzi.after(2000, tick)
    hanzi.after(1000, tick)

Button(window, text='输入', width=10, command=show).grid(row=2, column=0,
             sticky=W, padx=10,pady=5)  # 设置 button 指定 宽度 , 并且 关联 函数 , 使用表格式布局 .

tick()
window.mainloop()
