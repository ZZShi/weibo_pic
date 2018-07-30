# -*- coding: utf-8 -*-
"""
Created in   22:22
@file: face_process
@author: ZZShi
程序作用：
    人脸检测，根据输入的图片的二进制数据，返回
        age：年龄
        beauty: 美丑打分，范围0-100，越大表示越美。face_fields包含beauty时返回
        face_probability: 人脸置信度，范围0-1
        gender: male、female。face_fields包含gender时返回
        等信息
"""
import base64
import requests
from aip import AipFace
# 需要在百度AI开放平台注册账号申请 http://ai.baidu.com/
# 申请后直接复制粘贴过来
APP_ID = "10917093"
API_KEY = "V9KcvXGzRFAN8OgzBoocU3S9"
SECRET_KEY = "Ghcu8LP47ZFdo4VXeKD0GhXijTPNvzBy"


def _get_token():
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {
        "grant_type": "client_credentials",
        "client_id": API_KEY,
        "client_secret": SECRET_KEY
    }
    r = requests.post(url, params=params)
    return r.json().get("access_token")


def face_detection(content):
    """
    根据传入的图片的二进制形式返回检测的结果
    :param content:图片的二进制形式
    :return:包含年龄、颜值、人脸置信度、性别的json返回
    """
    url = "https://aip.baidubce.com/rest/2.0/face/v2/detect"
    params = {
        "access_token": _get_token(),
    }
    hd = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    face_fields = 'age,beauty,gender,face_probability'  # human信息不显示,删掉
    data = {
        "image": base64.b64encode(content),
        "face_fields": face_fields,  # tell me why??????????????  逗号后面不能加空格
        "max_face_num": 1
    }
    try:
        r = requests.post(url, params=params, headers=hd, data=data)
        r.raise_for_status()
        data = r.json().get('result')[0]
        return data

    except Exception as e:
        print("人脸检测失败代码：", e)
        return None


def _test():
    with open(r"D:\图片4.jpg", 'rb') as f:
        content = f.read()
        data = face_detection(content)
        print(data)


if __name__ == "__main__":
    _test()
