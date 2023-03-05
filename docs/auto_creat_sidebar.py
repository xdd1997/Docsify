""" Author:xdd2026@qq.com 
    Date:2022-09-18
    Purpose:用于自动生成 _sidebar.md, 仅适用两层文件夹    
"""

import os
import logging
from shutil import copyfile


# low->high: DEBUG-INFO-WARN-ERROR-CRITICAL
logging.basicConfig(level=logging.INFO, format='%(levelname)8s:%(message)s')
logging.info('*' * 80)

def remove_digits_front_of_string(strOld:str) -> str:
    """ 去除文件最前面连续数字：日期"""
    strNew = strOld
    for c in strNew:
        if c.isdigit():
            strNew = strNew[1:]

    # 去除首个字符 '-'
    if strNew[0] == '-':
        strNew = strNew[1:]
        
    return strNew



def deal_fileName_with_space():
    """ 去除文件名中的空格 """
    
    dir_path = r"md_File"
    fileList = []

    for root, dirs, files in os.walk(dir_path, topdown=False):
        for name in files:
            tmp = os.path.join(root, name)
            if os.path.isfile(tmp):
                fileList.append(tmp)

        for name in dirs:
            tmp = os.path.join(root, name)
            if os.path.isfile(tmp):
                fileList.append(tmp)


    for ii in fileList:
        name = os.path.basename(ii)
        rename = 0
        if ' ' in name:
            rename = 1
            name = name.replace(' ','')
            
        if name[8] != '-':
            rename = 1
            name = name[0:8] + '-' + name[8:]

        if rename == 1:
            target = os.path.join(os.path.dirname(ii),name)
            copyfile(ii, target)
            os.unlink(ii)






def gen_sidebar():
    """ 生成侧边栏md """
    
    dir_path = r"md_File"
    fileList = []

    with open('_sidebar.md', 'w', encoding='utf-8') as fw:
        fw.write('<!-- _sidebar.md -->' + '\n\n')

        for ii in os.listdir(dir_path):

            if os.path.isdir(os.path.join(dir_path,ii)):
                tmp = f'/md_File/{ii}'  
                iiNew = remove_digits_front_of_string(ii)
                fw.write('\n')
                fw.write(f'* [{iiNew}]' + '\n')  # 打印CAD-CAE等文件夹

                for jj in os.listdir(os.path.join(dir_path,ii)):
                    # print(jj)
                    tmp02 = os.path.join(dir_path,ii)
                    tt5 = os.path.join(tmp02,jj)

                    
                    if os.path.isdir(tt5):
                        tmp = f'/md_File/{ii}/{jj}'
                        ttt = os.path.join(tmp02,jj)
                        jjNew = remove_digits_front_of_string(jj)

                        fw.write('\n')
                        fw.write(f'    * [{jjNew}]' + '\n')  # 打印CAD-CAE等文件夹子文件夹

                        for kk in os.listdir(ttt):
                            tmp03 = os.path.join(ttt,kk)
                            if os.path.isfile(tmp03):
                                tmp = f'/md_File/{ii}/{jj}/{kk}'
                                kkNew = remove_digits_front_of_string(kk)
                                fw.write(' '*8+'* ' +f'[{kkNew}]({tmp})' + '\n')
                            else:
                                print(f'/md_File/{ii}/{jj}/{kk} 目录太深，暂不支持')

                    else:
                        tmp = f'/md_File/{ii}/{jj}'
                        jjNew = remove_digits_front_of_string(jj)
                        fw.write(f'    * [{jjNew}]({tmp})' + '\n')
            else:
                """ 为了在网页中先显示文件夹，最后显示根目录的文件
                    在本次循环只写文件夹的内容，不写文件内容 """
                pass


        """ 打印CAD-CAE等文件夹的同级文件 """
        for ii in os.listdir(dir_path):
            tt = os.path.join(dir_path,ii)
            if os.path.isfile(tt):
                tmp = f'/md_File/{ii}'
                iiNew = remove_digits_front_of_string(ii)
                fw.write(f'* [{iiNew}]({tmp})' + '\n')




if __name__ == "__main__":
    
    logging.info('=' * 80)
    deal_fileName_with_space()
    gen_sidebar()
    
    logging.info('_sidebar.md 生成完毕')

