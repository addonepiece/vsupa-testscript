"""
财税师登录系统，进入控制台，判断纳税人类型，录入费用单
流程，登录，切换控制台，进入单据
"""
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
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from test_case.pagebase import Page
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

class fyBill(unittest.TestCase):
    """费用单据添加"""
    global dr,fy
    def setUp(self):
        print("录制费用单据用例开始")
        global dr,fy
        # 实例化Page,并引用dr
        fy = Page()
        dr = fy.driver()
        fy.loginout("17700000001", "Abc123456")
    def AddFy(self):
        """
        费用单据添加
        :return:
        """
        global dr,fy
        # 进入控制台
        try:
            dr.find_element_by_xpath("//a[@href='/index']").click()
        except Exception as e:
            print("登录跳转到了控制台")
        print("进入控制台")
        # 控制台搜索企业
        fy.kongzhitai("cyb0811企业")
        sleep(3)
        # 判断纳税人类型，来知道单据添加页面有哪些字段需要设置
        fy.pagecount()
        type=fy.pagecount() # pagecount返回了企业的类型，打印出来
        # 进入单据添加页面，默认添加的是费用单据
        dr.find_element_by_xpath("//*[@id='menu_list']/li/a").click()  # 进入单据页面
        print("进入单据模块")
        sleep(3)
        dr.find_element_by_xpath("//*[@id='list_view']/div/div[1]/div/div[2]/fieldset/div[1]/div/button[1]").click()  # 点击添加
        print("进入单据添加页面")
        sleep(5)
        # 获取付款方式
        fy.paymethod()
        # 判断纳税人类型，录入各个字段
        # 名称设置
        fymingcheng = dr.find_element_by_xpath("//*[@id='template1_table']/tbody/tr/td[2]/div[1]")
        fymingcheng.click()
        ActionChains(dr).move_to_element(fymingcheng).perform()
        sleep(2)
        # 获取名称列表并随机点击一个名称
        fymclists = dr.find_elements_by_xpath("//*[@id='template1_table']/tbody/tr/td[2]/div[2]/div/span/div/div/div")
        fymclists[random.randint(0, len(fymclists) - 1)].click()
        print("随机选择一个费用名称")
        # 部门设置，获取部门列表，随机选择一个部门
        dr.find_element_by_xpath("//*[@id='template1_table']/tbody/tr/td[3]/div[1]").click()
        sleep(2)
        bumen = dr.find_element_by_xpath("//*[@id='template1_table']/tbody/tr/td[3]/div[2]/div//select")
        Select(bumen).select_by_value(str(random.randint(1, 3)))
        print("随机选择部门")
        # 金额设置
        jine = dr.find_element_by_xpath("//div[@class='cell_data pr30']")
        sleep(2)
        jine.click()
        sleep(2)
        jine2 = jine.get_attribute("class")
        if jine2 == "cell_data pr30 hide":
            dr.find_element_by_xpath("//*[@id='template1_table']/tbody/tr/td[4]/div[2]/div/input").send_keys(str(random.uniform(0, 999999999)))
            # print("费用金额写入%r"%je)
        else:
            print("金额为空")
        if type==0 or type==1: # 如果是一般纳税人企业（带进销存或不带），费用包含：名称，部门，金额，税率，税额5个字段
            print("该企业是一般纳税人带进销存，有五个参数，名称，部门，金额，税率，税额，需要设置税率和税额")
            # 税率设置
            dr.find_element_by_xpath("//*[@id='template1_table']/tbody/tr/td[5]/div[1]").click()
            sleep(2)
            shuilv=dr.find_element_by_xpath("//*[@id='template1_table']/tbody/tr/td[5]/div[2]/div/select")
            print(shuilv.text)
            sleep(5)
            shuilvcount=len(shuilv.find_elements_by_tag_name("option"))
            Select(shuilv).select_by_index(random.randint(0, shuilvcount - 1))    # 选择随机value税率
            sleep(3)
            print("随机选择税率")
        # 预览凭证
        dr.find_element_by_xpath("//a[@role='button' and @class='lightblue-btn previewVoucher']").click()
        sleep(3)
        dr.find_element_by_xpath("//button[@type='button' and @class='bootbox-close-button close']").click()
        print("预览凭证成功")
        sleep(2)
        # 提交单据
        dr.find_element_by_xpath("//a[@role='button' and @class='bluetbn-btn save' and @data-status='2']").click()
        # 判断是否添加成功

        #try:
       #     text = dr.find_element_by_xpath("//*[@id='layui-layer1']/div[1]").text
        #    self.assertNotIn("Exception", text, msg="失败了")
        #except NoSuchElementException as e:
         #   print("单据添加成功")
        # 判断是否有提示提交成功
        try:
            WebDriverWait(dr,5,0.1).until(EC.presence_of_element_located((By.ID,"notify_0")))
        except TimeoutException as e:
            print("单据提交失败")
            dr.get_screenshot_as_file("E:\\script\\report\\费用单据提交失败.jpg")
            self.assertEqual(0,1,msg="单据提交失败")
    def tearDown(self):
        dr.quit()

if __name__ == '__main__':
    unittest.main()

