"""
支付社保，支付公积金，页面一样，写在一起
"""
import unittest
from test_case.pagebase import Page
from time import *
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
class ZfSbGjj(unittest.TestCase):
    """录制支付社保，支付公积金"""
    global dr,zfzf
    def setUp(self):
        global dr,zfsg
        zfsg=Page()
        dr=zfsg.driver()
        zfsg.loginout("17700000001","Abc123456")
        # 进入控制台，搜索企业
        try:
            dr.find_element_by_xpath("//a[@href='/index']").click()
            print("进入控制台")
        except NoSuchElementException as e:
            print("登录跳转页面非首页")
        # 控制台搜索企业
        zfsg.kongzhitai("cyb0811企业")
        sleep(3)
        # 进入单据添加
        dr.find_element_by_xpath("//*[@id='menu_list']/li/a").click()  # 进入单据页面
        print("进入单据模块")
        sleep(3)
        dr.find_element_by_xpath("//*[@id='list_view']/div/div[1]/div/div[2]/fieldset/div[1]/div/button[1]").click()  # 点击添加
        print("进入单据添加页面")
        sleep(3)

    def zf(self,i,n): # i是切换单据类型时传得值，支付社保是4，支付公积金是5，n是页面元素,提示信息会变动。第一次提交是0，第二次提交是1，第三次提交是2
        global dr,zfsg
        # 切换单据类型
        billtype = dr.find_element_by_xpath("//*[@id='detail_view']/div/div/div[1]/div/div[1]/div[1]/div[1]/select")
        dr.find_element_by_xpath("//*[@id='detail_view']/div/div/div/div/div/div/div/span/span/span").click()
        ActionChains(dr).move_to_element(billtype)
        sleep(2)
        dr.find_elements_by_xpath("html/body/span/span/span[2]/ul/li[6]/ul/li")[i].click()
        sleep(3)
        # 输入公司承担
        dr.find_element_by_xpath("//*[@id='companyPay']").send_keys(str(random.uniform(1,500)))
        sleep(2)
        # 输入个人承担
        dr.find_element_by_xpath("//*[@id='personalPay']").send_keys(str(random.uniform(1, 500)))
        sleep(2)
        # 输入滞纳金
        dr.find_element_by_xpath("//*[@id='lateFee']").send_keys(str(random.uniform(1, 50)))
        sleep(2)
        # 付款方式选为现金
        zfsg.paymethod()
        sleep(3)
        # 预览凭证
        dr.find_element_by_xpath("//a[@role='button' and @class='lightblue-btn previewVoucher']").click()
        sleep(3)
        dr.find_element_by_xpath("//button[@type='button' and @class='bootbox-close-button close']").click()
        print("预览凭证成功")
        sleep(2)
        # 提交单据
        dr.find_element_by_xpath("//a[@role='button' and @class='bluetbn-btn save' and @data-status='2']").click()
        try:
            WebDriverWait(dr, 10, 0.1).until(EC.presence_of_element_located((By.ID, "notify_"+str(n)+"")))
        except TimeoutException as e:
            print("单据提交失败")
            dr.get_screenshot_as_file("E:\\script\\report\\单据提交失败.jpg")
            self.assertEqual(0, 1, msg="单据提交失败")
        sleep(5)
    def zfsbgjj(self):
        zff=ZfSbGjj()
        zff.zf(4,0)
        zff.zf(5,1)
    def tearDown(self):
        dr.quit()
if __name__ == '__main__':
    unittest.main()
