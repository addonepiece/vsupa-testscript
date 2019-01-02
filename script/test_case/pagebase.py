"""
该文件定义一些基础类，供其他文件调用。
"""
import unittest
from selenium import webdriver
from time import *
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os
import select
from selenium.webdriver.support.select import Select
from random import choice
import random
from random import randrange
from  random import uniform
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import NoSuchElementException

class Page(object):
    """
    基础类，用于页面对象的继承
    """
    global dr
    def __init__(self):
        print("test begin")
    def driver(self):  # 定义浏览器dr
        global dr
        url = "http://test.vsupa.com/homepage/login.html"
        dr = webdriver.Chrome()
        dr.maximize_window()
        dr.get(url)
        return dr     # 返回dr的值，供其他case使用
    def loginout(self,username,password):
        global dr
        sleep(2)
        # 输入用户名，输入密码，登录
        dr.find_element_by_id("loginName").send_keys(username)
        dr.find_element_by_id("password").send_keys(password)
        sleep(2)
        dr.find_element_by_id("loginBtn").click()
        sleep(5)
        try:
            dr.find_element_by_xpath("//*[@id='loginInfoBox']/li[1]/a")
        except NoSuchElementException as e:
            return False
            #print("登录失败，请查看系统是否有异常")
        return True
        #print("登录成功，登录功能无异常")
# 进入控制台，控制台搜索企业
    def kongzhitai(self,enterprisename):
        try:
            dr.find_element_by_xpath("//*[@id='control_area']/span[1]/input")  # 如果有控制台输入框，就是财税师财税机构角色
            kongzhitai = dr.find_element_by_xpath("//input[@type='text' and @class='custom-search type_finace_control tt-input']")
            kongzhitai.send_keys(enterprisename)
            sleep(2)
            print("在管理控制台输入企业")
            ActionChains(dr).move_to_element(kongzhitai).perform()  # 鼠标悬停
            sleep(2)
            dr.find_element_by_xpath("//div[@class='ls-menu tt-open']").click()
            print("进入企业做账模块")
            sleep(5)
        except NoSuchElementException as e:   # 企业或是财务角色，进入财税模块
            dr.find_element_by_xpath("//*[@id='type_enterprise']").click()
# 获取纳税人类型
    def pagecount(self):
        # 进入设置页面，账套页面
        dr.find_element_by_xpath("//*[@id='menu_list']/li[10]/a").click() # 点击设置，进入设置页面，默认显示账套详情页
        sleep(2)
        # 获取账套起始月
        start = dr.find_element_by_id("startAccountPeriod")
        startaccount = start.get_attribute("value")
        # 获取纳税人类型
        type = dr.find_element_by_xpath("//*[@id='accountType']")
        type1 = type.get_attribute("value")
        if type1 == "2":  # type为2是一般纳税人
            type1 = "一般纳税人"
            update1 = "没有升级时间"
            #return type1
        elif type1 == "1":   # type为1是小规模纳税人
            type1 = "小规模纳税人"
            #return type1  # 如果是小规模纳税人，获取升级时间
            update = dr.find_element_by_xpath("//*[@id='upgradeAccountPeriod']")
            update1 = update.get_attribute("value")
        # 获取进销存信息
        jxc = dr.find_element_by_xpath("//*[@id='invoicingStartAccountperiod']")
        jinxiaocundate1 = jxc.get_attribute("value")
        if "-" in jinxiaocundate1:
            jxctype = 1 # 为1启用了进销存
            jinxiaocundate = jinxiaocundate1
            #return jxctype
        else:
            jxctype = 0
            jinxiaocundate = "企业没有开启进销存"
            #return jxctype
        countmsg = str(
            "纳税人类型是：" + type1 + "账套启用时间是：" + startaccount + "账务升级时间是：" + update1 + "进销存启用时间是：" + jinxiaocundate)
        # 联合判断类型
        if type1=="一般纳税人" and jxctype==1:
            counttype=0
            return counttype
        elif type1=="一般纳税人" and jxctype==0:
            counttype=1
            return counttype
        elif type1=="小规模纳税人" and jxctype==1:
            counttype=2
            return counttype
        elif type1=="小规模纳税人" and jxctype==0:
            counttype=3
            return counttype
# 单据获取付款方式，目前写的是全部都设置为现金，不是现金的设置为现金
    def paymethod(self):  # 获取付款方式，添加，选择付款方式
        pay_method = dr.find_element_by_id("pay_method")
        pay_method2 = dr.find_element_by_id("select2-pay_method-container")
        method = pay_method2.get_attribute("title")
        if method != "现金":
            print("付款方式不是现金")
            pay_method2.click()
            Select(pay_method).select_by_value("noChild-1")
            print("付款方式改为现金")
            pay_method2.click()
            # 收起下拉框
        else:
            print("付款方式是现金")
            sleep(5)

# 单据切换类型

    def changetype(self, i):
        self.i = i
        billtype = dr.find_element_by_xpath("//*[@id='detail_view']/div/div/div[1]/div/div[1]/div[1]/div[1]/select")
        dr.find_element_by_xpath("//*[@id='detail_view']/div/div/div/div/div/div/div/span/span/span").click()
        ActionChains(dr).move_to_element(billtype)
        sleep(2)
        dr.find_elements_by_xpath("html/body/span/span/span[2]/ul/li")[i].click()
