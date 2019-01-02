"""
计提公积金单据
"""
import unittest
from test_case.pagebase import Page
from time import *
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class JtGjj(unittest.TestCase):
    """录制计提公积金"""
    global dr,jtgjjg
    def setUp(self):
        global dr,jtgjjg
        jtgjjg=Page()
        dr=jtgjjg.driver()
        jtgjjg.loginout("17700000001","Abc123456")
    def jtgjjadd(self):
        global dr,jtgjjg
        # 进入控制台，搜索企业
        try:
            dr.find_element_by_xpath("//a[@href='/index']").click()
            print("进入控制台")
        except NoSuchElementException as e:
            print("登录跳转页面非首页")
        # 控制台搜索企业
        jtgjjg.kongzhitai("cyb0811企业")
        sleep(3)
        # 进入单据添加
        dr.find_element_by_xpath("//*[@id='menu_list']/li/a").click()  # 进入单据页面
        print("进入单据模块")
        sleep(3)
        dr.find_element_by_xpath("//*[@id='list_view']/div/div[1]/div/div[2]/fieldset/div[1]/div/button[1]").click()  # 点击添加
        print("进入单据添加页面")
        sleep(3)
        # 切换单据类型为计提工资
        billtype = dr.find_element_by_xpath("//*[@id='detail_view']/div/div/div[1]/div/div[1]/div[1]/div[1]/select")
        dr.find_element_by_xpath("//*[@id='detail_view']/div/div/div/div/div/div/div/span/span/span").click()
        ActionChains(dr).move_to_element(billtype)
        sleep(2)
        dr.find_elements_by_xpath("html/body/span/span/span[2]/ul/li[6]/ul/li")[2].click()
        sleep(3)
        # 随机选择部门
        dr.find_element_by_xpath("//*[@id='template8_table']/tbody/tr/td[2]/div[1]").click()  # 点击部门，使得列表元素可见
        bumen=dr.find_element_by_xpath("//*[@id='template8_table']/tbody/tr/td[2]/div[2]/div/select")
        Select(bumen).select_by_value(str(random.randint(1, 3)))
        sleep(2)
        print("随机选择部门")
        # 输入公司承担
        dr.find_element_by_xpath("//*[@id='template8_table']/tbody/tr/td[3]/div[1]").click()  # 点击公司承担
        dr.find_element_by_xpath("//*[@id='template8_table']/tbody/tr/td[3]/div[2]/div/input").send_keys(str(random.uniform(1,500)))
        sleep(2)
        # 输入个人承担
        dr.find_element_by_xpath("//*[@id='template8_table']/tbody/tr/td[4]/div[1]").click()  # 点击个人承担
        dr.find_element_by_xpath("//*[@id='template8_table']/tbody/tr/td[4]/div[2]/div/input").send_keys(str(random.uniform(1, 500)))
        sleep(2)
        # 预览凭证，提交单据
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
            dr.get_screenshot_as_file("E:\\script\\report\\计提公积金单据提交失败.jpg")
            self.assertEqual(0, 1, msg="单据提交失败")
        sleep(5)
    def tearDown(self):
        dr.quit()
if __name__ == '__main__':
    unittest.main()
