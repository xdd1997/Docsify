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

        print(str(index+1) + ' / ' + str(len(my_pic_list)), end='\r')
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
    str00 = '<p align="center">  <a href="http://mail.qq.com/cgi-bin/qm_share?t=qm_mailme&email=gfnl5bOxs7fB8PCv4u7s" target="_blank"><img src="https://img.shields.io/badge/Email-xdd2026%40qq.com-green.svg"></a>'
    str01 = '<a href=http://wpa.qq.com/msgrd?v=1&uin=1837990190&site=qq&menu=yes" target="_blank"><img src="https://img.shields.io/badge/QQ-1837990190-brightgreen"></a></p>'

    str02 = '<span id="busuanzi_container_site_pv" style="display:none">本站总访问量：<span id="busuanzi_value_site_pv"></span> 次</span>'
    str03 = '\n\n[侧边栏](_sidebar.md)\n'
    str04 = '\n[我的网页](md_File/20221212-my_url.md)\n\n'

    content = []
    content.append(str00)
    content.append(str01)
    content.append(str02)
    content.append(str03)
    content.append(str04)

    N_file = len(file_list_new)
    content.append("|     " * num_row_pic + "|\n")
    content.append("|:---:" * num_row_pic + "|\n")

    # 获取图片列表
    row_pic = ''
    row_md = ''
    pic_list = os.listdir("./pic/used")

    # 对图片随机排序
    random_origin = random.sample(range(1000,10000), len(pic_list))
    sort_index = sorted(range(len(random_origin)), key=lambda i: random_origin[i])
    pic_list = [pic_list[i] for i in sort_index]
    

    #  写表格与内容
    for ii in range(N_file):
        if ii % num_row_pic == 0 and ii != 0:  # 换行，每行固定文章数目
            content.append(row_pic + "|\n")
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


    # 补足表格最后一行
    yuShu = N_file % num_row_pic
    content.append(row_pic + "| " * (num_row_pic-yuShu) + "|\n")
    content.append(row_md + "| " * (num_row_pic - yuShu) + "|\n")



    # 写出到新的markdown文件中
    with open('README.md', 'w', encoding='utf-8') as fw:
        fw.writelines(content)


def write_sort_articles_by_date(file_list_new):
    """ 写一个按照日期对文章分类的md文件 """

    content = []
    local_time = time.localtime(time.time())

    tmp_year = str(local_time[0])
    str_tmp = f'## {tmp_year}\n'
    content.append(str_tmp)

    for ii in file_list_new:
        tmp = os.path.basename(ii)[0:4]
        if tmp!= tmp_year:
            tmp_year = tmp
            str_tmp = f'## {tmp_year}\n'
            content.append(str_tmp)
        else:
            title = os.path.basename(ii)

            tmp_list = ii.split('\\')
            index = tmp_list.index("md_File")
            path = ''
            for jj in range(index, len(tmp_list)):
                path = os.path.join(path, tmp_list[jj])
            path = path.replace('\\', '/')
            str_tmp = f'##### [{title}]({path})\n'
            content.append(str_tmp)

    # 写出到 articles_by_date文件中
    with open('articles_by_date.md', 'w', encoding='utf-8') as fw:
        fw.writelines(content)



if __name__ == "__main__":
    folderAbs = os.path.abspath("./md_File")
    # folderAbs = r"D:\Git\docsify\docs\md_File"
    file_list = get_files_of_folder(folderAbs)
    file_list_new = sort_file_by_date(file_list)

    # 下载图片
    N_file = len(file_list_new)
    path = os.path.abspath('./pic/used')
    
    while True:
        N_exist = len((os.listdir(path)))
        if N_exist < N_file:
            print("正在下载图片")
            download_pic(path, N_file - N_exist)
        else:
            print("图片数目已经多于文章数目")
            break


    # 裁剪图片
    radio = [16, 9]
    cut_pic(path, radio)


    # 写readme文件
    num_row_pic = 3
    width_show = 1000
    write_readme_file(file_list_new, num_row_pic, width_show)

    # 写 articles_by_date.md
    write_sort_articles_by_date(file_list_new)

    print("=" *80 + " \nREADME.md文件与 articles_by_date.md 文件生成完毕\n")
    
