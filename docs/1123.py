# write by xdd1997  xdd2026@qq.com

import os
import winreg
import random
import requests
import urllib.request
from bs4 import BeautifulSoup
from PIL import Image



# 获取桌面路径
def desktop_path():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    path = winreg.QueryValueEx(key, "Desktop")[0]
    return path
# -------------递归创建目录-----------
def CreatPath():
    path = os.path.join(desktop_path().replace('/','\\'),'pa pic')
    if not os.path.exists(path):
        os.makedirs(path)
    return path

#微信下载图片的网址
try:
    num = random.randint(1,22222)
    url = "http://www.netbian.com/desk/{}.htm".format(num)
    r = requests.get(url)
    demo = r.text
    soup = BeautifulSoup(demo, "html.parser")
    piclist = []
    for link in soup.find_all('img'):
        link_list = link.get('src')
        if link_list != None:
            piclist.append(link_list)
    http = piclist[2]
except:
    url = "http://www.netbian.com/desk/22152.htm"
    r = requests.get(url)
    demo = r.text
    soup = BeautifulSoup(demo, "html.parser")
    piclist = []
    for link in soup.find_all('img'):
        link_list = link.get('src')
        if link_list != None:
            piclist.append(link_list)
    http = piclist[2]

print(http)
filesavepath = os.path.join(CreatPath(),'pic.jpg')
urllib.request.urlretrieve(http, filesavepath)
print('下载完成,保存路径为' + CreatPath())
img = Image.open(filesavepath)
img.show()

