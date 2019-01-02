"""本脚本只有登录，没有注册跟找回密码功能。注册与找回密码，需要获取验证码，链接到第三方软件，暂时不实现"""


#coding=utf-8
import sys
from selenium import webdriver
from time import*
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


dr=webdriver.Chrome()
#跳转到云算盘
dr.get("http://test.vsupa.com/homepage/login.html")
print("打开云算盘")
dr.maximize_window()
#登录系统
dr.find_element_by_id("loginName").send_keys("cybtest")


sleep(2)



password=dr.find_element_by_id("password")
password.send_keys("123456")


dr.find_element_by_id("loginBtn").click()
print("登录成功")