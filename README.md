# 广东天翼校园Young第三方登录

## 开源协议 

[AGPL V3](LICENSE)

特别指出禁止任何个人或者公司将本代码投入商业使用

由此造成的后果和法律责任均与本人无关。

## 使用教程

广州工贸技师学院南校区可以直接使用

|变量|类型|说明|
|--|--|--|
|ip|str|自行替换125.88.59.131:10001<br>换成自己的校园网ip|
|wlanAcIP|str|自行抓包<br>一般连接WIFI后自动弹出的页面的url就有|

### 例子：

```python
import api
if __name__ == "__main__":
    Young = api.young(ip='125.88.59.131:10001')
    f = open("code.jpg", "wb+")
    data = Young.changeCode()
    f.write(data)
    f.flush()
    f.close()
    user = input("账号：")
    password = input("密码：")
    code = input("验证码(请自行打开运行目录中的code.jpg查看验证码)：")
    userIP = input("IP（连接WIFI后的IPV4）：")
    print(Young.login(user, password, code, userIP))
    input("回车关闭。")
```

该版本是网页版登录接口，不是传统的pptp和xxx协议

该项目已停止维护，学校准备换运营商