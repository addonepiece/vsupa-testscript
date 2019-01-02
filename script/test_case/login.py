from selenium import webdriver
from time import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import unittest
from test_case import pagebase
from test_case.pagebase import Page


class Login(unittest.TestCase):
    global dr
    global l
    l=Page()  # 实例化Page()
    def setUp(self):
        global dr
        print("test begin")
        dr=l.driver()  # 将driver的返回值给dr
    def login(self):
        """输入正确账号进行登录"""
        global dr
        l.loginout("cybtest","Abc123456") # 登录
        sleep(2)

    def tearDown(self):
        sleep(3)
        dr.quit()

if __name__ == '__main__':
    unittest.main()

