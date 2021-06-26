
from genericpath import isfile
from tkinter import *
import tkinter.messagebox as messagebox
from tkinter.font import Font
from PIL import Image, ImageTk
import requests
import api
import socket
from os import getcwd, path
import json


class windows:
    def __init__(self, init_windows):
        self.init_windows = init_windows

        self.userIP = get_host_ip()
        self.Young = api.young()
        self.getCode(False)
        self.path_code = getcwd() + "\\code.jpg"
        self.path_config = getcwd() + "\\config.json"

    def set_init_windows(self):
        ## 修改参数
        self.init_windows.title("天翼校园--v0.1_demo")
        self.init_windows.geometry("300x300+10+10")

        #自动居中
        self.screen_width = self.init_windows.winfo_screenwidth()#获得屏幕宽度
        self.screen_height = self.init_windows.winfo_screenheight()  #获得屏幕高度
        self.init_windows.update_idletasks()#刷新GUI
        self.init_windows.withdraw() #暂时不显示窗口来移动位置
        self.init_windows.geometry('%dx%d+%d+%d' % (self.init_windows.winfo_width(), self.init_windows.winfo_height() ,(self.screen_width - self.init_windows.winfo_width()) / 2,(self.screen_height - self.init_windows.winfo_height()) / 2))  # center window on desktop
        self.init_windows.deiconify()   

        # 禁用最大化
        self.init_windows.resizable(False, False)

        # 标签
        ## 创建组件对象
        self.init_user_label = Label(self.init_windows, text="账号：")
        self.init_password_label = Label(self.init_windows, text="密码：")
        self.init_code_label = Label(self.init_windows, text="验证码：")
        self.init_userIP_label = Label(self.init_windows, text='IP：')

        ## 载入组件
        self.init_userIP_label.place(y=30, x=10)
        self.init_user_label.place(y=70, x=10)
        self.init_password_label.place(y=120, x=10)
        self.init_code_label.place(y=170, x=10)

        # 文本框
        ## 创建组件对象
        size = Font(size=18)
        self.init_user_Text = Entry(self.init_windows,width=15, font=size, relief=SUNKEN)
        self.init_password_Text = Entry(self.init_windows,width=15, font=size, show="*", relief=SUNKEN)
        self.init_code_Text = Entry(self.init_windows,width=5, font=size, relief=SUNKEN)
        self.init_userIP_Text = Entry(self.init_windows, width=15, font=size, relief=SUNKEN)

        ## 载入组件
        self.init_userIP_Text.place(y=25, x=65)
        self.init_user_Text.place(y=65, x=65)
        self.init_password_Text.place(y=115, x=65)
        self.init_code_Text.place(y=165, x=65)
        self.init_userIP_Text.insert(0, self.userIP)

        # 验证码图片框
        ## 创建组件对象
        self.init_code_Canvas = Button(self.init_windows, width=103, height=40, bg='#fff', bd=0, image=self.image_code_data, command=self.getCode)

        ## 载入组件
        self.init_code_Canvas.place(y=160, x=145)


        # 按钮组件
        ## 创建组件对象
        self.init_login_Button = Button(text="登录", height=2, width=10, takefocus=True, command=self.login, bd=1)

        ## 载入组件
        self.init_login_Button.place(y=220, x=100)

        # 执行函数
        self.keep(False)

    def login(self):
        self.init_login_Button.config(state=DISABLED)
        self.user_Text = ""
        self.password_Text = ""
        self.code_Text = ""
        try:
            self.user_Text = self.init_user_Text.get().split()[0]
            self.password_Text = self.init_password_Text.get().split()[0]
            self.code_Text = self.init_code_Text.get().split()[0]
            self.userIP = self.init_userIP_Text.get().split()[0]
        except:
            pass


 
        if self.user_Text == "":
            messagebox.showwarning("提示：", "请输入账号！")
            self.init_login_Button.config(state=NORMAL)
            return

        if self.password_Text == "":
            messagebox.showwarning("提示：", "请输入密码！")
            self.init_login_Button.config(state=NORMAL)
            return
        
        if self.code_Text == "":
            messagebox.showwarning("提示：", "请输入验证码！")
            self.init_login_Button.config(state=NORMAL)
            return

        if self.userIP == "":
            messagebox.showwarning("提示：", "请输入内网IP！")
            self.init_login_Button.config(state=NORMAL)
            return

        try:
            self.data = self.Young.login(self.user_Text, self.password_Text, self.code_Text, self.userIP)
        except:
            messagebox.showerror("错误：", "程序崩溃了".format(self.data))

        if isinstance(self.data,int):
            if self.data == -1:
                messagebox.showerror("错误：", "状态码：{0}\n验证码不是四位数！".format(self.data))
            else:
                messagebox.showerror("错误：", "状态码：{0}\n出现了不可意料的错误".format(self.data))
        else:
            self.data = json.loads(self.data)
            if self.data['resultCode'] == '0':
                messagebox.showinfo("状态：", "状态码：{0}\n登陆成功！".format(self.data['resultCode']))
            else:
                messagebox.showinfo("状态：", "状态码：{0}\n信息：{1}".format(self.data['resultCode'], self.data['resultInfo']))
            self.keep(True)
        self.getCode(True)
        self.init_login_Button.config(state=NORMAL)

    def keep(self, isKeep=False):
        if isKeep == True:
            with open(self.path_config, "w+", encoding='utf-8') as f_data:
                f_data.write(json.dumps({
                    "username": self.user_Text,
                    "password": self.password_Text,
                    "headers": self.Young.headers,
                    "wlanuserip": self.userIP
                }))
                f_data.flush()
                f_data.close()
        else:
            if path.isfile(self.path_config):
                with open(self.path_config, encoding='utf-8') as f_data:
                    try:
                        self.data = json.loads(f_data.read())
                        self.init_user_Text.insert(0, self.data['username'])
                        self.init_password_Text.insert(0, self.data['password'])
                    except:
                        pass
            else:
                with open(self.path_config, "w+", encoding='utf-8') as f_data:
                    f_data.write(json.dumps({
                        "wlanuserip": self.userIP
                    }))
                    f_data.flush()
                    f_data.close()
                

    def getCode(self, b=True):
        try:
            self.image_code_data = self.Young.changeCode()
            with open(getcwd() + "\\code.jpg", "wb+",) as self.F_Image:
                self.F_Image.write(self.image_code_data)
                self.F_Image.flush()
                self.F_Image.close()
                self.image_code_data = ImageTk.PhotoImage(Image.open(getcwd() + "\\code.jpg"))
            if b == True:
                self.init_code_Canvas.config(image=self.image_code_data)
        except requests.exceptions.HTTPError:
            messagebox.showerror("错误：", "请连接校园网！")
        except:
            pass
        
def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip     
        

def GUIStart():
    init_window = Tk()
    ZMJ_PORTAL = windows(init_window)
    ZMJ_PORTAL.set_init_windows()
    init_window.mainloop()

GUIStart()

