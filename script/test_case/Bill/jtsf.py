"""计提税费单据录制"""
import unittest
from time import *
from test_case.pagebase import Page
from selenium.common.exceptions import NoSuchElementException,TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from random import choice
import random
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class JtSf(unittest.TestCase):
    """录制计提税费单据"""
    global dr
    def setUp(self):
        global dr,jtsf
        jtsf=Page()
        dr=jtsf.driver()
        jtsf.loginout("17700000001","Abc123456")    # 登录
        sleep(5)
        # 进入控制台，搜索企业
        try:
            dr.find_element_by_xpath("//a[@href='/index']").click()
            print("进入控制台")
        except NoSuchElementException as e:
            print("登录跳转页面非首页")
        # 控制台搜索企业
        jtsf.kongzhitai("cyb0808企业")
        sleep(3)
        # 进入单据添加
        dr.find_element_by_xpath("//*[@id='menu_list']/li/a").click()  # 进入单据页面
        print("进入单据模块")
        sleep(3)
        dr.find_element_by_xpath("//*[@id='list_view']/div/div[1]/div/div[2]/fieldset/div[1]/div/button[1]").click()  # 点击添加
        print("进入单据添加页面")
        sleep(3)
    def jtsfadd(self):
        global dr
        # 切换单据类型为计提税费
        # 切换单据类型
        billtype = dr.find_element_by_xpath("//*[@id='detail_view']/div/div/div[1]/div/div[1]/div[1]/div[1]/select")
        dr.find_element_by_xpath("//*[@id='detail_view']/div/div/div/div/div/div/div/span/span/span").click()
        ActionChains(dr).move_to_element(billtype)
        sleep(2)
        dr.find_elements_by_xpath("html/body/span/span/span[2]/ul/li[7]/ul/li")[0].click() # 点击计提工资
        sleep(3)
        # 选择税种，如果选择增值税，提交时要给出提醒，增值税不能单独计提
        sz=dr.find_element_by_xpath("//*[@id='template12_table']/tbody/tr/td[2]/div[1]")  # 点击税种，使得列表可见
        sz.click()
        sleep(2)
        szsz=dr.find_element_by_xpath("//*[@id='template12_table']/tbody/tr/td[2]/div[2]/div/select")
        szlist=dr.find_elements_by_xpath("//*[@id='template12_table']/tbody/tr/td[2]/div[2]/div/select")
        valuelist=['01','03','04','05','06','07','08','09',10,11,12,13,14,15,16,17,18]
        a=random.choice(valuelist)
        print(a)
        Select(szsz).select_by_value(str(a))
        sleep(5)
        if a!='01':
            # 税种不是增值税，要设置品目，获取品目列表。默认选择了税种，品目自动选中第一个
            # 获取品目列表
            pmlist=dr.find_elements_by_xpath("//*[@id='template12_table']/tbody/tr/td[3]/div[2]/div/select")
            pm=dr.find_element_by_xpath("//*[@id='template12_table']/tbody/tr/td[3]/div[2]/div/select")
            pmcount=len(pmlist)  # 获取品目的个数，因为不同税种，品目个数不一样
            if pmcount>0:
                Select(pm).select_by_index(random.randint(0,pmcount-1))
        # 设置金额
        dr.find_element_by_xpath("//*[@id='template12_table']/tbody/tr/td[4]/div[1]").click()
        dr.find_element_by_xpath("//*[@id='template12_table']/tbody/tr/td[4]/div[2]/div/input").send_keys(str(random.uniform(1,999999999)))
        sleep(3)
        # 判断所选的税种，如果是增值税，预览单据和提交单据时需要弹框提示，增值税不能单独计提
        if a=='01':
            dr.find_element_by_xpath("//a[@role='button' and @class='lightblue-btn previewVoucher']").click()  # 点击预览凭证
            sleep(3)
            text=dr.find_element_by_xpath("//div[@class='layui-layer-content']").text
            sleep(3)
            dr.find_element_by_xpath("//div[@class='layui-layer-btn layui-layer-btn-c']/a").click()  # 关闭对话框
            sleep(3)
            dr.find_element_by_xpath("//a[@role='button' and @class='bluetbn-btn save' and @data-status='2']").click()  # 点击提交
            sleep(2)
            dr.find_element_by_xpath("//div[@class='layui-layer-btn layui-layer-btn-c']/a").click()
            print(text)
        else:
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
                dr.get_screenshot_as_file("E:\\script\\report\\计提税费单据提交失败.jpg")
                self.assertEqual(0, 1, msg="单据提交失败")
            sleep(5)


    def tearDown(self):

        dr.quit()
if __name__ == '__main__':
    unittest.main()
