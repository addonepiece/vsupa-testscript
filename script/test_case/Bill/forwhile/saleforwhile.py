# 循环录制销售单据500行，不进行提交操作。此脚本有前置条件，1、客户不为0，不需要添加。只是循环添加商品，添加行数。
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
import time

class saleforwhile(unittest.TestCase):
    """销售单录单"""
    global dr, salefor
    def setUp(self):
        print("录制销售单据开始")
        global dr, salefor
        # 实例化Page,并引用dr
        salefor= Page()
        dr = salefor.driver()
        salefor.loginout("17700000001", "123456")
        # 进入控制台。搜索企业
        try:
            dr.find_element_by_xpath("//a[@href='/index']").click()
        except NoSuchElementException as e:
            print("登录跳转到了控制台")
        print("进入控制台")
        # 控制台搜索企业
        salefor.kongzhitai("cyb0605测试企业")
        sleep(2)

    def saleforwhilewhile(self):

        global dr,salefor
        sleep(2)
        # 判断纳税人类型
        dr.find_element_by_xpath("//*[@id='menu_list']/li/a").click()  # 进入单据页面
        print("进入单据模块")
        sleep(2)
        dr.find_element_by_xpath("//*[@id='list_view']/div/div[1]/div/div[2]/fieldset/div[1]/div/button[1]").click()  # 点击添加
        print("进入单据添加页面")
        sleep(2)
        salefor.changetype(1)
        # 获取付款方式
        salefor.paymethod()
        # 选择客户
        dr.find_element_by_xpath("//*[@id='select2-auxiliary_users-container']").click()
        sleep(2)
        kh=dr.find_element_by_xpath("//*[@id='select2-auxiliary_users-results']")
        khlist = dr.find_elements_by_xpath("html/body/span/span/span[2]/ul/li")
        khcount=len(khlist)
        y=random.randint(0,khcount-1)
        khlist[y].click()
        sleep(2)
        i=1
        while i<200:   # 录制，录完加一行
            # 选商品，商品不够，添加商品
            sp = dr.find_element_by_xpath("//*[@id='template2_table']/tbody/tr["+str(i)+"]/td[4]/div[1]")  # 商品元素定位
            sp.click()  # 点击商品元素
            sleep(2)
            ActionChains(dr).move_to_element(
                dr.find_element_by_xpath("//*[@id='template2_table']/tbody/tr["+str(i)+"]/td[4]/div[1]"))  # 鼠标悬停
            bbb = dr.find_element_by_xpath("//*[@id='template2_table']/tbody/tr["+str(i)+"]/td[4]/div[2]/div/span/div/div")  # 获取打印商品名称
            ccc = bbb.text
            print(ccc)
            splists = dr.find_elements_by_xpath("//*[@id='template2_table']/tbody/tr["+str(i)+"]/td[4]/div[2]/div/span/div/div/div")
            sleep(2)
            # 如果商品只有两个，就是没有商品，两个是'未检测到数据'和’添加‘。此时需要添加商品
            if len(splists) == 2:
                splists[-1].click()  # 点击最后一项，即为添加
                sleep(2)
                now=time.strftime("%d%H%M%S")
                spname="商品"+now
                dr.find_element_by_xpath("//*[@id='name']").send_keys(str(spname))  # 写入商品名称
                sleep(2)
                # 判断是否有单位，没有的话，添加
                # 获取单位的select的option个数，为0时单位为空
                dw = dr.find_element_by_xpath("//*[@id='commodityUnitId']")
                dw.click()
                sleep(2)
                dwcount = len(dw.find_elements_by_tag_name("option"))
                print(dwcount)
                if dwcount == 0:  # 为0表示没有单位数据，要添加单位
                    dr.find_element_by_xpath("//*[@id='addUnits']/img").click()  # 添加单位，点击弹出添加框
                    sleep(2)
                    # dr.find_element_by_xpath("//*[id='addCommodityUtil']/fieldset/div/div/input").click()
                    dr.find_element_by_xpath(
                        "//*[@id='name' and @placeholder='最大长度16位' and @data-bv-field='name']").send_keys(
                        "单位1")  # 随机输入单位名称
                    dr.find_element_by_xpath(
                        "//button[@type='button' and @class='btn bluetbn-btn dir']").click()  # 关闭对话框
                    sleep(2)
                else:
                    print("单位选默认值")
                dr.find_element_by_xpath("//button[@type='button' and @class='btn bluetbn-btn']").click()  # 关闭添加单位对话框
                sleep(2)
                # 写入后，商品不会自动填充，还是要去选择商品
                sp.click()
                sleep(2)
                ActionChains(dr).move_to_element(dr.find_element_by_xpath("//*[@id='template2_table']/tbody/tr["+str(i)+"]/td[4]/div[1]"))
                bbb = dr.find_element_by_xpath("//*[@id='template2_table']/tbody/tr["+str(i)+"]/td[4]/div[3]/div/span/div/div")
                ccc = bbb.text
                print(ccc)
                splists = dr.find_elements_by_xpath("//*[@id='template2_table']/tbody/tr["+str(i)+"]/td[4]/div[2]/div/span/div/div/div")
                sleep(2)
                del splists[-1]  # 去除掉添加
                del splists[0]  # 去掉折扣.折扣排在第一位。去掉折扣
                # spcount = len(splists)
                # spcount = len(splists)
                spcount = len(splists)
                print("该企业销售单可用商品有%r个" % spcount)
                # 随机选择一个商品
                # 鼠标悬停，点击随机序列号
                splists[random.randint(0, spcount - 1)].click()
                sleep(2)
                spm = sp.text
                print("随机选择一个商品%r" % spm)
            else:
                del splists[-1]  # 去除掉添加
                del splists[0]  # 去掉折扣
                spcount = len(splists)
                spcount = len(splists)
                spcount = len(splists)
                print("该企业销售单可用商品有%r个" % spcount)
                # 随机选择一个商品
                # 鼠标悬停，点击随机序列号
                splists[random.randint(0, spcount - 1)].click()
                sleep(2)
                spm = sp.text
                print("随机选择一个商品%r" % spm)
                # 单位自动获取，不用设置，但是要获取单位的值
                sleep(2)
                spdw = dr.find_element_by_xpath("//*[@id='template2_table']/tbody/tr["+str(i)+"]/td[5]/div[1]").text
                print("商品单位为：%r" % spdw)
                # 数量设置
                dr.find_element_by_xpath("//*[@id='template2_table']/tbody/tr["+str(i)+"]/td[6]/div[1]").click()
                dr.find_element_by_xpath("//*[@id='template2_table']/tbody/tr["+str(i)+"]/td[6]/div[2]/div/input").send_keys(
                    str(random.randint(1, 100)))
                print("随机设置数量")
                # 金额设置

                dr.find_element_by_xpath("//*[@id='template2_table']/tbody/tr["+str(i)+"]/td[8]/div[1]").click()
                dr.find_element_by_xpath("//*[@id='template2_table']/tbody/tr["+str(i)+"]/td[8]/div[2]/div/input").send_keys(
                    str(random.uniform(1, 100)))
            # 新增一行
            sleep(3)
            dr.find_element_by_xpath("//*[@id='template2_table']/tbody/tr["+str(i)+"]/td[1]/div/img[1]").click()
            i=i+1
    def tearDown(self):
        print("录制500条")
if __name__ == '__main__':
    unittest.main()
