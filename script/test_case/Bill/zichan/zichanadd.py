"""资产添加单据"""
import unittest
from time import *
from test_case.pagebase import Page
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException,TimeoutException
import random
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class ZhiChan(unittest.TestCase):
    """资产增加"""
    global dr,zc
    def setUp(self):
        global dr,zc
        zc=Page()
        dr=zc.driver()
        zc.loginout("17700000001","Abc123456")
        sleep(3)
        # 进入控制台，搜索企业
        try:
            dr.find_element_by_xpath("//a[@href='/index']").click()
            print("进入控制台")
        except NoSuchElementException as e:
            print("登录跳转页面非首页")
        # 控制台搜索企业
        zc.kongzhitai("cyb0808企业")
        sleep(3)
        # 进入单据添加
        dr.find_element_by_xpath("//*[@id='menu_list']/li/a").click()  # 进入单据页面
        print("进入单据模块")
        sleep(3)
        dr.find_element_by_xpath("//*[@id='list_view']/div/div[1]/div/div[2]/fieldset/div[1]/div/button[1]").click()  # 点击添加
        print("进入单据添加页面")
        # 切换单据类型为资产添加
        sleep(5)
        dr.find_element_by_xpath("//*[@id='detail_view']/div/div/div[1]/div/div[1]/div[1]/div[1]/span").click()
        billtype = dr.find_element_by_xpath("//*[@id='detail_view']/div/div/div[1]/div/div[1]/div[1]/div[1]/select")
        ActionChains(dr).move_to_element(billtype)
        sleep(2)
        dr.find_elements_by_xpath("html/body/span/span/span[2]/ul/li[8]/ul/li")[0].click()  # 点击资产增加
        sleep(3)
    def zcaddtool(self,i,y):
        """不同资产类型的一些共通方法。如资产类型的切换，增加方式（无形和固定有，长期待摊没有）。定义通用方法，调用"""
        global dr,zc
        # 资产类型切换
        zctype=dr.find_element_by_xpath("//*[@id='asset_type_select']")     # 资产类型有三个，固定资产，无形资产，长期待摊
        zctypevalue=[1,2,3]     # 1是固定资产，2是无形资产，3是长期待摊资产
        zctype.click()
        Select(zctype).select_by_value(str(i))
        sleep(3)
        zc.paymethod()    # 付款方式改为现金。不同的增加方式，有的方式需要付款方式，有的不需要。写在前面。。不需要的时候自动隐藏，也不影响
        sleep(3)
        # 增加方式随机选择
        if i==1 or i==2:   # 1是固定资产，2是无形资产，为1或者2时，需要设置增加方式。3长期待摊没有这个字段
            zjmode=dr.find_element_by_xpath("//*[@id='asset_add_method']")
            zjmode.click()
            ActionChains(dr).move_to_element(zjmode)
            sleep(2)
            zjmodelist=dr.find_elements_by_xpath("//*[@id='view-content-main']/form/div/div[2]/div/div/select/option")
            print(len(zjmodelist))
            Select(zjmode).select_by_index(str(random.randint(0,len(zjmodelist)-1)))   # 随机选择增加方式。根据index。因为不同资产类型，可能增加方式数据不同
        sleep(3)
        # 资产名称输入
        dr.find_element_by_xpath("//*[@id='template14_table']/tbody/tr/td[2]/div[1]").click()
        dr.find_element_by_xpath("//*[@id='template14_table']/tbody/tr/td[2]/div[2]/div/input").send_keys(str("资产")+str(i))
        sleep(3)
        # 类别随机选择
        dr.find_element_by_xpath("//*[@id='template14_table']/tbody/tr/td[3]/div[1]").click()  # 点击类别使得列表可见
        lb=dr.find_element_by_xpath("//*[@id='template14_table']/tbody/tr/td[3]/div[2]/div/select")
        lblist=dr.find_elements_by_xpath("//*[@id='template14_table']/tbody/tr/td[3]/div[2]/div/select/option")
        print(len(lblist))
        Select(lb).select_by_index(str(random.randint(0,len(lblist)-1)))
        sleep(3)
        # 部门随机选择
        dr.find_element_by_xpath("//*[@id='template14_table']/tbody/tr/td[4]/div[1]").click()   # 点击是的列表可见
        bumen=dr.find_element_by_xpath("//*[@id='template14_table']/tbody/tr/td[4]/div[2]/div/select")
        Select(bumen).select_by_index(random.randint(0,2))  # value值有三个，1是管理部，2销售部，3生产部
        sleep(3)
        # 设置数量
        dr.find_element_by_xpath("//*[@id='template14_table']/tbody/tr/td[5]/div[1]").click()
        dr.find_element_by_xpath("//*[@id='template14_table']/tbody/tr/td[5]/div[2]/div/input").send_keys(str(random.randint(1,100)))
        sleep(5)
        # 金额设置
        dr.find_element_by_xpath("//*[@id='template14_table']/tbody/tr/td[7]/div[1]").click()
        sleep(3)
        dr.find_element_by_xpath("//*[@id='template14_table']/tbody/tr/td[7]/div[2]/div/input").send_keys(str(random.uniform(1, 999999999)))
        sleep(3)
        # 税率设置
        dr.find_element_by_xpath("//*[@id='template14_table']/tbody/tr/td[8]/div[1]").click()
        dr.find_element_by_xpath("//*[@id='template14_table']/tbody/tr/td[8]/div[2]/div/input").send_keys("0.05")
        # 单价跟税额自动计算了，不用写入
        sleep(3)
        if i==1:   # 固定资产需要设置残值率
            dr.find_element_by_xpath("//*[@id='template14_table']/tbody/tr/td[10]/div[1]").click()  # 点击残值率。点击之后默认填充0.05
            sleep(3)
        # 随机设置折旧方式或是摊销方式，名称不同，字段是同一个元素
        dr.find_element_by_xpath("//*[@id='template14_table']/tbody/tr/td[11]/div[1]").click()  # 点击使得列表可见
        zjfs=dr.find_element_by_xpath("//*[@id='template14_table']/tbody/tr/td[11]/div[2]/div/select")
        Select(zjfs).select_by_index(random.randint(0,2))  # 目前就三种，0平均年限法，1一次性加速折旧，2不提折旧
        # 折旧期限或是摊销期限，自动填充，不进行设置了
        sleep(3)
        # 写备注，摘要就不写了。影响凭证的摘要
        dr.find_element_by_xpath("//*[@id='bill_comment']").send_keys("单据单据55aaaa")
        #dr.find_element_by_xpath("//*[@id='bill_summary']").send_keys("单据单据55aaaa")
        # 预览凭证
        dr.find_element_by_xpath("//a[@role='button' and @class='lightblue-btn previewVoucher']").click()
        sleep(3)
        dr.find_element_by_xpath("//button[@type='button' and @class='bootbox-close-button close']").click()
        print("预览凭证成功")
        sleep(2)
        # 提交单据
        dr.find_element_by_xpath("//a[@role='button' and @class='bluetbn-btn save' and @data-status='2']").click()
        try:
            WebDriverWait(dr, 10, 0.1).until(EC.presence_of_element_located((By.ID, "notify_"+str(y)+"")))
        except TimeoutException as e:
            print("单据提交失败")
            dr.get_screenshot_as_file("E:\\script\\report\\资产增加单据提交失败.jpg")
            self.assertEqual(0, 1, msg="单据提交失败")
        sleep(5)
    def zcadd(self):
        zca=ZhiChan()
        zca.zcaddtool(1,0)
        zca.zcaddtool(2,1)
        zca.zcaddtool(3,2)
    def tearDown(self):
        dr.quit()
if __name__ == '__main__':
    unittest.main()
