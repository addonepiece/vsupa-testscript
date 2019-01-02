"""
资产减少单据。只能操作资产有数据的，无数据时不录单，直接关闭.
固定资产的减少方式：抵债、转让、报废、捐赠、投资、盘亏，在页面上没有区别
无形资产的减少方式：转让  带收款方式，资产名，原值，累计摊销，净值，金额，税率，税额
                 报废             资产名，原值，累计摊销，净值
                 捐赠             资产名，原值，累计摊销，净值
                 投资  带收款方式，资产名，原值，累计摊销，净值
                 抵债  带收款方式，资产名，原值，累计摊销，净值
                 所以，投资与抵债相同，报废与捐赠相同。转让
"""

import unittest
from time import *
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException,TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import random
from test_case.pagebase import Page
from selenium.webdriver.common.action_chains import ActionChains


class ZcJs(unittest.TestCase):
    """资产减少"""
    global dr,js
    def setUp(self):
        global dr,js
        js=Page()
        dr=js.driver()
        js.loginout("17700000001","Abc123456")   # 登录
        sleep(3)
        # 进入控制台，搜索企业
        try:
            dr.find_element_by_xpath("//a[@href='/index']").click()
            print("进入控制台")
        except NoSuchElementException as e:
            print("登录跳转页面非首页")
        # 控制台搜索企业
        js.kongzhitai("cyb0808企业")
        sleep(3)
        # 进入单据添加
        dr.find_element_by_xpath("//*[@id='menu_list']/li/a").click()  # 进入单据页面
        print("进入单据模块")
        sleep(3)
        dr.find_element_by_xpath("//*[@id='list_view']/div/div[1]/div/div[2]/fieldset/div[1]/div/button[1]").click()  # 点击添加
        print("进入单据添加页面")
        # 切换单据类型为资产减少
        sleep(5)
        dr.find_element_by_xpath("//*[@id='detail_view']/div/div/div[1]/div/div[1]/div[1]/div[1]/span").click()
        billtype = dr.find_element_by_xpath("//*[@id='detail_view']/div/div/div[1]/div/div[1]/div[1]/div[1]/select")
        ActionChains(dr).move_to_element(billtype)
        sleep(2)
        dr.find_elements_by_xpath("html/body/span/span/span[2]/ul/li[8]/ul/li")[1].click()  # 点击资产减少
        sleep(3)

    def zcjs(self,y,m):
        """

        :param y: 资产类型，1是固定，2是无形
        :param m: 提示信息。0是第一个提示，1是第二个提示
        :return:
        """
        global dr,js
        sleep(3)
        dr.find_element_by_xpath("//*[@id='asset_type_select']").click()   # 点击资产类型
        zctype=dr.find_element_by_xpath("//*[@id='asset_type_select']")
        sleep(3)
        Select(zctype).select_by_value(str(y))  # value为1固定资产，value为2无形资产
        sleep(3)
        dr.find_element_by_xpath("//*[@id='asset_remove_method']").click()
        jsfs=dr.find_element_by_xpath("//*[@id='asset_remove_method']")
        jsfslist=[3,2,4,5,7]
        i=random.choice(jsfslist)  # value=3转让，2报废，4捐赠，5投资，7抵债
        Select(jsfs).select_by_value(str(i))
        # 先设置共同字段
        # 设置资产名
        sleep(5)
        dr.find_element_by_xpath("//*[@id='template15_table']/tbody/tr/td[2]/div[1]").click()  # 点击资产名，使列表可见
        sleep(3)
        # 获取列表个数，为0时不能继续操作
        zclist=dr.find_elements_by_xpath("//*[@id='template15_table']/tbody/tr/td[2]/div[2]/div/span/div/div/div")
        zccount=len(zclist)
        print(zccount)
        if zccount==0 or zccount==1:
            self.assertEqual(1,0,msg="资产数量可能不够，请先添加再操作")
            print("没有资产或资产不够，请添加后操作")
        elif zccount>1:   # 资产个数大于1，任意随机点击一个资产
            z=random.randint(0,zccount-1)   # 生成一个在个数范围内的随机整数
            zclist[z].click()      # 点击
            sleep(3)
        # 原值和净值自动获取，不用填写，设置累计折旧
        dr.find_element_by_xpath("//*[@id='template15_table']/tbody/tr/td[4]/div[1]").click()
        dr.find_element_by_xpath("//*[@id='template15_table']/tbody/tr/td[4]/div[2]/div/input").send_keys(str(random.uniform(0,999)))
        sleep(3)
        # 设置备注
        dr.find_element_by_xpath("//*[@id='bill_comment']").send_keys("aaa测试单据22")
        # 下面开始设置不通用的字段。
        # 当为无形资产时，当i=3为转让时，设置付款方式为现金.需要多填字段，金额，税率，税额
        if y==2 and i==3:
            js.paymethod()
            # 金额填写
            dr.find_element_by_xpath("//*[@id='template15_table']/tbody/tr/td[6]/div[1]").click()
            dr.find_element_by_xpath("//*[@id='template15_table']/tbody/tr/td[6]/div[2]/div/input").send_keys(str(random.uniform(1,99999)))
            sleep(3)
            # 税率填写
            dr.find_element_by_xpath("//*[@id='template15_table']/tbody/tr/td[7]/div[1]").click()
            dr.find_element_by_xpath("//*[@id='template15_table']/tbody/tr/td[7]/div[2]/div/input").send_keys("0.05")
            sleep(3)
            # 税额自动计算，不处理
        elif y==2 and (i==5 or i==7):
            dr.find_element_by_xpath("//*[@id='select2-pay_method-container']").click()   # 点击收款方式，使得列表可见
            sleep(3)
            skfslist=dr.find_elements_by_xpath("//*[@id='select2-pay_method-results']/li")   # 获取列表
            sffscount=len(skfslist)
            if sffscount==1:   # 只有一个时，一般是多类支付
                dr.find_element_by_xpath("//*[@id='add_aux']/img").click()  # 点击添加
                sleep(3)
                dr.find_element_by_xpath("//*[@id='name']").send_keys("测试111")
                sleep(2)
                dr.find_element_by_xpath("//*[@type='button' and @class='btn bluetbn-btn confirmBtn']").click()  # 点击关闭
                sleep(5)
                dr.find_element_by_xpath("//*[@id='select2-pay_method-container']").click()
            n=random.randint(0,len(dr.find_elements_by_xpath("//*[@id='select2-pay_method-results']/li"))-1)
            print(n)
            skfslist[n].click()
        # 预览
        # 预览凭证
        dr.find_element_by_xpath("//a[@role='button' and @class='lightblue-btn previewVoucher']").click()
        sleep(3)
        dr.find_element_by_xpath("//button[@type='button' and @class='bootbox-close-button close']").click()
        print("预览凭证成功")
        sleep(3)
        # 提交单据
        dr.find_element_by_xpath("//a[@role='button' and @class='bluetbn-btn save' and @data-status='2']").click()
        try:
            WebDriverWait(dr, 10, 0.1).until(EC.presence_of_element_located((By.ID, "notify_" + str(m) + "")))
        except TimeoutException as e:
            print("单据提交失败")
            dr.get_screenshot_as_file("E:\\script\\report\\资产减少单据提交失败.jpg")
            self.assertEqual(0, 1, msg="单据提交失败")
        sleep(5)
    def jsbill(self):
        jsjs=ZcJs()
        jsjs.zcjs(1,0)
        jsjs.zcjs(2,1)
    def tearDown(self):
        dr.quit()

if __name__ == '__main__':
    unittest.main()
