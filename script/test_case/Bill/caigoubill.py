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
from test_case.Bill.salebill import Addsale

class Addcg(unittest.TestCase):
    """采购单录单"""
    global dr, sale
    def setUp(self):
        print("录制采购单据开始")
        global dr, caigou
        # 实例化Page,并引用dr
        caigou = Page()
        dr = caigou.driver()
        caigou.loginout("17700000001", "Abc123456")
        # 进入控制台。搜索企业
        try:
            dr.find_element_by_xpath("//a[@href='/index']").click()
        except NoSuchElementException as e:
            print("登录跳转到了控制台")
        print("进入控制台")
        # 控制台搜索企业
        caigou.kongzhitai("cyb0811企业")
        sleep(3)

    def cgbilladd(self):

        global dr,caigou
        # 判断纳税人类型
        type=caigou.pagecount()
        # 进入单据切换页面，切换单据类型
        dr.find_element_by_xpath("//*[@id='menu_list']/li/a").click()  # 进入单据页面
        print("进入单据模块")
        sleep(3)
        dr.find_element_by_xpath("//*[@id='list_view']/div/div[1]/div/div[2]/fieldset/div[1]/div/button[1]").click()  # 点击添加
        print("进入单据添加页面")
        sleep(5)
        caigou.changetype(2)
        # 获取付款方式
        caigou.paymethod()
        if type == 0 or type == 2:  # 该企业是一般纳税人带进销存
            print("该企业是一般纳税人或者小规模带进销存")
            if type == 0:  # 该企业是一般纳税人带进销存，多1个字段的操作，抵扣情况
                print("该企业为一般纳税人多进销存，多一个字段，抵扣情况，开始随机选择抵扣情况")
                dikou = dr.find_element_by_xpath("//*[@id='deduction']")  # 点击抵扣情况，弹出下拉框
                dikou.click()
                sleep(2)
                Select(dikou).select_by_value(str(random.randint(1, 5)))  # 抵扣情况一共五个值，1正常抵扣，2不能抵扣，3待认证，4待抵扣，5进项转出，随机选择
                sleep(3)
            # 获取采购类型，随机选择
            cgtype = dr.find_element_by_xpath("//*[@id='type']")  # 点击采购类型
            cgtype.click()
            sleep(2)
            Select(cgtype).select_by_value(str(random.randint(1, 2)))  # 采购类型有两个值，1普通采购，2暂估采购，随机选择
            # 获取供应商，如果没有，添加供应商
            sleep(5)
            dr.find_element_by_xpath("//*[@id='select2-auxiliary_suppliers-container']").click()  # 点击供应商，弹出下拉框
            gyslists = dr.find_elements_by_xpath("html/body/span/span/span[2]/ul/li")  # 获取供应商下拉列表
            del gyslists[0]  # 去除--请选择--这一项
            gyscount = len(gyslists)  # 获取供应商个数
            if gyscount != 0:
                print("该企业共有%r个供应商" % gyscount)  # 判断供应商是否为空。供应商不为空
                # 随机选择一个供应商
                gyslists[random.randint(0, gyscount - 1)].click()
                sleep(3)
                gys = dr.find_element_by_xpath("//*[@id='select2-auxiliary_suppliers-container']").text
                print("随机选择一个供应商%r" % gys)
            else:
                print("该客户没有供应商，需要添加供应商")
                sleep(3)
                dr.find_element_by_xpath("/html/body/span/span/span[3]").click()  # 点击添加
                sleep(2)
                dr.find_element_by_xpath("//*[@id='name']").send_keys("供应商123")  # 写入供应商名，名字为供应商+随机数
                sleep(3)
                dr.find_element_by_xpath("//*[@data-bb-handler='success' and @type='button' and @class='btn bluetbn-btn confirmBtn']").click()  # 点击确定，关闭对话框
            sleep(3)
            #cgcg=Addsale()
            caigou.xscg('template3_table')
            # 判断是否有弹出警告框
            try:
                WebDriverWait(dr, 5, 0.1).until(EC.presence_of_element_located((By.ID, "notify_0")))
            except TimeoutException as e:
                print("单据提交失败")
                dr.get_screenshot_as_file("E:\\script\\report\\采购单据提交失败.jpg")
                self.assertEqual(0, 1, msg="单据提交失败")
        elif type==1: # 一般纳税人不带进销存
            return
        else:         # 小规模不带进销存
            return
    def tearDown(self):
        dr.quit()
if __name__ == '__main__':
    unittest.main()

