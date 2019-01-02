import unittest
#coding=utf-8
from selenium import webdriver
from time import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os
import select
from selenium.webdriver.support.select import Select
from random import choice
import random
from random import randrange
from  random import uniform
from test_case.pagebase import Page
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

class Addsale(unittest.TestCase):
    """销售单录单"""
    global dr, sale
    def setUp(self):
        print("录制销售单据开始")
        global dr, sale
        # 实例化Page,并引用dr
        sale = Page()
        dr = sale.driver()
        sale.loginout("17700000001", "Abc123456")
        # 进入控制台。搜索企业
        try:
            dr.find_element_by_xpath("//a[@href='/index']").click()
        except NoSuchElementException as e:
            print("登录跳转到了控制台")
        print("进入控制台")
        # 控制台搜索企业
        sale.kongzhitai("cyb0811企业")
        sleep(3)

    def salebilladd(self):

        global dr,sale
        # 判断纳税人类型
        type=sale.pagecount()
        # 进入单据切换页面，切换单据类型
        dr.find_element_by_xpath("//*[@id='menu_list']/li/a").click()  # 进入单据页面
        print("进入单据模块")
        sleep(3)
        dr.find_element_by_xpath("//*[@id='list_view']/div/div[1]/div/div[2]/fieldset/div[1]/div/button[1]").click()  # 点击添加
        print("进入单据添加页面")
        sleep(5)
        sale.changetype(1)
        # 获取付款方式
        sale.paymethod()
        if type == 0 or type == 2:  # 该企业是一般纳税人带进销存，销售单有，客户，收款方式，商品名，单位，数量，单价，金额，税率，税额，折后金额，折后税额
            print("该企业为一般或小规模带进销存企业，销售单包含：客户，收款方式，商品名，单位，数量，单价，金额，税率，税额，折后金额，折后税额11个字段")
            # 客户设置，先要判断有没有客户。。有的话选择，没有的话添加
            dr.find_element_by_xpath("//*[@id='select2-auxiliary_users-container']").click()
            kehulists = dr.find_elements_by_xpath("html/body/span/span/span[2]/ul/li")
            del kehulists[0]  # 去除--请选择--这个项
            khcount = len(kehulists)
            if khcount != 0:
                print("该企业共有 %r 个客户" % khcount)
                # 随机选择一个客户
                i = random.randint(0, khcount - 1)
                kehulists[i].click()  # 随机点击一个客户
                sleep(3)
                kh = dr.find_element_by_xpath("//*[@id='select2-auxiliary_users-container']").text
                print("随机选择一个客户%r" % kh)
            else:
                print("该企业没有客户，需要添加客户")
                # 执行添加客户操作
                sleep(3)
                dr.find_element_by_xpath("/html/body/span/span/span[3]").click()  # 点击添加
                sleep(2)
                dr.find_element_by_xpath("//*[@id='name']").send_keys("客户123")  # 写入客户名
                dr.find_element_by_xpath("//*[@data-bb-handler='success' and @type='button' and @class='btn bluetbn-btn confirmBtn']").click()
                # 添加客户之后，系统自动将添加的客户选中
                sleep(2)
                print("已经成功添加客户")
            sleep(3)
            #salesale=Addsale()
            sale.xscg('template2_table')
            # 判断是否有弹出警告框
            try:
                WebDriverWait(dr, 5, 0.1).until(EC.presence_of_element_located((By.ID, "notify_0")))
            except TimeoutException as e:
                print("单据提交失败")
                dr.get_screenshot_as_file("E:\\script\\report\\销售单据提交失败.jpg")
                self.assertEqual(0, 1, msg="单据提交失败")
        elif type==1: # 一般纳税人不带进销存
            return
        else:         # 小规模不带进销存
            return
    def tearDown(self):
        dr.quit()
if __name__ == '__main__':
    unittest.main()

