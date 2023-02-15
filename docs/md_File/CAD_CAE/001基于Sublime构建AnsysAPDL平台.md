## 基于Sublime构建Ansys APDL平台

### 第一步，构建编译系统

**sublime---工具---编译系统---新建编译系统---输入下面内容---保存为run_in_Ansys.sublime-bulid**

```python
{
	"shell_cmd": "C:\\App\\Python38\\python.exe D:\\File_Python_src\\Sublime_run_Ansys\\run_Ansys.py -F $file"
}
```

### 第二步，建立控制脚本

**在新建文件**D:\\File_Python_src\\Sublime_run_Ansys\\run_Ansys.py，内容为

```python
# -*- coding: utf-8 -*-

import win32gui
import win32con
import time
import os
import pickle
import sys

# 获取输入参数
import argparse
parser = argparse.ArgumentParser(description="parameter setting")
parser.add_argument('-F', '--file', help='File Path')
args = parser.parse_args()
fileMacOld = args.file
print(fileMacOld)
# fileMacOld = r"F:\AnsysTmp\ss.mac"


if os.path.splitext(fileMacOld)[1].lower() not in ['.mac','txt','inp']:
    print('-' * 60)
    raise ValueError('the file is not a Ansys mac file')



# 寻找窗口,这里需要更改
# https://mypic2016.oss-cn-beijing.aliyuncs.com/picGo/202211251458644.png

indent1 = 'ANSYS Mechanical Enterprise Utility Menu'
indent2 = 'Mechanical APDL 19.0 Output Window'


try:
    hwnd_title = dict()

    def get_all_hwnd(hwnd, mouse):
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
            hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})

    win32gui.EnumWindows(get_all_hwnd, 0)
    count = 0
    for h, t in hwnd_title.items():
        if indent1 in t:
            hwnd1 = h
            count += 1

    if count > 1:
        raise ValueError('Found more than 1 open Ansys program')

    for h, t in hwnd_title.items():
        if indent2 in t:
            hwnd2 = h
            break

    hwnd = [hwnd1, hwnd2]

except:
    print("error")

title = win32gui.GetWindowText(hwnd1)
if indent1 not in title:
    print('---------------------------------------------------------')
    print('Xdd Note：No open Ansys program found')
    print('---------------------------------------------------------')

# 运行文件
directory, name = os.path.split(fileMacOld)
stuff = name.split('.')
filePath = os.path.join(directory,stuff[0])
location = f'/input,{filePath},{stuff[1]}'
print(location)

try:
    # win32gui.ShowWindow(hwnd1, win32con.SW_MAXIMIZE)  # 将 Ansys 窗口最大化
    win32gui.ShowWindow(hwnd1, win32con.SW_SHOW)
    time.sleep(0.3)
    win32gui.ShowWindow(hwnd2, win32con.SW_MINIMIZE)
    temp = win32gui.SetForegroundWindow(hwnd1)
except:
    pass
finally:
    time.sleep(0.3)
    WM_CHAR = 0x0102
    for char in location:
        win32gui.SendMessage(hwnd1, WM_CHAR, ord(char), None)
    time.sleep(0.1)
    win32gui.SendMessage(hwnd1, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
    win32gui.SendMessage(hwnd1, win32con.WM_KEYUP, win32con.VK_RETURN, 0)
```

### 第三步，使用步骤

打开Ansys，在任意位置新建*.mac命令流文件---工具---编译系统---**run_in_Ansys---Ctrl+B**

```python
finish
/clear
/filname,SSS
/prep7
blc4,0,0,1,1,10
```