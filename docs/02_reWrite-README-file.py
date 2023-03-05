"""
@Author: xdd2026@qq.com
@CreateData: 2023-03-04 16:13:12
@MaintenanceDate: 2023-03-04 16:13:12
@Purpose: 自动生成readme文件，安找日期对文件排序
@TODO:图片最后一行不够三个怎么处理
"""

import os
import time
import math
import random
import requests
import urllib.request
from fake_useragent import UserAgent
from lxml import etree
from PIL import Image  # pip3 install pillow


def get_files_of_folder(path):
    """获取指定路径下所有子文件夹的文件绝对路径"""
    file_list = []
    for foldername, subfolders, filenames in os.walk(path):
        for filename in filenames:
            file_list.append(os.path.join(foldername, filename))
    return file_list


def sort_file_by_date(file_list):
    """ 由文件名中的日期对文件列表排序 """

    date_list = []
    for ii in file_list:
        basename = os.path.basename(ii)
        date_list.append(basename[0:8])

    sorted_index = [i for i, x in sorted(enumerate(date_list), key=lambda x: x[1], reverse=True)]
    file_list_new = [file_list[ii] for ii in sorted_index]
    return file_list_new


def download_pic(path, pic_num):
    """ 下载彼岸图的动漫图片 """

    page_need = math.ceil(pic_num / 20)

    my_pic_list = []
    for ii in range(page_need):
        page_imdex = random.randint(2, 125)  # 20230304 彼岸图网动漫仅有126页
        url = f"https://pic.netbian.com/4kdongman/index_{page_imdex}.html"
        headers = {'user-agent': UserAgent().random}
        html_text = requests.get(url, headers=headers).text
        r = etree.HTML(html_text)
        my_http_list = r.xpath('//div/ul[@class="clearfix"]/li/a/@href')
        for ii in my_http_list:
            url = "https://pic.netbian.com" + ii
            html_text = requests.get(url, headers=headers).text
            r = etree.HTML(html_text)
            tmp = r.xpath('//div[@class="wrap clearfix"]/div/div/div/div[@class="photo-pic"]/a/img/@src')
            my_pic_list.append(tmp[0])



    for index, url in enumerate(my_pic_list):
        url = "https://pic.netbian.com" + url

        print(str(index) + ' / ' + str(len(my_pic_list)))
        picName = url.split('/')[-1]
        fileSavePath = os.path.join(path, picName)
        if not os.path.exists(fileSavePath):
            urllib.request.urlretrieve(url, fileSavePath)
            time.sleep(0.25)


def calu_pic_cropBox(size, radio):
    """根据一个尺寸以及比例计算中心点及四个较坐标"""

    width = size[0]
    height = size[1]

    if width / height > radio[0] / radio[1]:
        box_left = width / 2 - height * radio[0] / radio[1] / 2
        box_up = 0
        box_right = width / 2 + height * radio[0] / radio[1] / 2
        box_bottom = height
    else:
        box_left = 0
        box_up = height / 2 - width * radio[1] / radio[0] / 2
        box_right = width
        box_bottom = height / 2 + width * radio[1] / radio[0] / 2

    box = [box_left, box_up, box_right, box_bottom]

    return box


def cut_pic(folder, radio):
    """ 裁剪图片 """
    pic_list = os.listdir(folder)
    for ii in pic_list:
        ii_path = os.path.join(folder, ii)
        img = Image.open(ii_path)
        cropBox = calu_pic_cropBox(img.size, radio)
        cropped = img.crop(cropBox)
        cropped.save(ii_path)


def write_readme_file(file_list_new, num_row_pic, width_show):
    with open('README.md', encoding='utf-8') as f:
        content = f.readlines()

    N_file = len(file_list_new)
    content.append("|     " * num_row_pic + "|\n")
    content.append("|:---:" * num_row_pic + "|\n")

    # 获取图片列表
    row_pic = ''
    row_md = ''
    pic_list = os.listdir("./pic/used")
    for ii in range(N_file):
        if ii % num_row_pic == 0 and ii != 0:  # 换行，每行固定文章数目
            content.append(row_pic + "|\n")
            # content.append("| " * num_row_pic + "|\n")
            row_pic = ''
            content.append(row_md + "|\n")
            row_md = ''

        pic_ii_path = os.path.abspath(os.path.join("./pic/used", pic_list[ii]))
        pic_width = Image.open(pic_ii_path).size[0]
        radio = str(int(width_show / pic_width * 100))
        row_pic = row_pic + f'|<img src = "pic/used/{pic_list[ii]}" width = "{radio}%" height = "{radio}%">'

        # 写标题
        md_ii = file_list_new[ii]
        tmp_list = md_ii.split('\\')
        index = tmp_list.index("md_File")
        path = ''
        for jj in range(index, len(tmp_list)):
            path = os.path.join(path, tmp_list[jj])
        path = path.replace('\\', '/')
        basename = os.path.basename(md_ii)
        row_md = row_md + f'| [{basename}]({path})'



    yuShu = N_file % num_row_pic
    content.append(row_pic + "| " * (num_row_pic-yuShu) + "|\n")
    content.append(row_md + "| " * (num_row_pic - yuShu) + "|\n")



    # 写出到新的markdown文件中
    with open('README2.md', 'w', encoding='utf-8') as fw:
        fw.writelines(content)


if __name__ == "__main__":
    folderAbs = os.path.abspath("./md_File")
    # print(folderAbs)
    # folderAbs = r"D:\Git\docsify\docs\md_File"
    file_list = get_files_of_folder(folderAbs)
    file_list_new = sort_file_by_date(file_list)

    # 下载图片
    N_file = len(file_list_new)
    path = os.path.abspath('./pic/used')
    N_exist = len((os.listdir(path)))
    if N_exist < N_file:
        download_pic(path, N_file - N_exist)
    else:
        print("文件夹图片数目已经超过文章数目，无需下载图片")

    # 裁剪图片
    radio = [16, 9]
    cut_pic(path, radio)

    # 写readme文件
    num_row_pic = 3
    width_show = 1000
    write_readme_file(file_list_new, num_row_pic, width_show)
