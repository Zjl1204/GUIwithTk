# -*- coding:utf-8 -*-
# Author:zjl1204
import os
from tkinter import *

from math import radians, cos, sin, asin, sqrt

import tkinter.filedialog
import xlrd



# mean earth radius - https://en.wikipedia.org/wiki/Earth_radius#Mean_radius
_AVG_EARTH_RADIUS_KM = 6371.0088


def cal_dis(point1, point2):

    # unpack latitude/longitude
    lat1, lng1 = point1
    lat2, lng2 = point2

    # convert all latitudes/longitudes from decimal degrees to radians
    lat1 = radians(lat1)
    lng1 = radians(lng1)
    lat2 = radians(lat2)
    lng2 = radians(lng2)

    # calculate haversine
    lat = lat2 - lat1
    lng = lng2 - lng1
    d = sin(lat * 0.5) ** 2 + cos(lat1) * cos(lat2) * sin(lng * 0.5) ** 2

    return 2 * _AVG_EARTH_RADIUS_KM * asin(sqrt(d))


def seclet_usable_ROOT(Root_dis, coord1, table, freq):
    whole_list = list(range(0, 740, 4)) + list(range(740, 801)) + list(range(801, 840))
    indoor_list = []
    outdoor_list = []
    ext_list = []

    used_root_list = []
    for i in range(1, table.nrows):
        if table.cell_value(i, 5) == freq:
            coord2 = (table.cell_value(i, 2), table.cell_value(i, 1))
            dis = cal_dis(coord1, coord2)
            if dis < Root_dis:
                used_root_list.append(table.cell_value(i, 4))

    usable_list = (set(whole_list).difference(set(used_root_list)))  # 差集
    for i in usable_list:
        if i in whole_list[186:247]:
            indoor_list.append(i)
        if i in whole_list[0:186]:
            outdoor_list.append(i)
        else:
            ext_list.append(i)

    indoor_list.sort()
    outdoor_list.sort()
    ext_list.sort()

    return indoor_list, outdoor_list, ext_list


def seclet_usable_PCI(PCI_dis, coord1, table, freq):
    whole_list = list(range(0,505))
    indoor_list = []
    outdoor_list = []
    ext_list = []
    used_pci_list = []

    for i in range(1, table.nrows):
        if table.cell_value(i, 5) == freq:
            coord2 = (table.cell_value(i, 2), table.cell_value(i, 1))
            dis = cal_dis(coord1, coord2)
            if dis < PCI_dis:
                used_pci_list.append(table.cell_value(i, 3))

    usable_list = (set(whole_list).difference(set(used_pci_list)))  # 差集
    for i in usable_list:
        if i in whole_list[360:479]:
            indoor_list.append(i)
        if i in whole_list[0:360]:
            outdoor_list.append(i)
        else:
            ext_list.append(i)

    indoor_list.sort()
    outdoor_list.sort()
    ext_list.sort()

    return indoor_list, outdoor_list, ext_list


def is_continuous_list(list1):
    c = 0
    for i in range(len(list1)-2):
        if (list1[i+2] - list1[i+1] == 1) and (list1[i+1] - list1[i] == 1):
            c += 1
    return c


def find_best_root_list(coord1, freq, table, st):
    Root_dis = 10.0
    while True:
        if st == '室分':
            a = seclet_usable_ROOT(Root_dis, coord1, table, freq)[0]
        if st == '室外':
            a = seclet_usable_ROOT(Root_dis, coord1, table, freq)[1]
        if len(a) == 0:
            Root_dis -= 0.2
            continue
        if len(a) > 5:
            Root_dis += 1
            continue
        if Root_dis >= 30:
            break
        break
    t = st+'站 可选根序列 '+str(round(Root_dis, 2))+' KM'
    lb6.config(text=t)
    print('根序列距离：' + str(round(Root_dis, 2)) + ' KM')
    print('可选根序列：', a)
    return a


def find_best_pci_list(coord1, freq, table, st):
    PCI_dis = 10.0
    c = 0
    while True:
        if st == '室分':
            a = seclet_usable_PCI(PCI_dis, coord1, table, freq)[0]
        if st == '室外':
            a = seclet_usable_PCI(PCI_dis, coord1, table, freq)[1]
        if len(a) < 3:
            PCI_dis -= 0.3
            continue
        if is_continuous_list(a) == 0:
            c += 1
            if c > 1000:
                print('找不到3个连续的PCI')
                break
            PCI_dis -= 0.1
            continue
        if is_continuous_list(a) == 1:
            break
        if is_continuous_list(a) > 1:
            PCI_dis += 1
            continue
        if PCI_dis >= 30:
            break
        break

    t1 = st+'站 可选PCI '+str(round(PCI_dis, 2))+' KM'
    lb5.config(text=t1)
    print('PCI距离：' + str(round(PCI_dis, 2)) + ' KM')
    print('可选PCI:', a)
    return a


