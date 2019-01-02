"""
商品管理模块
create by yb.c 2017-11-01
"""

import unittest
from selenium.common.exceptions import NoSuchElementException,TimeoutException
from test_case.pagebase import Page
from time import *
import time
from selenium.webdriver.support import  expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

class SPadd(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global dr,sp,i,spxz,xzsl
        sp=Page()
        dr=sp.driver()
        # 登录系统
        sp.loginout("17700000001","Abc123456")
        # 进入控制台
        try:
            dr.find_element_by_xpath("//a[@href='/index']").click()
        except NoSuchElementException as e:
            print("登录跳转到了控制台")
        print("进入控制台")
        # 搜索企业
        sp.kongzhitai("cyb0808企业")
        sleep(3)
    def SPaddnormal(self):
        """
        常规添加商品。正常输入名称，规格等
        变量解释：
        jldwbtn:计量单位按钮
        addbtn:商品添加按钮
        edit:编辑
        delete:删除
        alldelete:全选后删除
        i:添加计量单位，循环添加整数和非整数，循环变量
        :return:
        """
        global i,n,addbtn
        # 进入设置页面
        dr.find_element_by_xpath("//*[@id='menu_list']/li[10]/a").click()
        sleep(2)
        # 进入商品管理
        dr.find_element_by_xpath("//*[@id='leftSider']/div/ul[1]/li[3]/a").click()
        sleep(4)
        # 定位
        jldwbtn=dr.find_element_by_xpath("//*[@id='commodityUtil']")  # 计量单位按钮
        addbtn=dr.find_element_by_xpath("//*[@id='newBtn']")    # 添加按钮
        edit=dr.find_element_by_xpath("//*[@id='commodityTable']/tbody/tr[1]/td[8]/span[1]/a")   # 操作中的编辑按钮
        delete=dr.find_element_by_xpath("//*[@id='commodityTable']/tbody/tr[1]/td[8]/span[2]/a")  # 操纵中的删除
        alldelete=dr.find_element_by_xpath("//*[@id='removeBatch']")   # 多选删除按钮

        now=time.strftime("%d%H%M%S")
        # Action
        # add添加计量单位
        # 点击计量单位，弹出对话框，添加一个整数单位
        jldwbtn.click() # 点击计量单位按钮，弹出计量单位对话框
        sleep(2)
        jldwaddbtn = dr.find_element_by_xpath("//*[@id='addBtn']")  # 计量单位对话框中的添加按钮
        sleep(2)
        i=1
        while i<3:
            jldwaddbtn.click()    # 点击添加按钮
            sleep(2)
            if i==1:
                jldw="整数单位"+now
            else:
                jldw="非整单位"+now
                dr.find_element_by_xpath("//*[@id='isInteger2']").click()  # 是否整数，勾选否。
                sleep(2)
            dr.find_element_by_xpath("//*[@id='name']").send_keys(jldw)  # 写入单位名称
            sleep(2)
            dr.find_element_by_xpath("//*[@type='button' and @class='btn bluetbn-btn dir']").click()   # 提交
            i = i + 1
            sleep(3)
            # 验证是否提交成功
        """  
            try:
                WebDriverWait(dr, 5, 0.1).until(EC.presence_of_element_located((By.ID, "notify_"+str(n)+"")))
            except TimeoutException as e:
                print("计提单位添加失败")
                dr.get_screenshot_as_file("E:\\script\\report\\计提单位添加失败.jpg")
                self.assertEqual(0, 1, msg="计提单位添加失败")
                sleep(3)
        """

        # 关闭计量单位对话框
        dr.find_element_by_xpath("//*[@type='button' and @class='btn bluetbn-btn']").click()
        sleep(3)
        # 添加商品
        #   点击添加按钮
        addbtn.click()
        sleep(2)
        #  输入商品名
        dr.find_element_by_xpath("//*[@id='name']").send_keys(str("商品"+now))
        sleep(2)
        # 写入规格
        dr.find_element_by_xpath("//*[@id='spec']").send_keys("规格"+now)
        # 因为已经添加过计量单位，所以计量单位肯定有值。且单位，性质，税率都默认填充了数据。直接提交即可
        sleep(2)
        dr.find_element_by_xpath("//*[@type='button' and @class='btn bluetbn-btn']").click()
        # 如果，名称+规格相同会出现重复数据，会弹出框，验证是否有弹框，有就关闭
        try:
            dr.find_element_by_xpath("//div[@class='layui-layer-btn layui-layer-btn-c']/a").click()
            # 提示重复之后，是不能提交商品的，取消添加商品
            dr.find_element_by_xpath("//*[@type='button' and @class='btn whitegray-btn']").click()
        except NoSuchElementException as e:
            print("没有重复")
        # 验证是否提交成功
        """
        try:
            WebDriverWait(dr, 5, 0.1).until(EC.presence_of_element_located((By.ID, "notify_" + str(n) + "")))
        except TimeoutException as e:
            print("商品添加失败")
            dr.get_screenshot_as_file("E:\\script\\report\\商品添加失败.jpg")
            self.assertEqual(0, 1, msg="商品添加失败")
        """

    def SPaddwhile(self):
        """
        根据性质和税率，循环添加商品
        变量解释：
        spxz:添加页面，商品性质
        spxzlist:商品性质列表
        spxzcount:商品性质数目
        xzsl:性质税率
        k：根据性质数量，循环添加商品循环变量
        m：根据税率变量，循环添加商品循环变量
        :return:
        """
        # 根据性质和税率循环，k是性质循环，m是税率循环
        sleep(3)
        global addbtn,k,m,spxz,xzsl
        k=0
        m=0
        dr.find_element_by_xpath("//*[@id='newBtn']").click()
        sleep(2)
        spxz = dr.find_element_by_xpath("//*[@id='property']")
        sleep(2)
        spxzlist = dr.find_elements_by_xpath("//*[@id='property']/option")  # 商品性质列表
        sleep(2)
        spxzcount = len(spxzlist)  # 商品性质个数
        sleep(2)
        # 点击添加，是为了获取元素，获取k和m的数量。关闭添加对话框，执行循环添加操作
        dr.find_element_by_xpath("//*[@type='button' and @class='btn whitegray-btn']").click()
        sleep(2)
        while k<spxzcount:
            addbtn.click()  # 点击添加
            now2=time.strftime("%d%H%M%S")
            dr.find_element_by_xpath("//*[@id='name']").send_keys(str("商品"+now2))  # 写入单位名称
            sleep(2)
            # 写入规格
            dr.find_element_by_xpath("//*[@id='spec']").send_keys(str("规格"+now2))
            sleep(3)
            # 选择性质
            # 选择税率
            spxz = dr.find_element_by_xpath("//*[@id='property']")
            Select(spxz).select_by_index(k)
            sleep(2)
            xzsl = dr.find_element_by_xpath("//*[@id='rate']")
            xzsl = dr.find_element_by_xpath("//*[@id='rate']")
            xzslcount= len(dr.find_elements_by_xpath("//*[@id='rate']/option"))
            if m<xzslcount:
                Select(xzsl).select_by_index(m)
                # 提交商品
                sleep(2)
                dr.find_element_by_xpath("//*[@type='button' and @class='btn bluetbn-btn']").click()
            m=m+1
            if m==xzslcount:
                k=k+1
                m=0
            sleep(3)
    @classmethod
    def tearDownClass(cls):
        print("ksg")
if __name__ == '__main__':
    unittest.main()
