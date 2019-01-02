"""现金存取单据\内部转账单据\对账单。不带进销存的企业，其他里面只有这三个类型。带进销存的多一些"""
import unittest
from test_case.pagebase import Page
from time import *
from selenium.common.exceptions import NoSuchElementException,TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import random

class xjnbdz(unittest.TestCase):
    """录制现金存取、内部转账、对账单"""
    global dr
    def setUp(self):
        global dr
        cq=Page()
        dr=cq.driver()
        cq.loginout("17700000001","Abc123456")
        sleep(3)
        # 进入控制台，搜索企业
        try:
            dr.find_element_by_xpath("//a[@href='/index']").click()
            print("进入控制台")
        except NoSuchElementException as e:
            print("登录跳转页面非首页")
        # 控制台搜索企业
        cq.kongzhitai("cyb0808企业")
        sleep(3)
        # 进入单据添加
        dr.find_element_by_xpath("//*[@id='menu_list']/li/a").click()  # 进入单据页面
        print("进入单据模块")
        sleep(3)
        dr.find_element_by_xpath(
            "//*[@id='list_view']/div/div[1]/div/div[2]/fieldset/div[1]/div/button[1]").click()  # 点击添加
        print("进入单据添加页面")

    def changetype(self,i):
        # 切换单据类型为
        """

        :param i: 传参，0是现金存取，1是内部转账，2是对账单
        :return:
        """
        sleep(5)
        dr.find_element_by_xpath("//*[@id='detail_view']/div/div/div[1]/div/div[1]/div[1]/div[1]/span").click()
        billtype = dr.find_element_by_xpath("//*[@id='detail_view']/div/div/div[1]/div/div[1]/div[1]/div[1]/select")
        ActionChains(dr).move_to_element(billtype)
        sleep(2)
        dr.find_elements_by_xpath("html/body/span/span/span[2]/ul/li[9]/ul/li")[i].click()  # 点击资产减少
        sleep(3)
    def yltj(self,n):
        # 预览提交单据
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
    def xjcqadd(self):
        # 录制现金存取单据
        global qtbill
        qtbill=xjnbdz()
        qtbill.changetype(0)
        sleep(3)
        # 类型随机选择，类型两种，存现和提现
        type=dr.find_element_by_xpath("//*[@id='type_select']")
        dr.find_element_by_xpath("//*[@id='type_select']").click()
        Select(type).select_by_value(str(random.randint(1,2)))   # 1是存现，2是提现
        sleep(2)
        # 填写金额
        # 设置金额
        dr.find_element_by_xpath("//*[@id='money']/div/div/input").send_keys(str(random.uniform(0, 999999999)))
        # 选择银行
        dr.find_element_by_xpath("//*[@id='bank' and @class='row']/div/div/div/div/span/span/span/span").click()
        banklist=dr.find_elements_by_xpath("html/body/span/span/span[2]/ul/li")  # 需要判断银行个数
        bankcount=len(banklist)   # 银行数量
        if bankcount<=2:     # 当只有两个时，可能是有银行，也可能是“未找到结果”和“添加”。最好是添加一个银行
            dr.find_element_by_xpath("/html/body/span/span/span[3]").click()
            sleep(2)
            dr.find_element_by_xpath("//*[@id='name']").send_keys("上海银行")
            dr.find_element_by_xpath("//*[@type='button' and @class='btn bluetbn-btn confirmBtn']").click()  # 点击关闭
            # 设置之后银行直接显示新添加数据
        else:
            banklist[random.randint(0,bankcount-1)].click()   # 随机选择银行点击
        sleep(3)
        # 预览和提交
        qtbill.yltj(0)
    def nbzzadd(self):
        global qtbill
        # 录制内部转账单据
        # 切换单据类型到内部转账
        sleep(3)
        qtbill.changetype(1)
        sleep(5)
        # 选择转出账号
        zczh=dr.find_element_by_xpath("//*[@id='form_bill_type19']/div/div[1]/div/div/div/span/span/span/span")
        zczh.click()
        ActionChains(dr).move_to_element(zczh)
        sleep(3)
        outbanklist=dr.find_elements_by_xpath("html/body/span/span/span[2]/ul/li")
        outbankcount=len(outbanklist)
        if outbankcount<=2:
            dr.find_element_by_xpath("/html/body/span/span/span[3]").click()
            dr.find_element_by_xpath("//*[@id='name']").send_keys("浦发银行")
            dr.find_element_by_xpath("//*[@type='button' and @class='btn bluetbn-btn confirmBtn']").click()  # 点击关闭
            sleep(2)
        else:
            outbanklist[random.randint(0,outbankcount-1)].click()
            sleep(2)
        # 转入银行选择
        dr.find_element_by_xpath("//*[@id='form_bill_type19']/div/div[2]/div/div/div/span/span/span/span").click()
        inbanklist=dr.find_elements_by_xpath("html/body/span/span/span[2]/ul/li")
        inbankcount=len(inbanklist)
        if inbankcount<=2:
            dr.find_element_by_xpath("/html/body/span/span/span[3]").click()
            sleep(3)
            dr.find_element_by_xpath("//*[@id='name']").send_keys("汇丰银行")
            dr.find_element_by_xpath("//*[@type='button' and @class='btn bluetbn-btn confirmBtn']").click()  # 点击关闭
            sleep(2)
        else:
            inbanklist[random.randint(0,inbankcount-1)].click()
        sleep(3)
        # 填写金额
        dr.find_element_by_xpath("//*[@id='money']").send_keys(str(random.uniform(0,999999999)))
        sleep(3)
        qtbill.yltj(1)
    def dzdadd(self):
        # 录制对账单单据
        global qtbill
        sleep(3)
        qtbill.changetype(2)
        sleep(3)
        # 选择银行
        dr.find_element_by_xpath("//*[@id='select2-bank-container']").click()
        banklist=dr.find_elements_by_xpath("//*[@id='select2-bank-results']/li")
        bankcount=len(banklist)
        if bankcount<=2:
            dr.find_element_by_xpath("/html/body/span/span/span[3]").click()
            sleep(3)
            dr.find_element_by_xpath("//*[@id='name']").send_keys("南丰银行")
            dr.find_element_by_xpath("//*[@type='button' and @class='btn bluetbn-btn confirmBtn']").click()  # 点击关闭
            sleep(2)
        else:
            banklist[random.randint(0, bankcount - 1)].click()
        sleep(3)
        # 填写金额
        dr.find_element_by_xpath("//*[@id='money']").send_keys(str(random.uniform(0,999999999)))
        sleep(3)
        # 提交单据。对账单没有预览
        # 提交单据
        dr.find_element_by_xpath("//a[@role='button' and @class='bluetbn-btn save' and @data-status='2']").click()
        try:
            WebDriverWait(dr, 10, 0.1).until(EC.presence_of_element_located((By.ID, "notify_2")))
        except TimeoutException as e:
            print("单据提交失败")
            dr.get_screenshot_as_file("E:\\script\\report\\对账单提交失败.jpg")
            self.assertEqual(0, 1, msg="单据提交失败")
        sleep(5)
    def add(self):
        lzqtbill=xjnbdz()
        lzqtbill.xjcqadd()
        lzqtbill.nbzzadd()
        lzqtbill.dzdadd()
    def tearDown(self):
        dr.quit()
if __name__ == '__main__':
    unittest.main()