# 调用Tk()创建主窗口
root_window = Tk()
root_window.title('筛选根序列和PCI')
# 窗口大小
root_window.geometry('800x400')
# 图标
root_window.iconbitmap('icon.ico')


# 定义一个处理文件的相关函数
def askfile():
    # 从本地选择一个文件，并返回文件的目录
    filename = tkinter.filedialog.askopenfilename()
    if filename != '':
         lb1.config(text=filename)

    else:
         lb1.config(text='您没有选择任何文件')


# 定义一个运行函数
def run_fun():
    text_GenXvLie.delete('1.0', 'end')
    text_PCI.delete('1.0', 'end')
    a = find_fun()
    text_PCI.insert(INSERT, str(a[0]))
    text_PCI.insert(END, '\n模三')
    text_PCI.insert(INSERT, str(list(map(lambda x: x % 3, a[0]))))
    text_GenXvLie.insert(INSERT, str(a[1]))


def find_fun():
    f_path = lb1['text']
    print(f_path)
    # 打开文件
    data = xlrd.open_workbook(f_path)
    table = data.sheets()[0]
    # 找到未规划行的经纬度，频段
    n = 1
    while True:
        try:
            if table.cell_value(n, 3) == xlrd.empty_cell.value:
                break
            n = n + 1
        except IndexError:
            print("没有未规划PCI的小区")

    site_type = table.cell_value(n, 7)
    freq = table.cell_value(n, 5)
    coord1 = (table.cell_value(n, 2), table.cell_value(n, 1))
    text1 = '筛选 ' + table.cell_value(n, 0) + ' ' + site_type + freq + ' 根序列和PCI'
    lb7.config(text=text1)
    b = find_best_root_list(coord1, freq, table, site_type)
    a = find_best_pci_list(coord1, freq, table, site_type)
    return a, b


# 在主窗口上添加一个frame控件
frame1 = Frame(root_window)
frame1.pack()
frame_in = Frame(frame1)
frame_in.pack(side=TOP, anchor=W)

frame_YX = Frame(frame1)
frame_YX.pack(side=BOTTOM, anchor='center')
btn2 = Button(frame_YX, text='运行', command=run_fun)
btn2.grid(row=0, column=0, padx=5)

frame_show = Frame(frame1)
frame_show.pack(side=TOP, anchor=W)

btn1 = Button(frame_in, text='选择文件', relief=RAISED, command=askfile)
btn1.pack(side=TOP, anchor=W)

lb1 = Label(frame_in, text='', bg='#87CEEB')
lb1.pack(side=TOP, anchor=W)

# # 可以使用动态标签比较帅，但是没必要
# lb2 = Label(frame_in, text='根序列距离：', bg='gray')
# lb2.grid(row=1, column=0, padx=5)
# lb3 = Label(frame_in, text='PCI距离：', bg='gray')
# lb3.grid(row=2, column=0, padx=5)
# entry1 = Entry(frame_in)
# entry1.grid(row=1, column=1, padx=5)
# entry2 = Entry(frame_in)
# entry2.grid(row=2, column=1, padx=5)
# lb3 = Label(frame_in, text='KM', bg='gray')
# lb3.grid(row=1, column=2, padx=5)
# lb4 = Label(frame_in, text='KM', bg='gray')
# lb4.grid(row=2, column=2, padx=5)

lb5 = Label(frame_show, text='可选根序列', bg='#87CEEB')
lb5.grid(row=0, column=0)
lb6 = Label(frame_show, text='可选PCI', bg='#87CEEB')
lb6.grid(row=0, column=1)
lb7 = Label(frame_in, text='', bg='pink')
lb7.pack(side=TOP, anchor=W)

# 创建一个文本控件
# width 一行可见的字符数；height 显示的行数
text_PCI = Text(frame_show, width=50, height=6)
text_PCI.grid(row=1, column=0, padx=2)
text_GenXvLie = Text(frame_show, width=50, height=6)
text_GenXvLie.grid(row=1, column=1, padx=2)

# 开启主循环，让窗口一直显示
root_window.mainloop()

