"""
辅助核算功能，财税师角色
账户、客户、供应商、其他往来、股东添加应该是一样的，一起写，调用即可
职员单独写
create by yb.c 2017-11-02
"""
import unittest
from time import *
from test_case.pagebase import Page
from selenium.common.exceptions import NoSuchElementException,TimeoutException
import time

class Fzhsadd(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global dr,fzhs
        fzhs=Page()
        dr=fzhs.driver()
        sleep(2)
        # 登录
        fzhs.loginout("17700000001","Abc123456")
        # 进入控制台
        try:
            dr.find_element_by_xpath("//a[@href='/index']").click()
        except NoSuchElementException as e:
            print("登录跳转到了控制台")
        print("进入控制台")
        # 搜索企业
        fzhs.kongzhitai("cyb0808企业")
        sleep(3)
        # 点击设置
        dr.find_element_by_xpath("//*[@id='menu_list']/li[10]/a").click()
        sleep(2)
        # 点击辅助核算
        dr.find_element_by_xpath("//*[@id='leftSider']/div/ul[1]/li[4]/a").click()
        sleep(2)
    def zkgqgadd(self):
        # 点击添加按钮。默认是账户，然后是客户，供应商，其他往来，股东
        i=2
        while i<8:
            dr.find_element_by_xpath("//*[@id='addAuxiliaryValueBtn']").click()
            sleep(2)
            # 写入名称
            now=time.strftime("%d%H%M%S")
            if i==7:   # 职员页面名称元素不一样，其他页面是一样的
                dr.find_element_by_xpath("//*[@id='name']").send_keys("职员"+now)
            else:
                dr.find_element_by_xpath("//*[@id='name']").send_keys("辅助核算"+now)
            # 提交
            dr.find_element_by_xpath("//div[@class='layui-layer-btn layui-layer-btn-c']/a").click()
            sleep(2)
            # 切换到其他类型
            if i<7:
                dr.find_element_by_xpath("//*[@id='auxiliaryCategoryTable']/li["+str(i)+"]/a").click()
            # 2是客户，3是供应商，4是其他往来，5是股东
            i=i+1
            sleep(3)
    @classmethod
    def tearDownClass(cls):
        print(56)

if __name__ == '__main__':
    unittest.main()
