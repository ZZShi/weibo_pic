weibo_pic
===
使用百度人像处理对微博图片进行筛选，下载颜值大于设定阈值的图片到本地
## 安装库
<br>pip install requests</br>
<br>pip install beautifulsoup4</br>
<br>pip install baidu-aip</br>
## 百度人脸人别
人脸识别调用了百度[AI开放平台](http://ai.baidu.com/)的API，此服务需要注册使用；传入需要解析的照片，设置参数，得到需要的结果；具体文档请参考[文档中心--百度AI-百度AI-AI开放平台](http://ai.baidu.com/docs#/Face-Detect/top)
## 结果展示
<br>本次爬取的目标为迪丽热巴的微博，如果需要爬取其它目标，只需在weibo_pic.py中更改全部变量VALUE</br>
<br>如何获取VALUE，打开目标的微博链接，如迪丽热巴：https://weibo.com/u/1669879400?is_hot=1 ，则VALUE为1669879400</br>
<img src="https://github.com/ZZShi/weibo_pic/blob/master/result.png" width="800" height="500" alt="图片加载失败"/>
