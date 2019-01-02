"""
create by yb.c  2017-10-30
账套的创建
"""

#coding=utf-8
import unittest
from selenium import webdriver

from time import *
from test_case.pagebase import Page   # 引入
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select
import random
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

class zhangtaoset(unittest.TestCase):
    global dr
    def setUp(self):
        global dr,zt
        # 实例化page，并引用dr
        zt=Page()
        dr=zt.driver()
        zt.loginout("17700000001","Abc123456")   # 登录财税师账号
        # 进入控制台
        try:
            dr.find_element_by_xpath("//a[@href='/index']").click()
        except NoSuchElementException as e:
            print("登录跳转到了控制台")
        print("进入控制台")
        # 搜索企业
        zt.kongzhitai("ccc企业30140325")
        sleep(3)
    def addzt(self):
        """
        没有账套，控制台搜索之后，直接在设置页面，添加账套
        有账套的企业，控制台搜索企业进入做账中心之后，默认是单据页面
        要判断，进去是否在设置页面
        :return:
        """
        global dr,i
        i=1
        # 点击设置
        dr.find_element_by_xpath("//*[@id='menu_list']/li[10]/a").click()
        try:
            dr.find_element_by_xpath("//*[@id='layui-layer1']/div[2]/a").click()    # 没有账套点击设置，会弹出无账套对话框
            i=i+1
        except NoSuchElementException as e:
            print("企业有账套")
        sleep(2)
        # 判断是否在账套页面，无需判断是否有账套。是添加还是编辑。返回至列表页，再进行添加
        try:
            dr.find_element_by_xpath("//*[@id='backToPackage']").click()
        except NoSuchElementException as e:
            print("不在账套视图页面")
        sleep(2)
        # 点击添加
        dr.find_element_by_xpath("//*[@id='addAccountPackageBtn']").click()
        sleep(5)
        # 定位
        ztname = dr.find_element_by_xpath("//*[@id='name']")
        zhidu = dr.find_element_by_xpath("//*[@id='accountSystemId']")
        hangye = dr.find_element_by_xpath("//*[@id='accountPackageForm']/div[1]/div[3]/div[1]/fieldset/div[3]/div/span/span[1]/span")  # 只是行业元素的定位，如果要设置行业，需要点击选择
        zsfs = dr.find_element_by_xpath("//*[@id='levyMode']")
        qydata = dr.find_element_by_xpath("//*[@id='startAccountPeriod']")
        nsrtype = dr.find_element_by_xpath("//*[@id='accountType']")
        # 本位币默认人民币，不设置
        hdl = dr.find_element_by_xpath("//*[@id='approvedRate']")
        jxcqy = dr.find_element_by_xpath("//*[@id='invoicingStartAccountperiod']")

        # Action
        # 写入账套名
        now = time.strftime("%d%H%M%S")
        ztname.clear()
        ztname.send_keys(str("账套"+now))
        # 选择财务制度
        #zhidu.click()
        sleep(2)
        Select(zhidu).select_by_visible_text("企业会计准则 beta版")
        sleep(2)
        # 设置行业
        hangye.click()
        sleep(3)
        hangyelist=dr.find_elements_by_xpath("/html/body/span/span/span[2]/ul/li")   # 行业的列表
        hangyelist[6].click()  # 选择F
        # 设置征收方式
        zsfs.click()
        sleep(2)
        Select(zsfs).select_by_visible_text("国月查")  # 选择国月查，国月查不需要设置核定率
        sleep(2)
        # 设置启用时间
        qydata.click()
        sleep(3)
        qydatalist=dr.find_elements_by_xpath("//*[@id='rightContainer']/div[4]/div[4]/table/tbody/tr/td/span")
        data1=random.randint(0,11)
        qydatalist[data1].click()  # 1-12月，从0开始.
        sleep(2)
        # 设置纳税人类型
        Select(nsrtype).select_by_value(str(random.randint(1,2)))
        sleep(2)
        # 设置进销存
        jxcqy.click()
        sleep(3)
        jxcqylist=dr.find_elements_by_xpath("//*[@id='rightContainer']/div[3]/div[4]/table/tbody/tr/td/span")
        try:
            jxcqylist[str(random.randint(0,data1-1))].click()
        except Exception as e:
            print("进销存启用时间不得早于账套启用")
        else:
            self.assertEqual(0,1,msg="进销存日期可早于起始月")
        data2=random.randint(data1,11)
        jxcqylist[data2].click()
        sleep(3)
        # 提交账套
        dr.find_element_by_xpath("//*[@id='rightContainer']/div[1]/div/div[2]/a[1]").click()
        sleep(2)
        # 显示等待
        gou=dr.find_element_by_xpath("//*[@id='""layui-layer"+str(i)+"']/div[3]/div/label/input")
        # 如果已有账套，点设置不弹出提示框，这个提交提示框是第一个框，layer1.如果无账套，弹出了框，这个提交提示框
        # 是第二个框，layer2
        #WebDriverWait(dr,12,2).until(EC.element_to_be_clickable(gou))
        sleep(10)
        gou.click()  # 勾选已阅读同意
        sleep(2)
        dr.find_element_by_xpath("//*[@id='""layui-layer"+str(i)+"']/div[3]/a[1]").click()  # 点击确定
        # 如果有账套，点设置没有弹出框。这是第二个框。如果无账套，弹出了提示框。这是第三个框
        sleep(3)
        # 弹出是否设置核定税种，点击取消
        dr.find_element_by_xpath("//*[@class='whitegray-btn btn-cancel' and @type='button']").click()
    def tearDown(self):
        dr.quit()
if __name__ == '__main__':
    unittest.main()
