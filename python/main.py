import tkinter
import tkinter as tk
from tkinter import END
from tkinter import messagebox
import windnd
from tkinter import ttk
import threading
import ctypes
from ctypes import *    #pip ctypes库，并导入库


#全局变量
window = tk.Tk()                                #定义一个窗口对象
var_usr_file = tk.StringVar()
file_path = ""
test = CDLL("G:/c.dll")    

#密码
def mima():
    test.jiemi.restype = ctypes.c_char_p  # 改变函数返回值
    result = test.jiemi(FileName1)
    str1 = str(ctypes.c_char_p(result).value)  # 打印结果
    #print(str1)
    return str1[2:8]

#提取
def Ctq():
    size = int(File_extract1_size.get())
    section = duanname(FileName1)[0]

    num = 0
    for i in range(len(section)):
        if section[i] == File_extract1_section.get():
            num = i
            break
    num = num + 1
    test.tiqu(FileName1, num, size)
    tk.messagebox.showinfo(title='提示', message="信息提取成功")
    pass

#隐藏
def Cyc():
    Password = File_hide_pwd.get().encode('utf-8')
    Plaintext = entry_File_hide_text.get(1.0, END).encode('utf-8')[:-1]
    section = duanname(FileName)[0]
    #print(section)
    num = 0
    for i in range(len(section)):
        if section[i] == File_hide_section.get():
            num = i
            break
    num = num + 1
    test.jiami(Password, Plaintext, FileName, num)
    tk.messagebox.showinfo(title='提示', message="信息隐藏成功")

# 节表名
def duanname(file):
    test.duan_name.restype = ctypes.c_char_p  # 改变函数返回值
    result = test.duan_name(file)
    str0 = str(ctypes.c_char_p(result).value)  # 打印结果
    #print(str0)
    section = str0.split('@')
    section[0] = section[0][2:]
    del section[-1]
    #print(section)
    name = []
    number = []

    for i in range(len(section)):
        if i % 2 == 0:
            name.append(section[i])
        else:
            number.append(section[i])

    # print(name)
    # print(number)
    PE = []
    PE.append(name)
    PE.append(number)
    return PE

#隐藏窗口显示最前
def File_hide_handler():
    window.attributes("-disabled", 0)
    File_hide_win.destroy()

#提取窗口显示最前
def File_extract_handler():
    window.attributes("-disabled", 0)
    File_extract_win.destroy()

#提取窗口显示最前
def File_extract1_handler():
    window.attributes("-disabled", 0)
    File_extract1_win.destroy()

#多线程
def thread():
    while True:
        str_text = entry_File_hide_text.get(1.0, END)
        str_size = '您还可以输入' + str(5 - (len(str_text) - 1)) + "个字符"
        tk.Label(File_hide_win, text=str_size).place(x=80, y=320)
        if len(str_text) > 5:
            entry_File_hide_text.configure(state='disabled')  # 只读

    pass

#文件隐藏
def File_hide(file):
    global File_hide_win
    global File_hide_pwd
    global File_hide_section
    global File_hide_size
    global entry_File_hide_text
    global str_text
    global FileName

    FileName = file.encode('utf-8')
    PE = duanname(FileName)
    section = PE[0]
    number = PE[1]

    tk.messagebox.showinfo(title='提示', message="密码设置长度为6")

    File_hide_win = tk.Toplevel(window)
    File_hide_win.title('hide')                  # 窗口标题
    File_hide_win.geometry('600x430+550+200')      # 窗口大小和显示位置
    File_hide_win.resizable(False, False)          # 禁止用户调整窗口大小
    window.attributes("-disabled", 1)
    File_hide_win.protocol("WM_DELETE_WINDOW", File_hide_handler)

    File_hide_pwd = tk.StringVar()
    File_hide_section = tk.StringVar()
    File_hide_size = tk.StringVar()

    tk.Label(File_hide_win, text='设置密码:').place(x=80, y=30)
    tk.Label(File_hide_win, text='选择区段:').place(x=80, y=80)
    tk.Label(File_hide_win, text='隐藏的空间:').place(x=310, y=80)
    tk.Label(File_hide_win, text='要隐藏的数据:').place(x=80, y=120)

    def show(event):
        a = 0
        for i in range(len(section)):
            if section[i] == File_hide_section.get():
                a = i
                break
        File_hide_size.set(number[a])

    entry_File_hide_section = tkinter.ttk.Combobox(File_hide_win, textvariable=File_hide_section)
    entry_File_hide_section ['value'] = section
    entry_File_hide_section.configure(state="readonly")  # 只读
    entry_File_hide_section.bind('<<ComboboxSelected>>', show)
    entry_File_hide_section.place(x=150, y=80)

    entry_File_hide_size = tk.Entry(File_hide_win, textvariable=File_hide_size, width=17)
    entry_File_hide_size.place(x=380, y=80)
    entry_File_hide_size['state'] = 'readonly'                              #只读
    entry_File_hide_pwd = tk.Entry(File_hide_win, textvariable=File_hide_pwd, width=50)
    entry_File_hide_pwd.place(x=150, y=30)
    entry_File_hide_text = tk.Text(File_hide_win, width=42, height=8, font=('宋体', 15))
    entry_File_hide_text.place(x=80,y=155)

    # t = threading.Thread(target=thread)  # 线程运行的函数和参数
    # t.setDaemon(True)  # 设置为守护线程（在主线程线程结束后自动退出，默认为False即主线程线程结束后子线程仍在执行）
    # t.start()  # 启动线程

    File_hide = tk.Button(File_hide_win, text='确定', command=Cyc)
    File_hide.place(x=140, y=365)
    File_extract = tk.Button(File_hide_win, text='清除', command=hide_clear)
    File_extract.place(x=340, y=365)

    pass

