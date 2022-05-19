# -*- coding:utf-8 -*-
# Author:zjl1204


from tkinter import *
import tkinter.filedialog


# 调用Tk()创建主窗口
root_window = Tk()
root_window.title('筛选根序列和PCI')
# 窗口大小
root_window.geometry('800x300')
# 图标
root_window.iconbitmap('icon.ico')


# 定义一个处理文件的相关函数
def askfile():
    # 从本地选择一个文件，并返回文件的目录
    filename = tkinter.filedialog.askopenfilename()
    if filename != '':
         lb1.config(text= filename)
    else:
         lb1.config(text='您没有选择任何文件')


# 在主窗口上添加一个frame控件
frame1 = Frame(root_window)
frame1.pack()
frame_in = Frame(frame1)
frame_in.pack(side=TOP, anchor=W)

frame_YX = Frame(frame1)
frame_YX.pack(side=BOTTOM, anchor='center')
btn2 = Button(frame_YX, text='运行')
btn2.grid(row=0, column=0, padx=5)

frame_show = Frame(frame1)
frame_show.pack(side=TOP, anchor=W)

btn1 = Button(frame_in, text='选择文件', relief=RAISED, command=askfile)
btn1.grid(row=0, column=0)
lb1 = Label(frame_in, text='', bg='#87CEEB')
lb1.grid(row=0, column=1, padx=5)
lb2 = Label(frame_in, text='根序列距离：', bg='gray')
lb2.grid(row=1, column=0, padx=5)
lb3 = Label(frame_in, text='PCI距离：', bg='gray')
lb3.grid(row=2, column=0, padx=5)
entry1 = Entry(frame_in)
entry1.grid(row=1, column=1, padx=5)
entry2 = Entry(frame_in)
entry2.grid(row=2, column=1, padx=5)
lb3 = Label(frame_in, text='KM', bg='gray')
lb3.grid(row=1, column=2, padx=5)
lb4 = Label(frame_in, text='KM', bg='gray')
lb4.grid(row=2, column=2, padx=5)

lb5 = Label(frame_show, text='可选根序列', bg='#87CEEB')
lb5.grid(row=0, column=0)
lb6 = Label(frame_show, text='可选PCI', bg='#87CEEB')
lb6.grid(row=0, column=1)
# 创建一个文本控件
# width 一行可见的字符数；height 显示的行数
text_GenXvLie = Text(frame_show, width=50, height=6)
text_GenXvLie.grid(row=1, column=0)
text_PCI = Text(frame_show, width=50, height=6)
text_PCI.grid(row=1, column=1)

# 开启主循环，让窗口一直显示
root_window.mainloop()
