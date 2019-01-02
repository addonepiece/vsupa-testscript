"""
单据模块，列表搜索，获取单据总数，单据区间，检索数据
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
from test_case import pagebase
from selenium.common.exceptions import NoSuchElementException
from test_case.pagebase import Page


class billsearchlist(unittest.TestCase):
    """单据模块列表搜索"""
    global dr,bl
    @classmethod
    def setUpClass(cls):
        print("单据列表检索开始")
        global dr,kk
        # 实例化Page,并引用dr
        bl = Page()
        dr = bl.driver()
        bl.loginout("17700000001", "Abc123456")
        # 进入控制台做账视图，默认是单据页面
        # 进入控制台
        try:
            dr.find_element_by_xpath("//a[@href='/index']").click()
        except NoSuchElementException as e:
            print("登录跳转到了控制台")
        print("进入控制台")
        # 控制台搜索企业
        bl.kongzhitai("cyb0811企业")
        sleep(3)
    def getdate(self):  # 获取当前会计区间
        date = dr.find_element_by_xpath("//*[@id='list_view']/div/div[1]/div/div[1]/fieldset/div/div[1]/input")
        date2 = date.get_attribute("value")
        print("当前单据区间为:%r" % date2)
    def billcounts(self):  # 获取单据总数
        global count
        count = dr.find_element_by_xpath("//*[@id='list_view']/div/div[2]/div/div/div[1]/div[2]/div[4]/div/span[1]").text
        print("单据总数:" + count)
        return
    def searchtest(self, searchtype):
        global dr
        if searchtype=="按状态":   # 如果传入的参数是状态
            path="//*[@id='list_view']/div/div[2]/div/div/div[1]/div[2]/div[1]/table/thead/tr/th[6]/div/div/ul/li" #状态的定位地址
            statuspath="//*[@id='dlabel-status']"
        else:               # 传入的参数是缺单
            path="//*[@id='list_view']/div/div[2]/div/div/div[1]/div[2]/div[1]/table/thead/tr/th[7]/div/div/ul/li"
            statuspath="//*[@id='dlabel-lackPic']"
        lenth=len(dr.find_elements_by_xpath(path))
        i=0
        while i<lenth:
            search=dr.find_element_by_xpath(statuspath)
            search.click()
            ActionChains(dr).move_to_element(search)
            statuslists=search.find_elements_by_xpath(path)
            sleep(5)
            status=statuslists[i]
            status1=status.text
            #print(status1)
            status.click()
            sleep(4)
            count = dr.find_element_by_xpath("//*[@id='list_view']/div/div[2]/div/div/div[1]/div[2]/div[4]/div/span[1]").text
            print("检索项"+status1+"的单据总数:" + count)
            sleep(3)
            i=i+1
        dr.find_element_by_xpath("//*[@id='menu_list']/li/a").click()    # 重载模块，清除所选
        sleep(5)
    def bothsearch(self,type1,type2):
        # 联合搜索，先按状态搜，再按缺单搜，或是相反
        if type1=="按状态":
            path1="//*[@id='list_view']/div/div[2]/div/div/div[1]/div[2]/div[1]/table/thead/tr/th[6]/div/div/ul/li"
            statuspath1="//*[@id='dlabel-status']"
            path2="//*[@id='list_view']/div/div[2]/div/div/div[1]/div[2]/div[1]/table/thead/tr/th[7]/div/div/ul/li"
            statuspath2="//*[@id='dlabel-lackPic']"
        else:
            path1 ="//*[@id='list_view']/div/div[2]/div/div/div[1]/div[2]/div[1]/table/thead/tr/th[7]/div/div/ul/li"
            statuspath1 ="//*[@id='dlabel-lackPic']"
            path2 ="//*[@id='list_view']/div/div[2]/div/div/div[1]/div[2]/div[1]/table/thead/tr/th[6]/div/div/ul/li"
            statuspath2 ="//*[@id='dlabel-status']"
        lenth1=len(dr.find_elements_by_xpath(path1))
        lenth2=len(dr.find_elements_by_xpath(path2))
        a=1
        b=1
        while a<lenth1:
            search1=dr.find_element_by_xpath(statuspath1)
            search1.click()
            ActionChains(dr).move_to_element(search1).perform()
            statuslists1=search1.find_elements_by_xpath(path1)
            sleep(5)
            status1=statuslists1[a]
            status2=status1.text
            status1.click()
            sleep(10)
            while b<lenth2:
                search2=dr.find_element_by_xpath(statuspath2)
                search2.click()
                ActionChains(dr).move_to_element(search2)
                statuslists2=search2.find_elements_by_xpath(path2)
                sleep(5)
                status3=statuslists2[b]
                status4=status3.text
                status3.click()
                sleep(4)
                count = dr.find_element_by_xpath("//*[@id='list_view']/div/div[2]/div/div/div[1]/div[2]/div[4]/div/span[1]").text
                print(status2+"与"+status4+"联合搜索的数目是："+count)
                b=b+1
            a=a+1
            b=1
            sleep(5)
        dr.find_element_by_xpath("//*[@id='menu_list']/li/a").click()  # 重载模块，清除所选
    @classmethod
    def tearDownClass(cls):
        dr.quit()
    def search(self):
        """
        单据区间获取，总数获取，类别检索
        """
        billsearch=billsearchlist()
        billsearch.getdate()
        billsearch.billcounts()
        billsearch.searchtest("按状态")
        billsearch.searchtest("按缺单")
        billsearch.bothsearch("按状态","按缺单")


if __name__ == '__main__':
    unittest.main()
