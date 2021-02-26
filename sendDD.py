import time
import hashlib
import hmac
import base64
import re
import requests
import datetime
import query_warning
import pymysql

message = ''


def SendMessage(message=''):
    # secret：密钥，机器人安全设置页面，加签一栏下面显示的SEC开头的字符串，例如：SECxxxxxxxx
    secret = 'SEC5a6d827dff9e81e1b7ed11691db0faa335ae30799c38c74cb71010bc8f44f0a3'
    # access_token：创建完钉钉机器人之后会自动生成，例如：access_tokenxxxx
    access_token = '7125dff18a4403753d85246801959edb93aed4035e29bed7c5bb3fa999038a69'
    # timestamp：当前时间戳，单位是毫秒，与请求调用时间误差不能超过1小时
    timestamp = int(round(time.time() * 1000))

    # 加密，获取sign和timestamp
    data = (str(timestamp) + '\n' + secret).encode('utf-8')
    secret = secret.encode('utf-8')
    signature = base64.b64encode(hmac.new(secret, data, digestmod=hashlib.sha256).digest())
    reg = re.compile(r"'(.*)'")
    signature = str(re.findall(reg, str(signature))[0])

    # 发送信息
    url = 'https://oapi.dingtalk.com/robot/send?access_token=%s&sign=%s&timestamp=%s' % (
        access_token, signature, timestamp)
    headers = {"Content-Type": "application/json ;charset=utf-8 "}
    try:
        response = requests.post(url, headers=headers, json=message, timeout=(3, 60))
        print(response)
        response_msg = str(response.status_code) + ' ' + str(response.content)
        print(response_msg)
    except Exception as error_msg:
        print('error_msg===' + str(error_msg))
        response_msg = error_msg
    return response_msg


def send(info):
    msg = {"msgtype": "text", "text": {"content": info}, "at": {"isAtAll": True}}
    print("msg", msg)
    SendMessage(msg)


if __name__ == "__main__":
    info = query_warning.get().get_data()
    now = datetime.datetime.now().strftime('%Y%m%d %H:%M:%S')
    if info != '':
        print(info)
        print("none")
        send('监控类型：服务器告警\n当前时间：' + now + '\n\n' + info)
        print('\n当前时间：', now, "\n告警发送成功！")
    else:
        print('\n当前时间：', now, "\n无告警内容！")
