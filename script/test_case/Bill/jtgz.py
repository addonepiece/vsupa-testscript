"""
计提工资单据
"""
import unittest
import selenium.webdriver
from test_case.pagebase import Page
from selenium.common.exceptions import NoSuchElementException
from time import *
import random
from random import randrange
from random import uniform
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import re
from selenium.webdriver.common.by import By

class JitiBill(unittest.TestCase):
    """计提工资录单"""
    def setUp(self):
        global dr,jt,gs
        jt=Page()
        dr=jt.driver()
        jt.loginout("17700000001","Abc123456")
        # 进入控制台，搜索企业
        try:
            dr.find_element_by_xpath("//a[@href='/index']").click()
            print("进入控制台")
        except NoSuchElementException as e:
            print("登录跳转页面非首页")
        # 控制台搜索企业
        jt.kongzhitai("cyb0811企业")
        sleep(3)

    def formatNum(self,num):   # 金额进行千分位计算函数
        num = str(num)
        pattern = r'(\d+)(\d{3})((,\d{3})*)'
        while True:
            num, count = re.subn(pattern, r'\1,\2\3', num)
            if count == 0:
                break
        return num
    def jtgzadd(self):
        """
        计提工资录单
        :return:
        """
        global rate,kcs,gs,sfgz,dr,zycount
        jtjt=JitiBill()
        """
        要判断有没有职员，没有职员的时候添加职员，暂时不添加复制工资的功能。
        :return:
        """
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
        dr.find_elements_by_xpath("html/body/span/span/span[2]/ul/li[6]/ul/li")[0].click()
        # 判断是否有职员
        i = 0
        y = 1
        sleep(3)
        while i <= 5:  # 设置循环添加多少行
            if i==0:   # 第一行元素的xpath比较特殊，为tr
                a="tr"
            else:
                a="tr["+str(y)+"]"   # 其他行的元素xpath，tr后面是带编号的。如第二行是tr2，第三行是tr3
                if i==1:  # 一行的所有字段填写之后，i+1，判断是否跳出循环，不跳出循环的继续执行，就要新增一行。当i=1时，就是要新增第二行，在第一行前面点加号新增，第一行xpath是tr
                    dr.find_element_by_xpath("//*[@id='template6_table']/tbody/tr/td[1]/div/img[1]").click()  #新增一行
                elif i>1: # 当i大于1时，要在y-1行点新增，新增一行。如i=2,y=3时，即为第第二行录制完成，要新增第三行，此时要点击第二行前面的添加，y-1
                    b="tr["+str(y-1)+"]"
                    dr.find_element_by_xpath("//*[@id='template6_table']/tbody/" + b + "/td[1]/div/img[1]").click()

            zy = dr.find_element_by_xpath("//*[@id='template6_table']/tbody/"+a+"/td[3]/div[1]")  # 职员元素
            zy.click()  # 点击职员，让列表可见
            sleep(2)
            ActionChains(dr).move_to_element(zy).perform()  # 鼠标悬停，便于获取列表
            sleep(5)
            zylist = dr.find_elements_by_xpath("//*[@id='template6_table']/tbody/"+a+"/td[3]/div[2]/div/span/div/div/div")  # 获取职员列表
            zycount = len(zylist)  # 获取职员个数，如果只有两个，就添加只有。数目为2时，要么是一个职员，一个添加。要么是没有职员
            print("职员人数是：%r"%zycount)
            if zycount==2:    # 判断没有职员或是只有一个职员，添加职员
                zylist[-1].click()  # 点击添加
                sleep(3)
                # 只需要输入名字
                name=str("职员")+str(y)
                dr.find_element_by_xpath("//*[@id='name']").send_keys(name)  # 输入职员名称
                # 点击确定
                dr.find_element_by_xpath("//a[@class='layui-layer-btn0']").click()
                # 添加之后，不会自动定位到职员，要再去点击，获取新的列表，随机选择职员
                zy.click()  # 点击职员，让列表可见
                sleep(3)
                ActionChains(dr).move_to_element(zy).perform()
                zylist1 = dr.find_elements_by_xpath("//*[@id='template6_table']/tbody/"+a+"/td[3]/div[2]/div/span/div/div/div")  # 获取职员列表
                del zylist1[-1] # 去掉添加
                zycount1 = len(zylist1)  # 获取职员个数，如果只有两个，就添加职员。数目为2时，要么是一个职员，一个添加。要么是没有职员
                # 随机选择职员
                zylist1[random.randint(0,zycount1-1)].click()
            else:
                del zylist[-1]  # 去掉添加
                zycount = len(zylist)  # 获取职员个数，如果只有两个，就添加职员。数目为2时，要么是一个职员，一个添加。要么是没有职员
                # 随机选择职员
                zylist[random.randint(0, zycount - 1)].click()  # 随机选择职员
            # 随机选择部门
            dr.find_element_by_xpath("//*[@id='template6_table']/tbody/"+a+"/td[4]/div[1]").click()  # 点击部门，让列表可见
            bm=dr.find_element_by_xpath("//*[@id='template6_table']/tbody/"+a+"/td[4]/div[2]/div/select")
            Select(bm).select_by_value(str(random.randint(1, 3)))   # 管理部是1，销售部是2，生产部是3
            # 写入基本工资,还要判断个税
            dr.find_element_by_xpath("//*[@id='template6_table']/tbody/"+a+"/td[5]/div[1]").click()
            jbgz=random.uniform(1,5365)
            dr.find_element_by_xpath("//*[@id='template6_table']/tbody/"+a+"/td[5]/div[2]/div/input").send_keys(str(jbgz))
            # 写入绩效工资
            jxgz=random.uniform(1,530)
            dr.find_element_by_xpath("//*[@id='template6_table']/tbody/"+a+"/td[6]/div[1]").click()
            dr.find_element_by_xpath("//*[@id='template6_table']/tbody/"+a+"/td[6]/div[2]/div/input").send_keys(str(jxgz))
            # 写入养老，医疗，失业
            yanglao=random.uniform(1,530)
            yiliao=random.uniform(1,530)
            shiye=random.uniform(1,530)
            dkgjj=random.uniform(1,530)
            dr.find_element_by_xpath("//*[@id='template6_table']/tbody/"+a+"/td[8]/div[1]").click()
            dr.find_element_by_xpath("//*[@id='template6_table']/tbody/"+a+"/td[8]/div[2]/div/input").send_keys(str(yanglao))

            dr.find_element_by_xpath("//*[@id='template6_table']/tbody/"+a+"/td[9]/div[1]").click()
            dr.find_element_by_xpath("//*[@id='template6_table']/tbody/"+a+"/td[9]/div[2]/div/input").send_keys(str(yiliao))

            dr.find_element_by_xpath("//*[@id='template6_table']/tbody/"+a+"/td[10]/div[1]").click()
            dr.find_element_by_xpath("//*[@id='template6_table']/tbody/"+a+"/td[10]/div[2]/div/input").send_keys(str(shiye))

            dr.find_element_by_xpath("//*[@id='template6_table']/tbody/"+a+"/td[12]/div[1]").click()
            dr.find_element_by_xpath("//*[@id='template6_table']/tbody/"+a+"/td[12]/div[2]/div/input").send_keys(str(dkgjj))
            # 操作完之后，光标会固定到代扣公积金，会影响获取元素，点击实发工资，将鼠标定位移走
            dr.find_element_by_xpath("//*[@id='template6_table']/tbody/"+a+"/td[14]/div[1]").click()
            # 判断应发工资是否正确
            yfgz=dr.find_element_by_xpath("//*[@id='template6_table']/tbody/"+a+"/td[7]/div[1]").text  # 获取页面上的数字，即系统计算的结果
            sleep(3)
            jbgz='%.2f'%jbgz  # 因为输入的是浮点型，小数位数较多，取两位小数
            jxgz='%.2f'%jxgz
            yiliao='%.2f'%yiliao
            shiye='%.2f'%shiye
            dkgjj='%.2f'%dkgjj
            yf='%.2f'%(float(jbgz) + float(jxgz))
            yf=jtjt.formatNum(yf)  # 根据输入的值进行计算，调用函数，进行保留两位小数，并做千分位计算。根据输入计算结果，与页面上系统计算结果对比
            self.assertEqual(yf,yfgz,msg="应发工资不正确")
            # 判断社保合计是否正确
            sbhj=dr.find_element_by_xpath("//*[@id='template6_table']/tbody/"+a+"/td[11]/div[1]").text
            hj='%.2f'%(float(yanglao)+float(yiliao)+float(shiye))
            hj=jtjt.formatNum(hj)
            self.assertEqual(hj,sbhj,msg="社保合计不正确")
            # 判断个税是否正确。个税计算：应纳个人所得税税额=应纳税所得额×适用税率-速算扣除数，应纳税所得额=扣除三险一金后月收入-扣除标准
            ynssde='%.2f'%(float(jbgz)+float(jxgz)-float(yiliao)-float(yanglao)-float(shiye)-float(dkgjj))  # 计算应纳税所得额，按国内籍计算。国内3500，国外4800
            if float(ynssde)>3500.00:
                ynssde=float(ynssde)-3500.00
                if ynssde<=1500.00:
                    rate=0.03
                    kcs=0.00
                elif 1500.00<ynssde<=4500.00:
                    rate=0.10
                    kcs=105.00
                elif 4500.00<ynssde<=9000.00:
                    rate=0.20
                    kcs=555.00
                elif 9000.00<ynssde<=35000.00:
                    rate=0.25
                    kcs=1005.00
                elif 35000.00<ynssde<=55000.00:
                    rate=0.30
                    kcs=2755.00
                elif 55000.00<ynssde<=80000.00:
                    rate=0.35
                    kcs=5505.00
                elif ynssde>80000.00:
                    rate=0.45
                    kcs=13505.00
                gs = '%.2f'%(ynssde * rate - kcs)
                gs = jtjt.formatNum(gs)  # 根据输入的值计算的个税
                gs2 = dr.find_element_by_xpath("//*[@id='template6_table']/tbody/"+a+"/td[13]/div[1]").text  # 获取个税
                self.assertEqual(gs, gs2, msg="个税计算不正确")
                sfgz = '%.2f' % (float(jbgz) + float(jxgz) - float(yanglao) - float(yiliao) - float(shiye) - float(dkgjj) - float(gs))
            else:
                print("工资小于3500，不扣个税")
                gs1=dr.find_element_by_xpath("//*[@id='template6_table']/tbody/"+a+"/td[13]/div[1]").text  # 获取个税
                print(gs1)
                sfgz = '%.2f' % (float(jbgz) + float(jxgz) - float(yanglao) - float(yiliao) - float(shiye) - float(dkgjj))
            #判断实发工资是否正确，实发工资=基本工资+绩效工资-养老-医疗-失业-代扣公积金-个税
            sfgz=jtjt.formatNum(sfgz)
            sfgz2=dr.find_element_by_xpath("//*[@id='template6_table']/tbody/"+a+"/td[14]/div[1]").text
            self.assertEqual(sfgz,sfgz2,msg="实发工资不正确")
            sleep(2)
            y=y+1  # 一行录制完成后，+1，要录制新的一行
            i=i+1
        sleep(3)
        # 预览凭证，提交单据
        dr.find_element_by_xpath("//a[@role='button' and @class='lightblue-btn previewVoucher']").click()
        sleep(3)
        dr.find_element_by_xpath("//button[@type='button' and @class='bootbox-close-button close']").click()
        print("预览凭证成功")
        sleep(2)
        # 提交单据
        dr.find_element_by_xpath("//a[@role='button' and @class='bluetbn-btn save' and @data-status='2']").click()
        try:
            WebDriverWait(dr, 5, 0.1).until(EC.presence_of_element_located((By.ID, "notify_0")))
        except TimeoutException as e:
            print("单据提交失败")
            dr.get_screenshot_as_file("E:\\script\\report\\收款单据提交失败.jpg")
            self.assertEqual(0, 1, msg="单据提交失败")
        sleep(5)
    def tearDown(self):
        dr.quit()

if __name__ == '__main__':
    unittest.main()
