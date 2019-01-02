"""
代客下单功能脚本，只提交订单，不进行支付
"""
import unittest
from test_case.pagebase import Page
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from time import *
import random
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
import re

class Daike(unittest.TestCase):
    """代客下单"""
    global dr,fwlxcount
    def setUp(self):
        global dr
        dk=Page()
        dr=dk.driver()
        dk.loginout("17700000001","Abc123456")   # 登录系统
        # 进入控制台。搜索企业
        try:
            dr.find_element_by_xpath("//a[@href='/index']").click()
        except NoSuchElementException as e:
            print("登录跳转到了控制台")
        print("进入控制台")
        # 进入控制台后，默认在服务企业页面，点击订单
        dr.find_element_by_xpath("//*[@id='menu_list']/li[2]/a").click()
    def dkxd(self):
        """
        57个服务类型，循环添加。服务总价、订单备注是共有字段。
        公司注册有客户账号
        其他服务是企业全称
        有服务类型的，选择服务类型。没有的不操作
        i是57个服务的循环变量，y是服务类型的循环变量。可选项都是select，按index循环，都是从0开始。
        :return:
        """
        global dr,fwlxcount,datay,datam
        i=0
        y=-1
        n=-1    # 提示信息个数
        while i<=56:
            sleep(3)
            y=y+1
            n=n+1
            dr.find_element_by_xpath("//*[@id='agentOrderBtn']").click()
            sleep(2)
            dr.find_element_by_xpath("//*[@id='select2-service-container']").click()  # 点击服务项目元素，使得列表可见
            fwxmlist=dr.find_elements_by_xpath("//*[@id='select2-service-results']/li")
            fwxmlist[i].click()  # 选择服务项目
            # 先填写共同项目，服务总价与订单备注
            dr.find_element_by_xpath("//*[@id='orderPrice']").send_keys(str(random.randint(1,999))) # 写入服务总价
            sleep(3)
            dr.find_element_by_xpath("//*[@id='agencyOrderForm']/fieldset/div[11]/div/textarea").send_keys("@#EEdi订单")  # 写入备注
            # 选服务类型，如果有服务类型的话
            try:
                fwlx=dr.find_element_by_xpath("//*[@id='serviceItem']")
                fwlx.click()  # 点击服务类型，使得列表可见
                fwlxlist=dr.find_elements_by_xpath("//*[@id='serviceItem']/option")   # 获取服务类型列表
                fwlxcount=len(fwlxlist)-1   # 获取服务类型数量
                sleep(2)
                if y<=fwlxcount:
                    sleep(2)
                    Select(fwlx).select_by_index(y)
            except Exception as e:
                fwlxcount=0
                print("没有服务类型")
            # 当服务项目是公司注册时，填写手机号，其他服务都是添加企业名
            if i==0:
                dr.find_element_by_xpath("//*[@id='userNameSuggestion']").send_keys("17700000066")
                sleep(2)
                dr.find_element_by_xpath("//*[@id='agencyOrderForm']/fieldset/div[9]/div/span/div/div/div").click()
            else:
                dr.find_element_by_xpath("//*[@id='enterpriseNameSuggestion']").send_keys("ccc1030企业")
                sleep(2)
                dr.find_element_by_xpath("//*[@id='agencyOrderForm']/fieldset/div[8]/div/span/div/div/div/strong").click()
            # 提交订单
            dr.find_element_by_xpath("//*[@id='submitOrder']").click()
            sleep(1)
            # 如果是财税托管服务，可能购买的类型跟之前不同会弹出框。判断弹出框，点确定
            try:
                dr.find_element_by_xpath("//*[@class='bluetbn-btn margin-right btn-ok' and @type='button']").click()
                sleep(1)
            except Exception as e:
                print("代客下单，项目%r"%i)
            # 也有可能是购买区间重复
            try:
                dr.find_element_by_xpath("//div[@class='layui-layer-btn layui-layer-btn-c']/a").click()
                sleep(1)
                # 如果提示购买区间重复，获取提示中的区间值，修改时间，再次提交
                # 上面点击确定是为了验证是否有该对话框。有的话，需要获取框上的文字，需要再次提交订单，弹出对话框
                # 提交
                dr.find_element_by_xpath("//*[@id='submitOrder']").click()
                # 如果有弹出购买类型不一致，点确定
                sleep(3)
                try:
                    dr.find_element_by_xpath("//*[@class='bootbox modal fade in' and @role='dialog']/div/div/div[3]/button[1]").click()
                    sleep(1)
                except Exception as e:
                    print("代客下单，项目%r"%i,33333)
                #dr.find_element_by_xpath("//*[@id='layui-layer1']").isDislayed
                sleep(1)
                chongfu=dr.find_element_by_xpath("//div[@class='layui-layer-content']").text
                print(chongfu)
                cflist=chongfu.split(',')  # 分割
                datalist=cflist[1]
                datay=datalist[3:7]
                datam=str(datalist[9:10]+"月")  # 取出年月
                print(datay,datam)
                # 关闭提示框
                dr.find_element_by_xpath("//div[@class='layui-layer-btn layui-layer-btn-c']/a").click()
                sleep(1)
                # 根据提示的年月，设置日期
                # 点击服务期限，弹出对话框
                dr.find_element_by_xpath("//*[@id='startDate']").click()
                sleep(2)
                # 点击年份，展示区间
                #dr.find_element_by_xpath("//div[@class='datetimepicker-months']/table/thead/tr/th[2]").click()
                dr.find_element_by_xpath("/html/body/div[6]/div[4]/table/thead/tr/th[2]").click()
                sleep(1)
                # 获取年份
                #yearlist=dr.find_elements_by_xpath("//div[@class='datetimepicker-years']/table/tbody/tr/td/span")
                yearlist=dr.find_elements_by_xpath("/html/body/div[6]/div[5]/table/tbody/tr/td/span")
                # 点击年份
                year=0
                while year <11:
                    ytext=yearlist[year].text
                    if ytext==datay:
                        yearlist[year].click()
                        break
                    else:
                        year=year+1
                sleep(2)
                # 点击年份之后显示月份页面，获取月份列表
                #monlist=dr.find_elements_by_xpath("//div[@class='datetimepicker-months']/table/tbody/tr/td/span")
                monlist=dr.find_elements_by_xpath("/html/body/div[6]/div[4]/table/tbody/tr/td/span")
                # 点击月份
                mon=0
                while mon<11:
                    montext=monlist[mon].text
                    if montext==datam:
                        monlist[mon].click()
                        break
                    else:
                        mon=mon+1
                sleep(1)
                # 选择年月之后，点击提交
                dr.find_element_by_xpath("//*[@id='submitOrder']").click()
                sleep(1)
                try:
                    dr.find_element_by_xpath("/html/body/div[13]/div/div/div[3]/button[1]").click()
                except NoSuchElementException as e:
                    print("wuuw")
            except NoSuchElementException as e:
                print("购买区间没有重复")
            # 判断是否提交成功
            try:
                WebDriverWait(dr, 10, 0.1).until(EC.presence_of_element_located((By.ID, "notify_" + str(n) + "")))
            except TimeoutException as e:
                print("代客下单提交失败")
                dr.get_screenshot_as_file("E:\\script\\report\\代客下单提交失败.jpg")
                self.assertEqual(0, 1, msg="代客下单提交失败")
            try:
                if y==fwlxcount:
                    y=-1
                    i=i+1
            except NameError:
                i=i+1
    def tearDown(self):
        print("gogogo")

if __name__ == '__main__':
    unittest.main()
