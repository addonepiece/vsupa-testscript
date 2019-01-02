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


class shoukuanbill(unittest.TestCase):
    """收款单录单"""
    global dr, sk
    def setUp(self):
        print("录制收款单据开始")
        global dr, sk
        # 实例化Page,并引用dr
        sk = Page()
        dr = sk.driver()
        sk.loginout("17700000001", "Abc123456")
        sleep(6)
        # 进入控制台。搜索企业
        try:
            dr.find_element_by_xpath("//a[@href='/index']").click()
        except Exception as e:
            print("登录跳转到了控制台")
        print("进入控制台")
        # 控制台搜索企业
        sk.kongzhitai("cyb0811企业")
        sleep(3)
    def skbilladd(self):
        """
         收款类单据，有三个字段，收款方式，付款方，还有一个付款方明细。金额。
        付款方是默认的五类，利息，客户，供应商，其他往来，股东。利息没有明细，其他四项有。选择的时候要判断是否需要填写明细
        :return:
         """
        global dr
        # 进入单据添加页面，切换单据类型
        dr.find_element_by_xpath("//*[@id='menu_list']/li/a").click()  # 进入单据页面
        print("进入单据模块")
        sleep(3)
        dr.find_element_by_xpath(
            "//*[@id='list_view']/div/div[1]/div/div[2]/fieldset/div[1]/div/button[1]").click()  # 点击添加
        print("进入单据添加页面")
        sleep(3)
        sk.changetype(3)
        sleep(3)
        sk.paymethod()
        # 付款方获取
        dr.find_element_by_xpath("//*[@id='template4_table']/tbody/tr/td[2]/div[1]").click()
        sleep(2)
        fkf = dr.find_element_by_xpath("//*[@id='template4_table']/tbody/tr/td[2]/div[2]/div/select")
        print(fkf.text)
        fkflist = dr.find_elements_by_xpath("//*[@id='template4_table']/tbody/tr/td[2]/div[2]/div/select")
        f = random.choice([30, 20, 21, 22, 23])
        print(f)
        Select(fkf).select_by_value(str(f))
        sleep(4)
        # 如果选择的是利息，不需要明细，如果不是利息，则需要设置下一个字段
        sleep(3)
        if f != 30:  # value值是30，是利息,利息不需要明细。不是利息时，需要操作下一个字段
            # 获取明细列表，看是否为空
            fkfmx = dr.find_element_by_xpath("//*[@id='template4_table']/tbody/tr/td[3]/div[2]/div/span/div")  # 付款方明细变成可见后，元素xpath
            fkfmxlist = dr.find_elements_by_xpath("//*[@id='template4_table']/tbody/tr/td[3]/div[2]/div/span/div/div/div")  # 获取付款方明细列表
            print(fkfmx.text)  # 打印付款方明细名称
            fkfcount = len(fkfmxlist)
            print(fkfcount)
            if fkfcount == 2:  # 如果序列中有两个原素，就是说明细为空。两个原素是添加，和未检测到数据。此时操作添加按钮
                fkfmxlist[-1].click()  # 添加是序列的最后一个元素，点击添加，弹出对话框
                sleep(3)
                dr.find_element_by_xpath("//*[@id='name']").send_keys("测试1311")
                dr.find_element_by_xpath("//*[@id='layui-layer1']/div[3]/a[1]").click()  # 关闭添加对话框
                # 添加完付款方明细后，也不会自动添加。执行手动随机选择操作
                sleep(3)
                dr.find_element_by_xpath(
                    "//*[@id='template4_table']/tbody/tr/td[3]/div[1]").click()  # 鼠标点击付款方明细，让元素列表可见
            # 获取明细列表，看是否为空
            fkfmx2 = dr.find_element_by_xpath(
                "//*[@id='template4_table']/tbody/tr/td[3]/div[2]/div/span/div")  # 付款方明细变成可见后，元素xpath
            fkfmxlist2 = dr.find_elements_by_xpath(
                "//*[@id='template4_table']/tbody/tr/td[3]/div[2]/div/span/div/div/div")  # 获取付款方明细列表
            # 需要去除添加
            del fkfmxlist2[-1]
            fkfcount2 = len(fkfmxlist2)
            fkfmxlist2[random.randint(0, fkfcount2 - 1)].click()
        # 写入金额
        sleep(3)
        dr.find_element_by_xpath("//*[@id='template4_table']/tbody/tr/td[4]/div[1]").click()
        dr.find_element_by_xpath("//*[@id='template4_table']/tbody/tr/td[4]/div[2]/div/input").send_keys(
            str(random.uniform(1, 999999999)))
        sleep(3)
        # 预览凭证
        dr.find_element_by_xpath("//a[@role='button' and @class='lightblue-btn previewVoucher']").click()
        sleep(3)
        dr.find_element_by_xpath("//button[@type='button' and @class='bootbox-close-button close']").click()
        print("预览凭证成功")
        sleep(2)
        # 提交单据
        dr.find_element_by_xpath("//a[@role='button' and @class='bluetbn-btn save' and @data-status='2']").click()
        print("提交收款单据")
        try:
            WebDriverWait(dr, 5, 0.1).until(EC.presence_of_element_located((By.ID, "notify_0")))
        except TimeoutException as e:
            print("单据提交失败")
            dr.get_screenshot_as_file("E:\\script\\report\\收款单据提交失败.jpg")
            self.assertEqual(0, 1, msg="单据提交失败")
        sleep(5)

    def tearDown(self):
        dr.quit()

if __name__ == '__main__':
    unittest.main()
