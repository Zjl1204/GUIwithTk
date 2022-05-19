# Auther:zjl1204
# Date:2022/5/12

import xlrd
import os

from math import radians, cos, sin, asin, sqrt


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


def find_ncell_list(dis_a, dis_b, coord1):

    used_root_list = []
    used_pci_list = []
    for i in range(1,table.nrows):
        if table.cell_value(i,5) == freq:
            coord2 = (table.cell_value(i,2), table.cell_value(i,1))
            dis = cal_dis(coord1, coord2)
            if dis < dis_a:
                used_root_list.append(table.cell_value(i,4))
            if dis < dis_b:
                used_pci_list.append(table.cell_value(i,3))

    print(str(dis_a) +'KM内根序列选取小区'+ str(len(used_root_list))+'个')
    print(str(dis_b) + 'KM内PCI选取小区' + str(len(used_pci_list))+'个')
    return used_root_list, used_pci_list


def seclet_usable_ROOT(used_list):
    whole_list = list(range(0,740,4)) + list(range(740,801)) + list(range(801,840))
    indoor_list = []
    outdoor_list = []
    ext_list = []

    usable_list = (set(whole_list).difference(set(used_list)))  # 差集
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


def seclet_usable_PCI(used_list):
    whole_list = list(range(0,505))
    indoor_list = []
    outdoor_list = []
    ext_list = []

    usable_list = (set(whole_list).difference(set(used_list)))  # 差集
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




# 以下是运行流程
try:
    data = xlrd.open_workbook('Latest_LTE.xls')
    table = data.sheets()[0]
except:
    print('没有找到文件Latest_LTE.xls')
    os.system('pause')


# 找到未规划行的经纬度，频段
n = 1
while True:
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

    while True:
        print('筛选 ' + table.cell_value(n, 0) + ' '+ freq + ' 根序列和PCI')
        while True:
            try:
                Root_dis = float(input('输入根序列不复用距离（KM）：'))
                break
            except ValueError:
                print('请输入数字！')
        while True:
            try:
                PCI_dis = float(input('输入PCI不复用距离（KM）：'))
                break
            except ValueError:
                print('请输入数字！')

        ncell_list = find_ncell_list(Root_dis, PCI_dis, coord1)
        a, b = seclet_usable_ROOT(ncell_list[0]), seclet_usable_PCI(ncell_list[1])


        print('根序列可选')
        if site_type == '室内':
            print('室内：',a[0])
        if site_type == '室外':
            print('室外：',a[1])
        print('预留：',a[2])
        print('\nPCI可选')

        if site_type == '室内':
            print('室内：',b[0])
        if site_type == '室外':
            print('室外：',b[1])
        print('预留：',b[2])
        print('\n选取合适的根序列和PCI，填入表格并保存后，重新运行程序进行下一个小区的规划。\n')

        next_comand = input('输入1回车完成，输入其它重新设置距离\n')
        if next_comand == '1':
            n = n+1
            continue
        os.system('cls')
