"""支付税费"""
import unittest
from time import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from test_case.pagebase import Page
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

import random

class ZfSf(unittest.TestCase):
    """支付税费录单"""
    global dr,sf
    def setUp(self):
        global dr,sf
        sf=Page()
        dr=sf.driver()   # 从基础页面，获得dr
        sf.loginout("17700000001","Abc123456")  # 登录系统
        sleep(5)
        # 进入控制台，搜索企业
        try:
            dr.find_element_by_xpath("//a[@href='/index']").click()
            print("进入控制台")
        except NoSuchElementException as e:
            print("登录跳转页面非首页")
        # 控制台搜索企业
        sf.kongzhitai("cyb0808企业")
        sleep(3)
        # 进入单据添加
        dr.find_element_by_xpath("//*[@id='menu_list']/li/a").click()  # 进入单据页面
        print("进入单据模块")
        sleep(3)
        dr.find_element_by_xpath("//*[@id='list_view']/div/div[1]/div/div[2]/fieldset/div[1]/div/button[1]").click()  # 点击添加
        print("进入单据添加页面")
        sleep(3)

    def zfsfadd(self):
        global dr,sf
        # 切换单据类型为支付税费
        billtype = dr.find_element_by_xpath("//*[@id='detail_view']/div/div/div[1]/div/div[1]/div[1]/div[1]/select")
        dr.find_element_by_xpath("//*[@id='detail_view']/div/div/div/div/div/div/div/span/span/span").click()
        ActionChains(dr).move_to_element(billtype)
        sleep(2)
        dr.find_elements_by_xpath("html/body/span/span/span[2]/ul/li[7]/ul/li")[1].click()  # 点击计提工资
        sleep(3)
        # 设置付款方式
        sf.paymethod()
        # 随机设置税种
        dr.find_element_by_xpath("//*[@id='template13_table']/tbody/tr/td[2]/div[1]").click()  # 点击税种，使得元素可见
        szvaluelist=['01','03','04','05','06','07','08','09',10,11,12,13,14,15,16,17,18,98,99]
        sz=dr.find_element_by_xpath("//*[@id='template13_table']/tbody/tr/td[2]/div[2]/div/select")
        a=random.choice(szvaluelist)
        Select(sz).select_by_value(str(a))
        sleep(2)
        # 设置品目
        if a!='01':    # 税种不是增值税，需要设置品目
            pm=dr.find_element_by_xpath("//*[@id='template13_table']/tbody/tr/td[3]/div[2]/div/select")
            pmlist=dr.find_elements_by_xpath("//*[@id='template13_table']/tbody/tr/td[3]/div[2]/div/select")
            Select(pm).select_by_index(str(random.randint(0,len(pmlist)-1)))
        # 设置金额
        dr.find_element_by_xpath("//*[@id='template13_table']/tbody/tr/td[4]/div[1]").click()   # 点击使得金额输入元素可见
        dr.find_element_by_xpath("//*[@id='template13_table']/tbody/tr/td[4]/div[2]/div/input").send_keys(str(random.uniform(1,999999999)))
        sleep(2)
        # 预览凭证
        dr.find_element_by_xpath("//a[@role='button' and @class='lightblue-btn previewVoucher']").click()
        sleep(3)
        dr.find_element_by_xpath("//button[@type='button' and @class='bootbox-close-button close']").click()
        print("预览凭证成功")
        sleep(2)
        # 提交单据
        dr.find_element_by_xpath("//a[@role='button' and @class='bluetbn-btn save' and @data-status='2']").click()
        try:
            WebDriverWait(dr, 10, 0.1).until(EC.presence_of_element_located((By.ID, "notify_0")))
        except TimeoutException as e:
            print("单据提交失败")
            dr.get_screenshot_as_file("E:\\script\\report\\支付税费单据提交失败.jpg")
            self.assertEqual(0, 1, msg="单据提交失败")
        sleep(5)
    def tearDown(self):
        dr.quit()
if __name__ == '__main__':
    unittest.main()
