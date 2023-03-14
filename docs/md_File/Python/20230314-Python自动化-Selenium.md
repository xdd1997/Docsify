## 基础知识

Python+Selenium基础入门及实践 - 简书

https://www.jianshu.com/p/1531e12f8852

### 下载chromedriver.exe

1. chrome浏览器---设置---关于Chrome, 查看Chrome版本
2. http://chromedriver.storage.googleapis.com/index.html --- 下载对应版本的 chromedriver.exe
3. 将 chromedriver.exe 文件夹加入到系统环境变量Path中（重启Pycharm）
4. 测试代码

```python
import time
from selenium import webdriver
browser = webdriver.Chrome()
browser.get('http://www.baidu.com/')
browser.find_element_by_id("kw").send_keys("ddx")
browser.find_element_by_id("su").click()
time.sleep(3)
browser.quit()
```

### 定位元素

- browser.find_element_by_id()
- browser.find_element_by_name()
- browser.find_element_by_tag_name()
- browser.find_element_by_class_name()
- browser.find_element_by_css_selector()
- browser.find_element_by_xpath()

```python
from selenium import webdriver
browser=webdriver.Firefox()
browser.get("http://www.baidu.com")
######### 百度搜索输入框的定位方式 ##########
#通过id方式定位
browser.find_element_by_id("kw").send_keys("selenium")
#通过name方式定位
browser.find_element_by_name("wd").send_keys("selenium")
#通过tag name方式定位
browser.find_element_by_tag_name("input").send_keys("selenium")
#通过class name方式定位
browser.find_element_by_class_name("s_ipt").send_keys("selenium")
#通过CSS方式定位
browser.find_element_by_css_selector("#kw").send_keys("selenium")
#通过xpath方式定位
browser.find_element_by_xpath("//input[@id='kw']").send_keys("selenium")
######### 百度搜索百度一下按钮的定位方式 ##########
browser.find_element_by_id("su").click()

time.sleep(3)
browser.quit()
```

### 操作方法

1. 输入内容：`.send_keys("ddx")`，`send_keys(u"测试")`
2. 左键单击：`.click()`
3. 下拉列表框选择：select_by_index(1), select_by_value("zhengzhou"), select_by_visible_text("郑州"), deselect_all()
4. 

## 实例

### 百度搜索

```python
# pip install selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

s = Service(r"C:\Users\614\Downloads\chromedriver_win32\chromedriver.exe")
driver = webdriver.Chrome(service=s)
driver.get('https://www.baidu.com')

driver.find_element_by_id("kw").send_keys("ddx")
driver.find_element_by_id("su").click()
```





## 