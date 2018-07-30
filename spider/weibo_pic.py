# -*- coding: utf-8 -*-
"""
Created in   22:25
@file: weibo_pic
@author: ZZShi
程序作用：
    根据输入的微博value值下载该微博的图片
    对图片进行筛选，只保存颜值大于40(阈值可修改）的，筛选使用的是百度AI开放平台的人脸识别服务
"""

import os
import re
import requests
import face_process

# 可配置的参数
# 用户的value值，可在用户首页的链接中提取  如迪丽热巴的微博链接https://weibo.com/u/1669879400?is_hot=1
VALUE = "1669879400"
# 颜值筛选阈值
BEAUTY = 40


def get_page(page, value=VALUE):
    url = "https://m.weibo.cn/api/container/getIndex?"
    params = {
        "type": "uid",
        "value": value,
        "containerid": "107603" + value,
        "page": page
    }
    hd = {
        "Host": "m.weibo.cn",
        "Referer": "https://m.weibo.cn/u/" + value,
        "User-Agent": "Mozilla/5.0",
        "X-Requested-With": "XMLHttpRequest"
    }
    try:
        r = requests.get(url, params=params, headers=hd, timeout=10)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.json()
    except Exception as e:
        print("失败链接：", url)
        print("失败原因：", e)


def extract_info(info):
    cards = info.get("data").get("cards")
    for card in cards:
        if card.get("card_type") != 9:
            continue
        mblog = card.get("mblog")
        pics = mblog.get("pics")
        if pics is None:
            continue
        created_at = mblog.get("created_at")
        text = mblog.get("text")
        # text文本处理
        pattern = re.compile(r"<.*?>", re.S)
        text = re.sub(pattern, "---", text)
        if len(text) >= 10:
            text = text[:10]
        yield[created_at, text, pics]


def get_content(url):
    hd = {
        "User-Agent": "Mozilla/5.0",
    }
    try:
        r = requests.get(url, headers=hd, timeout=10)
        r.raise_for_status()
        return r.content
    except Exception as e:
        print("失败链接：", url)
        print("失败原因：", e)


def save_pic(content, user, created_at, text, index):
    first_root = "D://weibo_pic"
    if not os.path.exists(first_root):
        os.mkdir(first_root)
    second_root = first_root + "//" + user
    if not os.path.exists(second_root):
        os.mkdir(second_root)
    path = second_root + "//" + created_at + "_" + text + "_" + str(index) + ".jpg"
    if not os.path.exists(path):
        with open(path, "wb") as f:
            f.write(content)
            print("Save Succeed: ", created_at + "_" + text + str(index) + ".jpg")
    else:
        print("Picture has existed!")


def get_info():
    """
    获取用户名及用户发布内容的总页数
    :return:
    """
    result = get_page("2")
    user = result.get("data").get("cards")[0].get("mblog").get("user").get("screen_name")
    total = result.get("data").get("cardlistInfo").get("total")
    return user, total


def main():
    user, total = get_info()
    for page in range(2, int(total / 10 + 2)):
        info = get_page(str(page))
        for created_at, text, pics in extract_info(info):
            for index, pic in enumerate(pics):
                pic_url = pic.get("url")
                content = get_content(pic_url)
                result = face_process.face_detection(content)
                print(result)
                if result.get("gender_probability") < 0.6:
                    continue
                if result.get("beauty") < BEAUTY:
                    continue
                save_pic(content, user, created_at, text, index)


if __name__ == "__main__":
    main()