#隐藏清除
def hide_clear():
    File_hide_pwd.set("")
    File_hide_section.set("")
    File_hide_size.set("")
    entry_File_hide_text.delete("1.0","end")

    pass

#文件提取
def File_extract(file):
    global File_extract_win
    global File_extract_pwd
    global FileName1

    FileName1 = file.encode('utf-8')
    File_extract_win = tk.Toplevel(window)
    File_extract_win.title('extract')  # 窗口标题
    File_extract_win.geometry('600x150+550+200')  # 窗口大小和显示位置
    File_extract_win.resizable(False, False)  # 禁止用户调整窗口大小
    window.attributes("-disabled", 1)
    File_extract_win.protocol("WM_DELETE_WINDOW", File_extract_handler)

    File_extract_pwd = tk.StringVar()

    tk.Label(File_extract_win, text='请输入密码:').place(x=80, y=30)

    entry_File_extract_pwd = tk.Entry(File_extract_win, textvariable=File_extract_pwd, width=50)
    entry_File_extract_pwd.place(x=150, y=30)

    File_hide = tk.Button(File_extract_win, text='确定', command=File_extract1)
    File_hide.place(x=140, y=100)
    File_extract = tk.Button(File_extract_win, text='清除', command=extract_clear)
    File_extract.place(x=340, y=100)

    pass

#文件提取1
def File_extract1():
    global File_extract1_win
    global File_extract1_section
    global File_extract1_size

    str_pwd = mima()

    if File_extract_pwd.get() != str_pwd:
        tk.messagebox.showerror(title='错误', message="密码错误")
        return 0

    File_extract_win.destroy()
    File_extract1_win = tk.Toplevel(window)
    File_extract1_win.title('extract1')  # 窗口标题
    File_extract1_win.geometry('600x150+550+200')  # 窗口大小和显示位置
    File_extract1_win.resizable(False, False)  # 禁止用户调整窗口大小
    window.attributes("-disabled", 1)
    File_extract1_win.protocol("WM_DELETE_WINDOW", File_extract1_handler)

    File_extract1_section = tk.StringVar()
    File_extract1_size = tk.StringVar()

    tk.Label(File_extract1_win, text='选择区段:').place(x=80, y=30)
    tk.Label(File_extract1_win, text='提取的大小:').place(x=310, y=30)

    PE = duanname(FileName1)
    section = PE[0]

    entry_File_extract1_section = tkinter.ttk.Combobox(File_extract1_win, textvariable=File_extract1_section)
    entry_File_extract1_section['value'] = section
    entry_File_extract1_section.configure(state="readonly")  # 只读
    entry_File_extract1_section.place(x=150, y=30)

    entry_File_extract1_size = tk.Entry(File_extract1_win, textvariable=File_extract1_size, width=17)
    entry_File_extract1_size.place(x=380, y=30)

    File_hide = tk.Button(File_extract1_win, text='确定', command=Ctq)
    File_hide.place(x=140, y=100)
    File_extract1 = tk.Button(File_extract1_win, text='清除', command=extract_clear1)
    File_extract1.place(x=340, y=100)

    pass

#提取清除
def extract_clear():
    File_extract_pwd.set("")
    pass

#提取清除
def extract_clear1():
    File_extract1_section.set("")
    File_extract1_size.set("")

    pass

#信息隐藏
def hide():
    global file_path

    if len(file_path) < 1:
        tk.messagebox.showerror(title='错误', message="请输入文件路径")
        return
    f = open(file_path, mode="rb")
    str = f.read(4)
    if str[0] == 0x4d and str[1] == 0x5a and str[2] == 0x90 and str[3] == 0x0:
        File_hide(file_path)
    else:
        tk.messagebox.showerror(title='错误', message="不是正确的PE文件")

#信息提取
def extract():
    global file_path

    if len(file_path) < 1:
        tk.messagebox.showerror(title='错误', message="请输入文件路径")
        return
    f = open(file_path, mode="rb")
    str = f.read(4)
    if str[0] == 0x4d and str[1] == 0x5a and str[2] == 0x90 and str[3] == 0x0:
        File_extract(file_path)
    else:
        tk.messagebox.showerror(title='错误', message="不是正确的PE文件")

#界面的代码实现,在窗口中写入文字
def ck():
    global var_usr_file
    tk.Label(window, text='文件路径:').place(x=30, y=30)

    entry_usr_file = tk.Entry(window, textvariable=var_usr_file, width=35)
    entry_usr_file.place(x=100, y=30)

#将获取到的文件路径显示到GUI窗口
def file(files):
    global var_usr_file
    global file_path

    file_path = '\n'.join(item.decode('gbk') for item in files)
    var_usr_file.set(file_path)

# 信息隐藏和信息提取按钮
def anniu():
    btn_hide = tk.Button(window, text='信息隐藏', command=hide)
    btn_hide.place(x=80, y=80)
    btn_extract = tk.Button(window, text='信息提取', command=extract)
    btn_extract.place(x=280, y=80)

#主函数
def main():
    window.title('IYM')                             #窗口标题
    window.geometry('400x150+600+300')              #窗口大小和显示位置
    window.resizable(False, False)                  #禁止用户调整窗口大小
    ck()                                            #窗口
    anniu()                                         #按钮
    windnd.hook_dropfiles(window, func=file)        #获取文件路径
    window.mainloop()                               #调用主循环，显示窗口，同时开始tkinter的事件循环

if __name__ == '__main__':
    main()
