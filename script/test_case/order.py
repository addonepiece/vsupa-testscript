import unittest
#coding=utf-8
import sys
from selenium import webdriver
from time import*
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os
from selenium.common.exceptions import NoSuchElementException
#import test_case.login
#from test_case.login import Login
from test_case.pagebase import Page
"""
此段脚本实现如下功能：登录系统，点击财税托管进入购买页面
判断纳税人类型，如果是小规模的选一般，如果是一般，选小规模
提交订单，如果有弹出框（提示纳税人类型与之前不一致），点关闭
提交订单
"""

class Order(unittest.TestCase):
    """企业账号订单购买，不含支付"""
    global dr
    def setUp(self):
        print("订单测试开始")
        global dr
        # 实例化Page,并引用dr
        o=Page()
        dr = o.driver()
        o.loginout("cybtest","Abc123456")
    def orderBuy(self):
        """登录企业账号进行下单"""
        sleep(6)
        # 购买财税托管
        try:
            dr.find_element_by_xpath("//*[@id='loginInfoBox']/li[1]/a")
        except NoSuchElementException as e:
            print("登录跳转到了控制台")
            dr.find_element_by_xpath("/html/body/div[1]/div[1]/a[1]/img").click()
            sleep(10)
        # 滚动一下页面，使得元素可见。不然定位不到元素
        dr.execute_script("window.scrollTo(0, 100);")
        sleep(3)
        tt=dr.find_element_by_id("service")
        tt02 = tt.find_element_by_xpath("//div[@data-index='0']")
        tt03 = tt02.find_element_by_xpath("//li[@data-intro-url='/homepage/product/account.html?id=account_agency']")
        ActionChains(dr).move_to_element(tt03).perform()
        sleep(3)
        tt03.find_element_by_xpath("//a[@href='/homepage/purchase/buy-account.html']").click()
        print("进入购买财税托管页面")
        sleep(6)
        # 跳转页面后要重新定位
        dr.switch_to_window(dr.window_handles[1])
        # 判断纳税人类型，如果原来是小规模，购买一般，如果是一般，购买小规模
        xiao = dr.find_element_by_xpath("//li[@value='account_agency_01']")
        yiban = dr.find_element_by_xpath("//li[@value='account_agency_02']")
        dd = xiao.get_attribute("class")
        if dd == 'active':
            yiban.click()
        else:
            xiao.click()
        # 提交订单
        dr.find_element_by_id("submitOrder").click()
        # 操作弹出框
        # 判断是否弹出框
        dr.switch_to_window(dr.window_handles[1])
        # 判断框是否存在
        try:
            dr.find_element_by_xpath("//a[@class='cancel-btn']")
            sleep(2)
            dr.find_element_by_xpath("//a[@class='confirm-btn']").click()
        except NoSuchElementException as e:
            print("购买类型与上次相同")
        # 判断验证订单是否提交
        sleep(3)
        try:
            dr.find_element_by_xpath("//*[@id='payBtn']")  # 检查页面是否存在立即支付按钮，存在即提交成功，不存在即下单失败
            print("提交订单成功")
        except NoSuchElementException as e:
            print("提交订单失败，请检查系统")

    def tearDown(self):
        sleep(3)
        print("订单流程结束")
        dr.quit()
if __name__ == '__main__':
    unittest.main()