# 进入单据添加页面
    def billadd(self):
        dr.find_element_by_xpath("//*[@id='menu_list']/li/a").click()  # 进入单据页面
        print("进入单据模块")
        sleep(3)
        dr.find_element_by_xpath("//*[@id='list_view']/div/div[1]/div/div[2]/fieldset/div[1]/div/button[1]").click()  # 点击添加
        print("进入单据添加页面")
        sleep(5)
    def xscg(self,x):
        global dr
        """
            这个函数提取的功能是，销售和采购单据，销售和采购添加函数会调用。一般纳税人带进销存的，获取商品列表，添加商品，设置金额，数量等。
            需要传入1个参数。
            :param x: 商品名称的xpath地址,,销售是template2_table,采购是template3_table,就数字不一样，用传参的方式写入
            :return:
        """
        print("获取商品列表")
        sp = dr.find_element_by_xpath("//*[@id='" + x + "']/tbody/tr/td[4]/div[1]")  # 商品元素定位
        sp.click()  # 点击商品元素
        sleep(5)
        ActionChains(dr).move_to_element(dr.find_element_by_xpath("//*[@id='" + x + "']/tbody/tr/td[4]/div[1]"))   # 鼠标悬停
        bbb = dr.find_element_by_xpath("//*[@id='" + x + "']/tbody/tr/td[4]/div[2]/div/span/div/div")    # 获取打印商品名称
        ccc = bbb.text
        print(ccc)
        splists = dr.find_elements_by_xpath("//*[@id='" + x + "']/tbody/tr/td[4]/div[2]/div/span/div/div/div")
        sleep(5)
        # 如果商品只有两个，就是没有商品，两个是'未检测到数据'和’添加‘。此时需要添加商品
        if len(splists) == 2:
            splists[-1].click()  # 点击最后一项，即为添加
            sleep(3)
            dr.find_element_by_xpath("//*[@id='name']").send_keys("商品1")  # 写入商品名称
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
                sleep(4)
                # dr.find_element_by_xpath("//*[id='addCommodityUtil']/fieldset/div/div/input").click()
                dr.find_element_by_xpath(
                    "//*[@id='name' and @placeholder='最大长度16位' and @data-bv-field='name']").send_keys("单位1")  # 随机输入单位名称
                dr.find_element_by_xpath("//button[@type='button' and @class='btn bluetbn-btn dir']").click()  # 关闭对话框
                sleep(4)
            else:
                print("单位选默认值")
            dr.find_element_by_xpath("//button[@type='button' and @class='btn bluetbn-btn']").click()  # 关闭添加单位对话框
            sleep(5)
            # 写入后，商品不会自动填充，还是要去选择商品
            sp.click()
            sleep(5)
            ActionChains(dr).move_to_element(dr.find_element_by_xpath("//*[@id='" + x + "']/tbody/tr/td[4]/div[1]"))
            bbb = dr.find_element_by_xpath("//*[@id='" + x + "']/tbody/tr/td[4]/div[3]/div/span/div/div")
            ccc = bbb.text
            print(ccc)
            splists = dr.find_elements_by_xpath("//*[@id='" + x + "']/tbody/tr/td[4]/div[2]/div/span/div/div/div")
            sleep(5)
            del splists[-1]  # 去除掉添加
            del splists[0]  # 去掉折扣.折扣排在第一位。去掉折扣
            #spcount = len(splists)
            #spcount = len(splists)
            spcount = len(splists)
            print("该企业销售单可用商品有%r个" % spcount)
            # 随机选择一个商品
            # 鼠标悬停，点击随机序列号
            splists[random.randint(0, spcount - 1)].click()
            sleep(6)
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
            sleep(6)
            spm = sp.text
            print("随机选择一个商品%r" % spm)
            # 单位自动获取，不用设置，但是要获取单位的值
            sleep(2)
            spdw = dr.find_element_by_xpath("//*[@id='" + x + "']/tbody/tr/td[5]/div[1]").text
            print("商品单位为：%r" % spdw)
            # 数量设置
            dr.find_element_by_xpath("//*[@id='" + x + "']/tbody/tr/td[6]/div[1]").click()
            dr.find_element_by_xpath("//*[@id='" + x + "']/tbody/tr/td[6]/div[2]/div/input").send_keys(str(random.randint(0, 999999999)))
            print("随机设置数量")
            # 金额设置

            dr.find_element_by_xpath("//*[@id='" + x + "']/tbody/tr/td[8]/div[1]").click()
            dr.find_element_by_xpath("//*[@id='" + x + "']/tbody/tr/td[8]/div[2]/div/input").send_keys(str(random.uniform(0, 999999999)))

            # 设置税率，税率自动显示了，不显示
            # dr.find_element_by_xpath("//*[@id='"+x+"']/tbody/tr/td[9]/div[1]").click()
            # dr.find_element_by_xpath("//*[@id='"+x+"']/tbody/tr/td[9]/div[2]/div/input").send_keys("0.17")
            # print("设置税率0.17，自动计算税额")

            # 单价自动计算，获取单价
            sleep(5)
            spdj = dr.find_element_by_xpath("//*[@id='" + x + "']/tbody/tr/td[7]/div[1]").text
            print("商品单价为：%r" % spdj)
            # 预览凭证
            sleep(3)
            dr.find_element_by_xpath("//*[@id='footer_title']/div/div[1]/a").click()  # 点击预览凭证
            sleep(5)
            dr.find_element_by_xpath("//button[@type='button' and @class='bootbox-close-button close']").click()  # 关闭预览对话框
            # 提交单据
            sleep(3)
            dr.find_element_by_xpath("//*[@id='footer_title']/div/div[4]/a").click()  # 提交单据


