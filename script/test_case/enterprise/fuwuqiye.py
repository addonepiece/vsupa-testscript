"""
财税师服务企业，添加服务企业。添加新客户。已有客户的验证较多，暂时不考虑
思路：
选择服务项目（6个），选择服务类型。只有财税托管有托管时间，默认。客户类型为新客户，默认
当项目不是工商注册时，需要设置企业名。
填写账号，填写办公地址
完成
"""

import unittest
from test_case.pagebase import Page
from selenium.common.exceptions import NoSuchElementException,TimeoutException
from time import *
from selenium.webdriver.support.select import Select
import time

class Enterprise(unittest.TestCase):
    """添加服务企业"""
    global dr
    def setUp(self):
        global dr
        ent=Page()
        dr=ent.driver()
        ent.loginout("17700000001","Abc123456")  # 登录系统
        # 进入控制台
        try:
            dr.find_element_by_xpath("//a[@href='/index']").click()
            print("进入控制台")
        except NoSuchElementException as e:
            print("登录跳转页面非首页")
        dr.implicitly_wait(5)
        # 进入控制台，即展示“服务企业”列表
    def AddEnterprise(self):
        global dr
        i = 1
        y = -1
        sleep(3)
        # 获取企业个数
        entcount=dr.find_element_by_xpath("//*[@id='servicetab11']/div/div[3]/div[2]/div[4]/div/span[1]").text
        print("服务企业有：%r"%entcount)
        sleep(3)
        # 获取一共有几页
        entpagelist=dr.find_elements_by_xpath("//*[@id='servicetab11']/div/div[3]/div[2]/div[4]/div/ul/li")
        entpagecount=len(entpagelist)   # 因为翻页操作中，有一个前一页，一个后一页，总元素个数减去2，就是页数
        print("服务企业数据有: %r 页"%(entpagecount-2))
        sleep(3)
        # 添加服务企业
        # 点击添加按钮
        # 循环的话在这里加
        while i<=6:   # 目前有6项目
            y=y+1
            try:
                dr.find_element_by_xpath("//*[@id='add_service']").click()
            except NoSuchElementException as e:
                print("服务企业添加失败")
                dr.get_screenshot_as_file("E:\\script\\report\\服务企业添加失败.jpg")
                self.assertEqual(0, 1, msg="服务企业添加失败")
            dr.implicitly_wait(3)
            sleep(2)
            # 判断是否跳转成功
            try:
                dr.find_element_by_xpath("//*[@id='back_serviceEnt']")
            except NoSuchElementException as e:
                print("没有进入服务企业添加页面")
                dr.get_screenshot_as_file("E:\\script\\report\\服务企业添加页面加载失败.jpg")
                self.assertEqual(0,1,msg="服务企业添加页面加载失败")
            # 服务项目共有6个，财税托管，工商注册，财税自助，企业变更，企业注销，证照遗失补办。默认是财税托管
            sleep(5)
            fwxm=dr.find_element_by_xpath("//*[@id='selService']")
            Select(fwxm).select_by_value(str(i))
            sleep(3)
            # 选择服务类型
            fwlx=dr.find_element_by_xpath("//*[@id='selServiceType']")
            fwlxcount=len(dr.find_elements_by_xpath("//*[@id='selServiceType']/option"))-1
            now = time.strftime("%d%H%M%S")
            if y<=fwlxcount:
                Select(fwlx).select_by_index(str(y))
                if i!=2:    # 如果服务项目不是工商注册，填写企业全称，如果是公司注册，则不需要
                    # 为了名字的唯一性，命名方式为命名加时分秒
                    entname="ccc企业"+now
                    dr.find_element_by_xpath("//*[@id='enterpriseName1']").send_keys(str(entname))
                sleep(3)
                # 写入登录账号
                entlogin="ccc"+now
                dr.find_element_by_xpath("//*[@id='loginName']").send_keys(str(entlogin))
                sleep(3)
                # 选择办公地址，市区选择东莞市，匹配ssc
                city=dr.find_element_by_xpath("//*[@id='selectcity']/select[2]")
                Select(city).select_by_value("东莞市")
                sleep(2)
                # 填写详细地址
                dr.find_element_by_xpath("//*[@id='street']").send_keys("SES@#$@#$地址地址")
            # 确认完成
            dr.find_element_by_xpath("//*[@id='saveBtn']").click()
            sleep(3)
            # 提交后返回到服务企业列表页。如果没有返回则提交失败
            if y==fwlxcount:
                y=-1
                i=i+1
            dr.implicitly_wait(5)
    def tearDown(self):
        print("gogogo")

if __name__ == '__main__':
    unittest.main()
