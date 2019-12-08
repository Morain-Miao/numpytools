#!C:\Python34\python.exe
# -*- coding: utf-8 -*-


from tkinter import *
from tkinter import scrolledtext  # 导入带滚动条文本框
from tkinter import messagebox  # 导入弹窗模块
from tkinter import ttk
import threading  # 导入多线程模块
import difflib
import numpy as np
import random

window = Tk()
window.title('Numpy练习小程序---------by Gupao.Mr Miao')
window.geometry('1440x976')
# ↓定义带滚动条文本框1、2，所属A、B列，用于提供两列待对比的内容↓
# t1代表新架构时间点文件路径文本框
l1 = Label(window, text='题型：')
l1.place(x=50, y=5)

# 创建下拉菜单
cmb = ttk.Combobox(window)
cmb.pack()
cmb.grid(padx=50, pady=30)
# 设置下拉菜单中的值
cmb['value'] = ('根据代码给结果', '根据结果给出代码')
# 设置默认值，即默认下拉框中的内容  默认值中的内容为索引，从0开始
cmb.current(0)
l6 = Label(window, text='维度设置：')
l6.place(x=400, y=100)
t1 = Entry(window)
t1.grid(padx=460, pady=20)
t1.insert('end', '1')
# t2代表老架构时间点文件路径文本框
l2 = Label(window, text='生成题目：')
l2.place(x=800, y=5)
t2 = scrolledtext.ScrolledText(window, height=5, width=80)
t2.place(x=800, y=30)

l3 = Label(window, text='你的答案：')
l3.place(x=50, y=170)
# 要比对的内容文本框
t3 = scrolledtext.ScrolledText(window, height=5, width=80)
t3.place(x=50, y=200)

# 错误信息文本框
l4 = Label(window, text='正确答案：')
l4.place(x=800, y=170)
t4 = scrolledtext.ScrolledText(window, height=5, width=80)
t4.place(x=800, y=200)

# ↑定义带滚动条文本框1、2，所属A、B列↑
# ↓定义带滚动条文本框，用于显示对比后的结果↓
l5 = Label(window, text='数组显示：')
l5.place(x=50, y=270)
t5 = scrolledtext.ScrolledText(window, height=50, width=190)
t5.place(x=50, y=300)
# ↑定义带滚动条文本框，用于显示对比后的结果↑
# ↓定义5个单选按钮↓
'''
rvalue=StringVar()  #第一组单选按钮
r1=Radiobutton(window,text='A→B',variable=rvalue,value='r1value1',indicatoron=False)
r1.place(x=480,y=130)
r2=Radiobutton(window,text='A←B',variable=rvalue,value='r2value2',indicatoron=False)
r2.place(x=580,y=130)
r3=Radiobutton(window,text='A←→B',variable=rvalue,value='r3value3',indicatoron=False)
r3.place(x=680,y=130)
'''

# v = StringVar()  #第二组单选按钮
# v.set("L")  #使第二组单选按钮有互斥效果
OnlyRedioStatus = IntVar()
OnlyRedioStatus.set(1)

r4 = Radiobutton(window, variable=OnlyRedioStatus, text='索引模式', value=1)
r4.place(x=250, y=30)
r5 = Radiobutton(window, variable=OnlyRedioStatus, text='切片模式', value=2)
r5.place(x=350, y=30)
r6 = Radiobutton(window, variable=OnlyRedioStatus, text='切片+索引模式', value=3)
r6.place(x=100, y=30)



# 全局变量
# 提示形状
prompt_shape = None
answer_result = None


# 根据形状得到数组
def generate_array(array_shape):
    try:
        # 求乘积
        prod_number = np.prod(tuple(array_shape))
        x = np.arange(prod_number).reshape(tuple(array_shape))
        return x
    except TypeError:
        x = np.arange(array_shape).reshape(array_shape)
        return x


# 随机1-5维array
def generate_numpy(axis_num=1, shuffle=True):
    # x = np.arange(120).reshape(2,3,4,5)
    # 2-8之间取2行3列整数
    # a = np.random.randint(2,8,size=(2,3))
    array_shape_list = []
    for i in range(axis_num):
        rand_num = np.random.randint(1, 9)
        array_shape_list.append(rand_num)
    result_array = generate_array(array_shape_list)
    if shuffle:
        # 打乱的索引序列，默认对第一维打乱
        result_array = np.random.permutation(result_array)
    t5.insert('end', '%s' % result_array)
    return result_array


