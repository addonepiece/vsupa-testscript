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


class fukuanbill(unittest.TestCase):
    """付款单录单"""
    global dr, fk
    def setUp(self):
        print("录制付款单据开始")
        global dr, fk
        # 实例化Page,并引用dr
        fk = Page()
        dr = fk.driver()
        fk.loginout("17700000001", "Abc123456")
        # 进入控制台。搜索企业
        try:
            dr.find_element_by_xpath("//a[@href='/index']").click()
        except NoSuchElementException as e:
            print("登录跳转到了控制台")
        print("进入控制台")
        # 控制台搜索企业
        fk.kongzhitai("cyb0811企业")
        sleep(3)
    def fkbilladd(self):
        # 进入单据添加页面，切换单据类型
        dr.find_element_by_xpath("//*[@id='menu_list']/li/a").click()  # 进入单据页面
        print("进入单据模块")
        sleep(3)
        dr.find_element_by_xpath("//*[@id='list_view']/div/div[1]/div/div[2]/fieldset/div[1]/div/button[1]").click()  # 点击添加
        print("进入单据添加页面")
        sleep(3)
        fk.changetype(4)
        sleep(3)
        fk.paymethod()
        # 收款方获取
        dr.find_element_by_xpath("//*[@id='template5_table']/tbody/tr/td[2]/div[1]").click()
        sleep(2)
        skf = dr.find_element_by_xpath("//*[@id='template5_table']/tbody/tr/td[2]/div[2]/div/select")
        print(skf.text)
        skflist = dr.find_elements_by_xpath("//*[@id='template5_table']/tbody/tr/td[2]/div[2]/div/select")
        s = random.choice([20, 21, 22, 23])
        print(s)
        Select(skf).select_by_value(str(s))
        sleep(4)
        # 获取明细列表，看是否为空
        if s==20:
            dr.find_element_by_xpath("//*[@id='template5_table']/tbody/tr/td[3]/div[1]").click()
        skfmx = dr.find_element_by_xpath("//*[@id='template5_table']/tbody/tr/td[3]/div[2]/div/span/div")  # 收款方明细变成可见后，元素xpath
        skfmxlist = dr.find_elements_by_xpath("//*[@id='template5_table']/tbody/tr/td[3]/div[2]/div/span/div/div/div")  # 获取收款方明细列表
        print(skfmx.text)  # 打印收款方明细名称
        skfcount = len(skfmxlist)
        print(skfcount)
        if skfcount == 2:  # 如果序列中有两个原素，就是说明细为空。两个原素是添加，和未检测到数据。此时操作添加按钮
            skfmxlist[-1].click()  # 添加是序列的最后一个元素，点击添加，弹出对话框
            sleep(3)
            dr.find_element_by_xpath("//*[@id='name']").send_keys("测试11321")
            dr.find_element_by_xpath("//*[@id='layui-layer2']/div[3]/a[1]").click()  # 关闭添加对话框
            # 添加完收款方明细后，也不会自动添加。执行手动随机选择操作
            sleep(3)
            dr.find_element_by_xpath("//*[@id='template5_table']/tbody/tr/td[3]/div[1]").click()  # 鼠标点击付款方明细，让元素列表可见
        # 获取明细列表，看是否为空
        skfmx2 = dr.find_element_by_xpath(
            "//*[@id='template5_table']/tbody/tr/td[3]/div[2]/div/span/div")  # 收款方明细变成可见后，元素xpath
        skfmxlist2 = dr.find_elements_by_xpath(
            "//*[@id='template5_table']/tbody/tr/td[3]/div[2]/div/span/div/div/div")  # 获取收款方明细列表
        # 需要去除添加
        del skfmxlist2[-1]
        skfcount2 = len(skfmxlist2)
        skfmxlist2[random.randint(0, skfcount2 - 1)].click()
        # 写入金额
        sleep(3)
        dr.find_element_by_xpath("//*[@id='template5_table']/tbody/tr/td[4]/div[1]").click()
        dr.find_element_by_xpath("//*[@id='template5_table']/tbody/tr/td[4]/div[2]/div/input").send_keys(
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
        print("提交付款单据成功")
        try:
            WebDriverWait(dr, 5, 0.1).until(EC.presence_of_element_located((By.ID, "notify_0")))
        except TimeoutException as e:
            print("单据提交失败")
            dr.get_screenshot_as_file("E:\\script\\report\\付款单据提交失败.jpg")
            self.assertEqual(0, 1, msg="单据提交失败")
        sleep(5)

    def tearDown(self):
        dr.quit()

if __name__ == '__main__':
    unittest.main()
