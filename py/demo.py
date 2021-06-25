from genericpath import isfile
import api
import json
from os import getcwd

if __name__ == "__main__":

    y = api.young() # 创建对象

    f_code = open(getcwd() + "\\code.jpg", "wb+") # 获取验证码部分，并写入文件
    data = y.changeCode()
    f_code.write(data)
    f_code.flush()
    f_code.close()

    # 登录
    user = input("账号：")
    password = input("密码：")
    code = input("验证码(请自行打开运行目录中的code.jpg查看验证码)：")
    userIP = input("IP（连接WIFI后的IPV4）：")
    print(y.login(user, password, code, userIP))

    with open(getcwd() + '\\data.json', 'w+', encoding='utf-8') as f_headers:
        data = {
            'username': user,
            'password': password,
            'headers': y.headers
        }
        f_headers.write(json.dumps(data))
        f_headers.flush()
        f_headers.close()
    input("回车关闭。")