# 传入数组的形状，得到随机索引或者切片或者索引+切片
def get_random_index_or_slice(array_shape, flag='index'):
    shape_list = []
    if array_shape.__len__() > 1:
        lenth = np.random.randint(1, array_shape.__len__() + 1)
        print('题目长度：' + str(lenth))
    else:
        lenth = 1
    for index in range(lenth):
        if flag == 'index_and_slice':
            shuffle_flag = np.random.randint(0, 2)
        else:
            shuffle_flag = 0
        if flag == 'index' or int(shuffle_flag) == 1:
            x = np.random.randint(0, array_shape[index])
        else:
            while True:
                start = np.random.randint(0, array_shape[index])
                end = np.random.randint(0, array_shape[index])+1
                if end > start:
                    x = slice(start, end)
                    break
                elif array_shape.__len__() == 1 and array_shape[0] == 1:
                    x = slice(start, end)
                    break
        shape_list.append(x)
    return shape_list


# 自动生成题目
def generate_subject(result_array):
        shape_list = []
        global prompt_shape
        global answer_result
        array_shape = result_array.shape # 得到当前数组形状
        print('生成的数组形状：' + str(result_array.shape))
        prompt_shape = result_array.shape
        if OnlyRedioStatus.get() == 1:  # 索引模式
            shape_list = get_random_index_or_slice(array_shape,'index')
        elif OnlyRedioStatus.get() == 2:  # 切片模式
            shape_list = get_random_index_or_slice(array_shape,'slice')
        elif OnlyRedioStatus.get() == 3:  # 混合模式
            shape_list = get_random_index_or_slice(array_shape, 'index_and_slice')
        t2.delete(1.0, END)
        t4.delete(1.0, END)
        if str(shape_list).find('slice'):
            shape_list_str = slice_str(shape_list)
        else:
            shape_list_str = str(shape_list)
        if cmb.get() == '根据代码给结果':
            print('题目：'+str(shape_list))
            # [slice(0, 3, None), slice(1, 5, None)]
            t2.insert('end','%s' % shape_list_str)
            print('答案：'+str(result_array[tuple(shape_list)]))
            answer_result = result_array[tuple(shape_list)]
            # t4.insert('end', '%s' % str(result_array[tuple(shape_list)]))
        elif cmb.get() == '根据结果给出代码':
            print('答案：' + shape_list_str)
            # t4.insert('end', '%s' % str(shape_list))
            answer_result = shape_list_str
            print('题目：' + str(result_array[tuple(shape_list)]))
            t2.insert('end', '%s' % str(result_array[tuple(shape_list)]))
        return result_array[tuple(shape_list)]  # 3


def slice_str(shape_list):
    slice_list = str(shape_list).replace('[', '').replace(']', '').replace(', None', '').replace('(', '').replace(')',
                                                                                                                  '').strip().split(
        ", slice")
    slice_result_list = []
    for line in slice_list:
        line = line.replace('slice', '').replace(',', ':')
        slice_result_list.append(line)
    return slice_result_list.__str__().replace('\'', '').replace(' ', '')


# 提示形状
def prompt():
    t4.delete(1.0, END)
    t4.insert('end', '形状：%s' % str(prompt_shape))


# 显示答案
def answer():
    t4.delete(1.0, END)
    t4.insert('end', '答案：%s' % str(answer_result))


def pipeline():
    axis_num = int(t1.get())
    generate_subject(generate_numpy(axis_num))


def start_thread():  # 开启线程
    # 每次调用清空错误信息文本框
    t4.delete(1.0, END)  # 错误信息文本框
    t5.delete(1.0, END)  # 结果文本框
    added_thread1 = threading.Thread(target=pipeline())
    added_thread1.start()


def help_info():
    messagebox.showinfo(title='使用说明', message='1.如界面，输入要比对时间点文件的绝对路径\n2.标点请使用英文标点\n3.点击开始比对')


# ↓定义一个按钮↓
b = Button(window, text='使用说明', command=help_info)
b.place(x=300, y=100)
b = Button(window, text='开始出题', command=start_thread)
b.place(x=200, y=100)

b = Button(window, text='提示形状', command=prompt)
b.place(x=900, y=160)
b = Button(window, text='显示答案', command=answer)
b.place(x=1000, y=160)
# ↑定义一个按钮↑
window.mainloop()
