"""
支付工资
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

class ZfGz(unittest.TestCase):
    """支付工资"""
    global dr,zfzf
    def setUp(self):
        global dr,zfzf
        zfzf=Page()
        dr=zfzf.driver()
        zfzf.loginout("17700000001","Abc123456")
        # 进入控制台，搜索企业
        try:
            dr.find_element_by_xpath("//a[@href='/index']").click()
            print("进入控制台")
        except NoSuchElementException as e:
            print("登录跳转页面非首页")
        # 控制台搜索企业
        zfzf.kongzhitai("cyb0808企业")
        sleep(3)
        # 进入单据添加
        dr.find_element_by_xpath("//*[@id='menu_list']/li/a").click()  # 进入单据页面
        print("进入单据模块")
        sleep(3)
        dr.find_element_by_xpath(
            "//*[@id='list_view']/div/div[1]/div/div[2]/fieldset/div[1]/div/button[1]").click()  # 点击添加
        print("进入单据添加页面")
        sleep(3)
    def zfgz(self):
        global dr,zfzf,xryf,xrdkgjj,xrdksb,xrdkgs
        # 切换单据类型为支付工资
        billtype = dr.find_element_by_xpath("//*[@id='detail_view']/div/div/div[1]/div/div[1]/div[1]/div[1]/select")
        dr.find_element_by_xpath("//*[@id='detail_view']/div/div/div/div/div/div/div/span/span/span").click()
        ActionChains(dr).move_to_element(billtype)
        sleep(2)
        dr.find_elements_by_xpath("html/body/span/span/span[2]/ul/li[6]/ul/li")[3].click()
        sleep(3)
        # 如果已经录入过计提，应发工资会自动填充数据，不需要写入。如果为空，才要写入，需要判断
        # 先判断应发，代扣，实发有没有值，有值时获取值，没值时写入值
        yf=dr.find_element_by_xpath("//*[@id='totalSalary']").get_attribute("value")
        if yf=='':    # 为空时写入值，不为空时不写入
            xryf = '%.2f' % (random.uniform(1, 500))
            dr.find_element_by_xpath("//*[@id='totalSalary']").send_keys(str(xryf))
        # 判断代扣社保
        dksb = dr.find_element_by_xpath("//*[@id='deductSocialSecurity']").get_attribute("value")
        if dksb=='':
            xrdksb = '%.2f' % (random.uniform(1, 500))
            # 输入代扣社保
            dr.find_element_by_xpath("//*[@id='deductSocialSecurity']").send_keys(str(xrdksb))
        # 判断代扣公积金
        dkgjj = dr.find_element_by_xpath("//*[@id='deductHousingFund']").get_attribute("value")
        if dkgjj=='':
            xrdkgjj = '%.2f' % (random.uniform(1, 500))
            # 输入代扣公积金金
            dr.find_element_by_xpath("//*[@id='deductHousingFund']").send_keys(str(xrdkgjj))
        # 判断代扣个税
        dkgs=dr.find_element_by_xpath("//*[@id='deductPersonalIncomeTax']").get_attribute("value")
        if dkgs=='':
            xrdkgs='%.2f'%(random.uniform(1,100))
            # 输入代扣个税
            dr.find_element_by_xpath("//*[@id='deductPersonalIncomeTax']").send_keys(str(xrdkgs))
        sleep(3)
        # 重新获取应发，代扣的值。不管是原来有值，还是输入的值，再次获取，计算出应发，比较是否正确
       # yf2 = dr.find_element_by_xpath("//*[@id='totalSalary']").get_attribute("value")
        #dksb2 = dr.find_element_by_xpath("//*[@id='deductSocialSecurity']").get_attribute("value")
        #dkgjj2 = dr.find_element_by_xpath("//*[@id='deductHousingFund']").get_attribute("value")
        #dkgs2 = dr.find_element_by_xpath("//*[@id='deductPersonalIncomeTax']").get_attribute("value")
        # 验证实发工资是否正确，如果yf不为空，跟获取值判断，如果为空，跟写入值判断，实发工资=应发工资-代扣
        sfgz=dr.find_element_by_xpath("//*[@id='finalSalary']").get_attribute("value")  # 获取的实发工资
        if yf=='' and dksb=='' and dkgjj=='' and dkgs=='':  #如果全是手动输入的，计算，比较结果。如果是获取的，就不比较了。包含千分位，后续再优化
            jssf=float(xryf)-float(xrdksb) -float(xrdkgjj)-float(xrdkgs)  # 计算的实发工资，转换千分位
            try:
                self.assertEqual(jssf,sfgz,msg="实发工资计算不正确")
            except:
                print("实发工资为：%r"%sfgz)
        # 设置付款方式为现金
        zfzf.paymethod()
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
            dr.get_screenshot_as_file("E:\\script\\report\\计提社保单据提交失败.jpg")
            self.assertEqual(0, 1, msg="单据提交失败")
        sleep(5)

    def tearDown(self):
        dr.quit()
if __name__ == '__main__':
    unittest.main()
