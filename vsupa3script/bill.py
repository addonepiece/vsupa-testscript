"""本脚本是财税师角色，登录系统，帮企业录单,先获取账套起始日期，获取目前结账区间，再去录单。字段定义，
date：区间
enterprise：企业名
billcount:单据总数"""

#coding=utf-8
from selenium import webdriver
from time import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os
import select
from selenium.webdriver.support.select import Select
from random import choice
import random
from random import randrange
from  random import uniform

# 登录系统
# import login.py  #调用登录
dr=webdriver.Chrome()
# 跳转到云算盘
dr.get("http://test.vsupa.com/homepage/login.html")
print("打开云算盘")
dr.maximize_window()
# 登录系统
dr.find_element_by_id("loginName").send_keys("17700000001")
sleep(2)
password=dr.find_element_by_id("password")
password.send_keys("123456")

dr.find_element_by_id("loginBtn").click()
print("登录成功")
sleep(8)
# 进入控制台
dr.find_element_by_xpath("//a[@href='/index']").click()
print("进入控制台")
sleep(2)
class kongzhitai():
    def __init__(self):
        #self.enterprise=enterprise
        print("开始输入企业搜索")
    def searchenterprise(self,enterprise):
        kongzhitai1 = dr.find_element_by_xpath("//input[@type='text' and @class='custom-search type_finace_control tt-input']")
        kongzhitai1.send_keys(enterprise)
        sleep(2)
        print("在管理控制台输入企业")
        ActionChains(dr).move_to_element(kongzhitai1).perform()  #鼠标悬停
        sleep(2)
        dr.find_element_by_xpath("//div[@class='ls-menu tt-open']").click()
        print("进入企业做账模块")
        sleep(5)

# 获取账套信息，录单的时候选择日期之前的月份，修改单据，录入单据时，进行判断
class setpage():
    global startaccout
    global type1
    global update1
    global jinxiaocundate
    def __init__(self):
        print("进入设置页面")
        sleep(3)
    def gosetpage(self):
        global startaccount
        dr.find_element_by_xpath("//*[@id='menu_list']/li[10]/a").click()
        print("进入账套页面")
        sleep(2)
        start = dr.find_element_by_id("startAccountPeriod") # 获取账套起始月
        startaccount=start.get_attribute("value")
        # 获取纳税人类型
    def getaccounttype(self):
        global type1
        global update1
        type=dr.find_element_by_xpath("//*[@id='accountType']")
        type1=type.get_attribute("value")
        if type1 == "2":
            type1="一般纳税人"
            update1="没有升级时间"
            return type1
        elif type1=="1":
            type1="小规模纳税人"
            return type1        # 如果是小规模纳税人，获取升级时间
            update=dr.find_element_by_xpath("//*[@id='upgradeAccountPeriod']")
            update1=update.get_attribute("value")
        else:
            return

        # 是否开启进销存
    @staticmethod
    def jinxiaocun():
        global jinxiaocundate
        global startaccout
        global type1
        global update1
        global jxctype
        jxc=dr.find_element_by_xpath("//*[@id='invoicingStartAccountperiod']")
        jinxiaocundate1=jxc.get_attribute("value")
        if "-" in jinxiaocundate1:
            jxctype=1
            jinxiaocundate=jinxiaocundate1
            return jxctype
        else:
            jxctype=0
            jinxiaocundate="企业没有开启进销存"
            return jxctype
    def print(self):
        print("企业纳税人类型是："+type1,"账套启用时间是："+startaccount,"账务升级时间是："+update1,"进销存启用时间是："+jinxiaocundate,jxctype)

# 获取结账日期，判断未结账首月。修改单据时可以使用
class checkout():
    global checkdate
    def __init__(self):
        print("进入结账页面")
    def check(self):
        global checkdate
        dr.find_element_by_xpath("//*[@id='menu_list']/li[3]/a").click()
        sleep(2)
        checkdate=dr.find_element_by_xpath("//*[@id='checkout']/div[1]/div/div[1]/span[2]").text
        print("当前未结账首月为："+checkdate)
        return

"""录入单据，要先判断纳税人类型，一般纳税人带进销存，一般纳税人不带进销存，小规模纳税人带进销存，小规模纳税人不带进销存。以及是否开启精确到日"""
# bill类，有区间判断函数，有获取单据数目函数，有录单函数
# 进入单据模块，获取当前月份，获取单据数目
class billlist():
    global count

    def __init__(self):
        dr.find_element_by_xpath("//*[@id='menu_list']/li[1]/a").click()
        sleep(2)
        print("进入单据模块")
    def getdate(self):  # 获取当前会计区间
        date = dr.find_element_by_xpath("//*[@id='list_view']/div/div[1]/div/div[1]/fieldset/div/div[1]/input")
        date2 = date.get_attribute("value")
        print("当前单据区间为:%r" % date2,"账套起始月是："+startaccount)
    def billcounts(self):# 获取单据总数
        global count
        count = dr.find_element_by_xpath("//*[@id='list_view']/div/div[2]/div/div/div[1]/div[2]/div[4]/div/span[1]").text
        print("单据总数:" + count)
        return
    def searchtest(self,searchtype):
        if searchtype=="按状态":   # 如果传入的参数是状态
            path="//*[@id='list_view']/div/div[2]/div/div/div[1]/div[2]/div[1]/table/thead/tr/th[6]/div/div/ul/li" #状态的定位地址
            statuspath="//*[@id='dlabel-status']"
        else:               # 传入的参数是缺单
            path="//*[@id='list_view']/div/div[2]/div/div/div[1]/div[2]/div[1]/table/thead/tr/th[7]/div/div/ul/li"
            statuspath="//*[@id='dlabel-lackPic']"

        lenth=len(dr.find_elements_by_xpath(path))
        i=0
        while i<lenth:
            search=dr.find_element_by_xpath(statuspath)
            search.click()
            ActionChains(dr).move_to_element(search)
            statuslists=search.find_elements_by_xpath(path)
            sleep(5)
            status=statuslists[i]
            status1=status.text
            #print(status1)
            status.click()
            sleep(4)
            count = dr.find_element_by_xpath("//*[@id='list_view']/div/div[2]/div/div/div[1]/div[2]/div[4]/div/span[1]").text
            print("检索项"+status1+"的单据总数:" + count)
            sleep(3)
            i=i+1
        dr.find_element_by_xpath("//*[@id='menu_list']/li/a").click()    # 重载模块，清除所选
        sleep(5)

    def bothsearch(self,type1,type2):
        # 联合搜索，先按状态搜，再按缺单搜，或是相反
        if type1=="按状态":
            path1="//*[@id='list_view']/div/div[2]/div/div/div[1]/div[2]/div[1]/table/thead/tr/th[6]/div/div/ul/li"
            statuspath1="//*[@id='dlabel-status']"
            path2="//*[@id='list_view']/div/div[2]/div/div/div[1]/div[2]/div[1]/table/thead/tr/th[7]/div/div/ul/li"
            statuspath2="//*[@id='dlabel-lackPic']"
        else:
            path1 ="//*[@id='list_view']/div/div[2]/div/div/div[1]/div[2]/div[1]/table/thead/tr/th[7]/div/div/ul/li"
            statuspath1 ="//*[@id='dlabel-lackPic']"
            path2 ="//*[@id='list_view']/div/div[2]/div/div/div[1]/div[2]/div[1]/table/thead/tr/th[6]/div/div/ul/li"
            statuspath2 ="//*[@id='dlabel-status']"
        lenth1=len(dr.find_elements_by_xpath(path1))
        lenth2=len(dr.find_elements_by_xpath(path2))
        a=1
        b=1
        while a<lenth1:
            search1=dr.find_element_by_xpath(statuspath1)
            search1.click()
            ActionChains(dr).move_to_element(search1).perform()
            statuslists1=search1.find_elements_by_xpath(path1)
            sleep(5)
            status1=statuslists1[a]
            status2=status1.text
            status1.click()
            sleep(10)
            while b<lenth2:
                search2=dr.find_element_by_xpath(statuspath2)
                search2.click()
                ActionChains(dr).move_to_element(search2)
                statuslists2=search2.find_elements_by_xpath(path2)
                sleep(5)
                status3=statuslists2[b]
                status4=status3.text
                status3.click()
                sleep(4)
                count = dr.find_element_by_xpath("//*[@id='list_view']/div/div[2]/div/div/div[1]/div[2]/div[4]/div/span[1]").text
                print(status2+"与"+status4+"联合搜索的数目是："+count)
                b=b+1
            a=a+1
            b=1
            sleep(5)
        dr.find_element_by_xpath("//*[@id='menu_list']/li/a").click()  # 重载模块，清除所选

class addbilltool():
    def __init__(self):
        print("")

    def judgmenttype(self):
        #  判断账务类型，因为不同的账务类型，页面不一样。账务类型有四种，2小规模带进销存，3小规模不带进销存，0一般带进销存，1一般不带进销存
        # 先获取账务类型，与进销存
        global type
        goset2=setpage()
        goset2.gosetpage()
        sleep(3)
        accounttype=goset2.getaccounttype() # 获取账务类型
        jinxiaocun2=goset2.jinxiaocun()
        if type1=="一般纳税人":
            if jxctype==1:
                type=0
                sleep(5)
                print("该企业是一般纳税人带进销存")
            elif jxctype==0:
                type=1
                print("该企业是一般纳税人不带进销存")
        elif type1=="小规模纳税人":
            if jxctype==1:
                type=2
                print("该企业为小规模纳税人带进销存")
            else:
                type=3
                print("该企业为小规模纳税人不带进销存")
    def goadd(self):
        dr.find_element_by_xpath("//*[@id='menu_list']/li/a").click()    # 进入单据页面
        print("进入单据模块")
        sleep(3)
        dr.find_element_by_xpath("//*[@id='list_view']/div/div[1]/div/div[2]/fieldset/div[1]/div/button[1]").click()  # 点击添加
        print("进入单据添加页面")
        sleep(5)
    def paymethod(self):            # 获取付款方式，添加，选择付款方式
        pay_method = dr.find_element_by_id("pay_method")
        pay_method2 = dr.find_element_by_id("select2-pay_method-container")
        method = pay_method2.get_attribute("title")
        if method != "现金":
            print("付款方式不是现金")
            pay_method2.click()
            Select(pay_method).select_by_value("noChild-1")
            print("付款方式改为现金")
            pay_method2.click()
            # 收起下拉框
        else:
            print("付款方式是现金")
        sleep(5)
    def changetype(self,i):
        self.i=i
        billtype = dr.find_element_by_xpath("//*[@id='detail_view']/div/div/div[1]/div/div[1]/div[1]/div[1]/select")
        dr.find_element_by_xpath("//*[@id='detail_view']/div/div/div/div/div/div/div/span/span/span").click()
        ActionChains(dr).move_to_element(billtype)
        sleep(2)
        dr.find_elements_by_xpath("html/body/span/span/span[2]/ul/li")[i].click()
    def xscg(self,x):
        """
        这个函数提取的功能是，销售和采购单据，销售和采购添加函数会调用。一般纳税人带进销存的，获取商品列表，添加商品，设置金额，数量等。
        需要传入1个参数。
        :param x: 商品名称的xpath地址,,销售是template2_table,采购是template3_table,就数字不一样，用传参的方式写入
        :return:
        """
        print("获取商品列表")
        sp = dr.find_element_by_xpath("//*[@id='"+x+"']/tbody/tr/td[3]/div[1]")
        sp.click()
        sleep(5)
        ActionChains(dr).move_to_element(dr.find_element_by_xpath("//*[@id='"+x+"']/tbody/tr/td[3]/div[1]"))
        bbb = dr.find_element_by_xpath("//*[@id='"+x+"']/tbody/tr/td[3]/div[2]/div/span/div/div")
        ccc = bbb.text
        print(ccc)
        splists = dr.find_elements_by_xpath("//*[@id='"+x+"']/tbody/tr/td[3]/div[2]/div/span/div/div/div")
        sleep(5)
        # 如果商品只有两个，就是没有商品，两个是'未检测到数据'和’添加‘。此时需要添加商品
        if len(splists) == 2:
            splists[-1].click()  # 点击最后一项，即为添加
            sleep(3)
            dr.find_element_by_xpath("//*[@id='name']").send_keys("商品1")  # 写入商品名称
            sleep(2)
            # 判断是否有单位，没有的话，添加
            # 获取单位的select的option个数，为0时单位为空
            dw = dr.find_element_by_xpath("//*[@id='commodityUnitId']")
            dw.click()
            sleep(2)
            dwcount = len(dw.find_elements_by_tag_name("option"))
            print(dwcount)
            if dwcount == 0:  # 为0表示没有单位数据，要添加单位
                dr.find_element_by_xpath("//*[@id='addUnits']/img").click()  # 添加单位，点击弹出添加框
                sleep(4)
                # dr.find_element_by_xpath("//*[id='addCommodityUtil']/fieldset/div/div/input").click()
                dr.find_element_by_xpath("//*[@id='name' and @placeholder='最大长度16位' and @data-bv-field='name']").send_keys("单位1")  # 随机输入单位名称
                dr.find_element_by_xpath("//button[@type='button' and @class='btn bluetbn-btn dir']").click()  # 关闭对话框
                sleep(4)
            else:
                print("单位选默认值")
            dr.find_element_by_xpath("//button[@type='button' and @class='btn bluetbn-btn']").click()  # 关闭添加单位对话框
            sleep(5)
            # 写入后，商品不会自动填充，还是要去选择商品
            sp.click()
            sleep(5)
            ActionChains(dr).move_to_element(dr.find_element_by_xpath("//*[@id='"+x+"']/tbody/tr/td[3]/div[1]"))
            bbb = dr.find_element_by_xpath("//*[@id='"+x+"']/tbody/tr/td[2]/div[3]/div/span/div/div")
            ccc = bbb.text
            print(ccc)
            splists = dr.find_elements_by_xpath("//*[@id='"+x+"']/tbody/tr/td[3]/div[2]/div/span/div/div/div")
            sleep(5)
            del splists[-1]  # 去除掉添加
            del splists[-1]  # 去掉折扣
            spcount = len(splists)
            spcount = len(splists)
            spcount = len(splists)
            print("该企业销售单可用商品有%r个" % spcount)
            # 随机选择一个商品
            # 鼠标悬停，点击随机序列号
            splists[random.randint(0, spcount - 1)].click()
            sleep(6)
            spm = sp.text
            print("随机选择一个商品%r" % spm)
        else:
            del splists[-1]  # 去除掉添加
            del splists[-1]  # 去掉折扣
            spcount = len(splists)
            spcount = len(splists)
            spcount = len(splists)
            print("该企业销售单可用商品有%r个" % spcount)
            # 随机选择一个商品
            # 鼠标悬停，点击随机序列号
            splists[random.randint(0, spcount - 1)].click()
            sleep(6)
            spm = sp.text
            print("随机选择一个商品%r" % spm)
            # 单位自动获取，不用设置，但是要获取单位的值
            sleep(2)
            spdw = dr.find_element_by_xpath("//*[@id='"+x+"']/tbody/tr/td[4]/div[1]").text
            print("商品单位为：%r" % spdw)
            # 数量设置
            dr.find_element_by_xpath("//*[@id='"+x+"']/tbody/tr/td[5]/div[1]").click()
            dr.find_element_by_xpath("//*[@id='"+x+"']/tbody/tr/td[5]/div[2]/div/input").send_keys(str(random.randint(0, 999999999)))
            print("随机设置数量")
            # 金额设置

            dr.find_element_by_xpath("//*[@id='"+x+"']/tbody/tr/td[7]/div[1]").click()
            dr.find_element_by_xpath("//*[@id='"+x+"']/tbody/tr/td[7]/div[2]/div/input").send_keys(str(random.uniform(0, 999999999)))

            # 设置税率，税率自动显示了，不显示
            # dr.find_element_by_xpath("//*[@id='"+x+"']/tbody/tr/td[8]/div[1]").click()
            # dr.find_element_by_xpath("//*[@id='"+x+"']/tbody/tr/td[8]/div[2]/div/input").send_keys("0.17")
            # print("设置税率0.17，自动计算税额")

            # 单价自动计算，获取单价
            sleep(5)
            spdj = dr.find_element_by_xpath("//*[@id='"+x+"']/tbody/tr/td[6]/div[1]").text
            print("商品单价为：%r" % spdj)
            # 预览凭证
            sleep(3)
            dr.find_element_by_xpath("//*[@id='footer_title']/div/div[1]/a").click()  # 点击预览凭证
            sleep(5)
            dr.find_element_by_xpath(
                "//button[@type='button' and @class='bootbox-close-button close']").click()  # 关闭预览对话框
            # 提交单据
            sleep(3)
            dr.find_element_by_xpath("//*[@id='footer_title']/div/div[4]/a").click()    #提交单据

class addfybill():
    def addfeiyong(self):          # 添加费用单据。进入添加页面，默认就是费用类型，无需切换类别
        """
        费用添加函数，四种财务类型，一般纳税人两种相同，小规模纳税人两种相同。一般比小规模，多了两个字段，税率和税额
        先获取付款方式，再选择费用名称，部门名称，写入金额
        判断纳税人类型是一般，选择税率和税额。否则为小规模的
        预览凭证，提交单据
        :return:
        """
        print("开始添加费用类单据")
        feiyong_method=addbilltool()
        feiyong_method.paymethod()     # 付款方式选为现金
        # 名称设置
        fymingcheng = dr.find_element_by_xpath("//*[@id='template1_table']/tbody/tr/td[2]/div[1]")
        fymingcheng.click()
        ActionChains(dr).move_to_element(fymingcheng).perform()
        sleep(2)
        # 获取名称列表并随机点击一个名称
        fymclists = dr.find_elements_by_xpath("//*[@id='template1_table']/tbody/tr/td[2]/div[2]/div/span/div/div/div")
        fymclists[random.randint(0, len(fymclists) - 1)].click()
        print("随机选择一个费用名称")
        # 部门设置，获取部门列表，随机选择一个部门
        dr.find_element_by_xpath("//*[@id='template1_table']/tbody/tr/td[3]/div[1]").click()
        sleep(2)
        bumen = dr.find_element_by_xpath("//*[@id='template1_table']/tbody/tr/td[3]/div[2]/div//select")
        Select(bumen).select_by_value(str(random.randint(1, 3)))
        print("随机选择部门")
        # 金额设置
        jine = dr.find_element_by_xpath("//div[@class='cell_data pr30']")
        sleep(2)
        jine.click()
        sleep(2)
        jine2 = jine.get_attribute("class")
        if jine2 == "cell_data pr30 hide":
            dr.find_element_by_xpath("//*[@id='template1_table']/tbody/tr/td[4]/div[2]/div/input").send_keys(str(random.uniform(0, 999999999)))
            # print("费用金额写入%r"%je)
        else:
            print("金额为空")
        if type==0 or type==1: # 如果是一般纳税人企业（带进销存或不带），费用包含：名称，部门，金额，税率，税额5个字段
            print("该企业是一般纳税人带进销存，有五个参数，名称，部门，金额，税率，税额，需要设置税率和税额")
            # 税率设置
            dr.find_element_by_xpath("//*[@id='template1_table']/tbody/tr/td[5]/div[1]").click()
            sleep(2)
            shuilv=dr.find_element_by_xpath("//*[@id='template1_table']/tbody/tr/td[5]/div[2]/div/select")
            print(shuilv.text)
            sleep(5)
            shuilvcount=len(shuilv.find_elements_by_tag_name("option"))
            Select(shuilv).select_by_index(random.randint(0, shuilvcount - 1))    # 选择随机value税率
            sleep(3)
            print("随机选择税率")
        # 预览凭证
        dr.find_element_by_xpath("//a[@role='button' and @class='lightblue-btn previewVoucher']").click()
        sleep(3)
        dr.find_element_by_xpath("//button[@type='button' and @class='bootbox-close-button close']").click()
        print("预览凭证成功")
        sleep(2)
        # 提交单据
        dr.find_element_by_xpath("//a[@role='button' and @class='bluetbn-btn save' and @data-status='2']").click()
        print("提交费用单据")
class addsalebill():
    global khcount
    def __init__(self):
        print("开始添加销售单据，常规销售单添加，不包含折扣，红冲") # 折扣与红冲的另外写
    def changetosalec(self):
        sleep(3)
        billtool = addbilltool()
        if (dr.find_element_by_xpath("//*[@id='detail_view']/div/div/div/div/div/div/div/span/span/span")):
            print("当前在单据添加页面，开始切换类型为销售")
            billtool.changetype(1)
        else:
            print("当前不在单据添加页面，需要进入单据添加页面")
            billtool.goadd()    # 进入添加页面
            sleep(3)
            billtool.changetype(1)
    def addsalebill(self):
        """
        四种纳税人类型，一般纳税人带进销存与一般纳税人不带进销存是一样的。合并
        先获取付款方式。
        判断纳税人类型，带进销存的一起写。
        :return:
        """
        global khcount
        salesale=addbilltool()
        salesale.paymethod()# 付款方式切换成现金
        # 判断纳税人类型
        if type==0 or type==2:  # 该企业是一般纳税人带进销存，销售单有，客户，收款方式，商品名，单位，数量，单价，金额，税率，税额，折后金额，折后税额
            print("该企业为一般或小规模带进销存企业，销售单包含：客户，收款方式，商品名，单位，数量，单价，金额，税率，税额，折后金额，折后税额11个字段")
            # 客户设置，先要判断有没有客户。。有的话选择，没有的话添加
            dr.find_element_by_xpath("//*[@id='select2-auxiliary_users-container']").click()
            kehulists = dr.find_elements_by_xpath("html/body/span/span/span[2]/ul/li")
            del kehulists[0]  # 去除--请选择--这个项
            khcount = len(kehulists)
            if khcount!=0:
                print("该企业共有 %r 个客户"%khcount)
               # 随机选择一个客户
                i = random.randint(0, khcount - 1)
                kehulists[i].click()  # 随机点击一个客户
                sleep(3)
                kh = dr.find_element_by_xpath("//*[@id='select2-auxiliary_users-container']").text
                print("随机选择一个客户%r" % kh)
            else:
                print("该企业没有客户，需要添加客户")
                # 执行添加客户操作
                sleep(3)
                dr.find_element_by_xpath("/html/body/span/span/span[3]").click()   # 点击添加
                sleep(2)
                dr.find_element_by_xpath("//*[@id='name']").send_keys("客户123")    # 写入客户名
                dr.find_element_by_xpath("//*[@data-bb-handler='success' and @type='button' and @class='btn bluetbn-btn confirmBtn']").click()
                #添加客户之后，系统自动将添加的客户选中
                sleep(2)
                print("已经成功添加客户")
            # 商品名称设置
            sleep(3)
            #调用函数
            salesale.xscg('template2_table')
            sleep(3)
            print("添加销售单据成功")
        elif type==1:  # 一般纳税人不带进销存
            return

        else:           # 小规模纳税人不带进销存
            return
            # 预览凭证

# 添加采购单据
class AddCaigouBill():
    def __init__(self):
        print("开始添加采购单据，采购常规单，不包含红冲，红冲暂估，折扣")
    def ChangeToCaigou(self):
        sleep(3)
        billtool1=addbilltool()
        if (dr.find_element_by_xpath("//*[@id='detail_view']/div/div/div/div/div/div/div/span/span/span")):
            print("当前在单据添加页面，开始切换类型为采购")
            billtool1.changetype(2)
        else:
            print("当前不在单据添加页面，需要进入单据添加页面")
            billtool1.goadd()    # 进入添加页面
            sleep(3)
            billtool1.changetype(2)
            sleep(5)
    def AddCaigouBill(self):
        """
        一般纳税人带进销存比小规模纳税人带进销存，多了两个字段，抵扣情况和采购类型，其他都是一样的。目前这两个不考虑，后续可以添加随机选择。
        先判断type=0 or type=2.再判断type=0，操作抵扣情况和采购类型，随机选择。跳出判断。执行其他字段的操作。
        :return:
        """
        # 获取付款方式
        cgcg = addbilltool()
        cgcg.paymethod()
        # 判断纳税人类型
        if type==0 or type==2:  # 该企业是一般纳税人带进销存
            print("该企业是一般纳税人或者小规模带进销存")
            if type==0:  # 该企业是一般纳税人带进销存，多1个字段的操作，抵扣情况
                print("该企业为一般纳税人多进销存，多一个字段，抵扣情况，开始随机选择抵扣情况")
                dikou=dr.find_element_by_xpath("//*[@id='deduction']")  # 点击抵扣情况，弹出下拉框
                dikou.click()
                sleep(2)
                Select(dikou).select_by_value(str(random.randint(1,5)))  # 抵扣情况一共五个值，1正常抵扣，2不能抵扣，3待认证，4待抵扣，5进项转出，随机选择
                sleep(3)
            # 获取采购类型，随机选择
            cgtype=dr.find_element_by_xpath("//*[@id='type']")  # 点击采购类型
            cgtype.click()
            sleep(2)
            Select(cgtype).select_by_value(str(random.randint(1,2)))  #  采购类型有两个值，1普通采购，2暂估采购，随机选择
            # 获取供应商，如果没有，添加供应商
            sleep(5)
            dr.find_element_by_xpath("//*[@id='select2-auxiliary_suppliers-container']").click()  # 点击供应商，弹出下拉框
            gyslists=dr.find_elements_by_xpath("html/body/span/span/span[2]/ul/li")  # 获取供应商下拉列表
            del gyslists[0]  # 去除--请选择--这一项
            gyscount=len(gyslists)  # 获取供应商个数
            if gyscount!=0:
                print("该企业共有%r个供应商"%gyscount)   #判断供应商是否为空。供应商不为空
                # 随机选择一个供应商
                gyslists[random.randint(0,gyscount-1)].click()
                sleep(3)
                gys=dr.find_element_by_xpath("//*[@id='select2-auxiliary_suppliers-container']").text
                print("随机选择一个供应商%r"%gys)
            else:
                print("该客户没有供应商，需要添加供应商")
                sleep(3)
                dr.find_element_by_xpath("/html/body/span/span/span[3]").click()  # 点击添加
                sleep(2)
                dr.find_element_by_xpath("//*[@id='name']").send_keys("供应商123")  #写入供应商名，名字为供应商+随机数
                sleep(3)
                dr.find_element_by_xpath("//*[@data-bb-handler='success' and @type='button' and @class='btn bluetbn-btn confirmBtn']").click()  #点击确定，关闭对话框

            # 获取商品名称列表，如果商品为空，添加商品。调用函数xscg()
            cgcg.xscg('template3_table')
            print("采购单据添加成功")
        elif type==1:  # 一般纳税人不带进销存
            return
        elif type==3:  # 小规模不带进销存
            return
class AddGetBill():
    def __init__(self):
        print("开始添加收款类单据，收款类单据不分纳税人类型")
    def ChangeToGetbill(self):
        sleep(3)
        billtool2 = addbilltool()
        if (dr.find_element_by_xpath("//*[@id='detail_view']/div/div/div/div/div/div/div/span/span/span")):
            print("当前在单据添加页面，开始切换类型为收款")
            billtool2.changetype(3)
        else:
            print("当前不在单据添加页面，需要进入单据添加页面")
            billtool2.goadd()  # 进入添加页面
            sleep(3)
            billtool2.changetype(3)
            sleep(5)
    def AddGetBill(self):
        """
        收款类单据，有三个字段，收款方式，付款方，还有一个付款方明细。金额。
        付款方是默认的五类，利息，客户，供应商，其他往来，股东。利息没有明细，其他四项有。选择的时候要判断是否需要填写明细
        :return:
        """
        # 收款和付款，只有一个收款方不一样，付款没有利息。考虑两个单据一起写。。。通过传参的形式调用
        # 收款方式
        sleep(4)
        fkmethod=addbilltool()
        fkmethod.paymethod()
        # 付款方获取
        dr.find_element_by_xpath("//*[@id='template4_table']/tbody/tr/td[2]/div[1]").click()
        sleep(2)
        fkf=dr.find_element_by_xpath("//*[@id='template4_table']/tbody/tr/td[2]/div[2]/div/select")
        print(fkf.text)
        fkflist=dr.find_elements_by_xpath("//*[@id='template4_table']/tbody/tr/td[2]/div[2]/div/select")
        f=random.choice([30,20,21,22,23])
        print(f)
        Select(fkf).select_by_value(str(f))
        sleep(4)
        # 如果选择的是利息，不需要明细，如果不是利息，则需要设置下一个字段
        sleep(3)
        if f!=30:  # value值是30，是利息,利息不需要明细。不是利息时，需要操作下一个字段
            # 获取明细列表，看是否为空
            fkfmx=dr.find_element_by_xpath("//*[@id='template4_table']/tbody/tr/td[3]/div[2]/div/span/div") # 付款方明细变成可见后，元素xpath
            fkfmxlist=dr.find_elements_by_xpath("//*[@id='template4_table']/tbody/tr/td[3]/div[2]/div/span/div/div/div") # 获取付款方明细列表
            print(fkfmx.text) # 打印付款方明细名称
            fkfcount=len(fkfmxlist)
            print(fkfcount)
            if fkfcount==2:  # 如果序列中有两个原素，就是说明细为空。两个原素是添加，和未检测到数据。此时操作添加按钮
                fkfmxlist[-1].click()  # 添加是序列的最后一个元素，点击添加，弹出对话框
                sleep(3)
                dr.find_element_by_xpath("//*[@id='name']").send_keys("测试1311")
                dr.find_element_by_xpath("//*[@id='layui-layer1']/div[3]/a[1]").click() # 关闭添加对话框
                # 添加完付款方明细后，也不会自动添加。执行手动随机选择操作
                sleep(3)
                dr.find_element_by_xpath("//*[@id='template4_table']/tbody/tr/td[3]/div[1]").click()  # 鼠标点击付款方明细，让元素列表可见
            # 获取明细列表，看是否为空
            fkfmx2 = dr.find_element_by_xpath("//*[@id='template4_table']/tbody/tr/td[3]/div[2]/div/span/div")  # 付款方明细变成可见后，元素xpath
            fkfmxlist2 = dr.find_elements_by_xpath("//*[@id='template4_table']/tbody/tr/td[3]/div[2]/div/span/div/div/div")  # 获取付款方明细列表
            # 需要去除添加
            del fkfmxlist2[-1]
            fkfcount2=len(fkfmxlist2)
            fkfmxlist2[random.randint(0,fkfcount2-1)].click()
        # 写入金额
        sleep(3)
        dr.find_element_by_xpath("//*[@id='template4_table']/tbody/tr/td[4]/div[1]").click()
        dr.find_element_by_xpath("//*[@id='template4_table']/tbody/tr/td[4]/div[2]/div/input").send_keys(str(random.uniform(1,999999999)))
        sleep(3)
        # 预览凭证
        dr.find_element_by_xpath("//a[@role='button' and @class='lightblue-btn previewVoucher']").click()
        sleep(3)
        dr.find_element_by_xpath("//button[@type='button' and @class='bootbox-close-button close']").click()
        print("预览凭证成功")
        sleep(2)
        # 提交单据
        dr.find_element_by_xpath("//a[@role='button' and @class='bluetbn-btn save' and @data-status='2']").click()
        print("提交收款单据")
# 付款单据
class AddPayBill():
    def __init__(self):
        print("开始添加付款单据")
    def ChangeToPaybill(self):
        sleep(3)
        billtool3 = addbilltool()
        if (dr.find_element_by_xpath("//*[@id='detail_view']/div/div/div/div/div/div/div/span/span/span")):
            print("当前在单据添加页面，开始切换类型为付款")
            billtool3.changetype(4)
        else:
            print("当前不在单据添加页面，需要进入单据添加页面")
            billtool3.goadd()  # 进入添加页面
            sleep(3)
            billtool3.changetype(4)
            sleep(5)
    def PayBill(self):
        sleep(4)
        paybill = addbilltool()
        paybill.paymethod()
        # 收款方获取
        dr.find_element_by_xpath("//*[@id='template5_table']/tbody/tr/td[2]/div[1]").click()
        sleep(2)
        skf = dr.find_element_by_xpath("//*[@id='template5_table']/tbody/tr/td[2]/div[2]/div/select")
        print(skf.text)
        skflist = dr.find_elements_by_xpath("//*[@id='template5_table']/tbody/tr/td[2]/div[2]/div/select")
        s = random.choice([ 20, 21, 22, 23])
        print(s)
        Select(skf).select_by_value(str(s))
        sleep(4)
        # 获取明细列表，看是否为空
        skfmx = dr.find_element_by_xpath("//*[@id='template5_table']/tbody/tr/td[3]/div[2]/div/span/div")  # 收款方明细变成可见后，元素xpath
        skfmxlist = dr.find_elements_by_xpath("//*[@id='template5_table']/tbody/tr/td[3]/div[2]/div/span/div/div/div")  # 获取收款方明细列表
        print(skfmx.text)  # 打印收款方明细名称
        skfcount = len(skfmxlist)
        print(skfcount)
        if skfcount == 2:  # 如果序列中有两个原素，就是说明细为空。两个原素是添加，和未检测到数据。此时操作添加按钮
            skfmxlist[-1].click()  # 添加是序列的最后一个元素，点击添加，弹出对话框
            sleep(3)
            dr.find_element_by_xpath("//*[@id='name']").send_keys("测试11321")
            dr.find_element_by_xpath("//*[@id='layui-layer2']/div[3]/a[1]").click()  # 关闭添加对话框
            # 添加完收款方明细后，也不会自动添加。执行手动随机选择操作
            sleep(3)
            dr.find_element_by_xpath("//*[@id='template5_table']/tbody/tr/td[3]/div[1]").click()  # 鼠标点击付款方明细，让元素列表可见
        # 获取明细列表，看是否为空
        skfmx2 = dr.find_element_by_xpath("//*[@id='template5_table']/tbody/tr/td[3]/div[2]/div/span/div")  # 收款方明细变成可见后，元素xpath
        skfmxlist2 = dr.find_elements_by_xpath("//*[@id='template5_table']/tbody/tr/td[3]/div[2]/div/span/div/div/div")  # 获取收款方明细列表
        # 需要去除添加
        del skfmxlist2[-1]
        skfcount2 = len(skfmxlist2)
        skfmxlist2[random.randint(0, skfcount2 - 1)].click()
        # 写入金额
        sleep(3)
        dr.find_element_by_xpath("//*[@id='template5_table']/tbody/tr/td[4]/div[1]").click()
        dr.find_element_by_xpath("//*[@id='template5_table']/tbody/tr/td[4]/div[2]/div/input").send_keys(str(random.uniform(1, 999999999)))
        sleep(3)
        # 预览凭证
        dr.find_element_by_xpath("//a[@role='button' and @class='lightblue-btn previewVoucher']").click()
        sleep(3)
        dr.find_element_by_xpath("//button[@type='button' and @class='bootbox-close-button close']").click()
        print("预览凭证成功")
        sleep(2)
        # 提交单据
        dr.find_element_by_xpath("//a[@role='button' and @class='bluetbn-btn save' and @data-status='2']").click()
        print("提交付款单据成功")

# 调用进入控制台，搜索企业，进入做账模块
enterprise=kongzhitai()
enterprise.searchenterprise("cyb0811企业")
sleep(3)

# 进入账套页面，获取账套信息
# 为了加快执行速度，先屏蔽，到时候再放开
#goset=setpage()
#goset.gosetpage()
#goset.getaccounttype()
#goset.jinxiaocun()
#goset.print()

# 进入结账页面，获取当前会计区间
# 为了加快执行速度，先屏蔽，到时候再放开
#check1=checkout()
#check1.check()
sleep(3)

# 回到单据页面
# 下面是单据列表页面操作，搜索
#billsearch=billlist()
# 为了加快执行速度，先屏蔽，到时候再放开
#billsearch.searchbystatus()
#billsearch.searchbylost()
#billsearch.searchbystatus()
#billsearch.searchtest("按状态")
#billsearch.searchtest("按缺单")
#billsearch.bothsearch("按状态","按缺单")

# 进入单据添加页面
billtool=addbilltool()
billtool.judgmenttype()
billtool.goadd()

# 添加费用单
#fybill=addfybill()
#fybill.addfeiyong()

# 进入销售添加页面，添加销售单据
#salebill=addsalebill()
#salebill.changetosalec()
#salebill.addsalebill()

# 添加采购单
#cgbill=AddCaigouBill()
#cgbill.ChangeToCaigou()
#cgbill.AddCaigouBill()

# 添加收款单据
skbill=AddGetBill()
skbill.ChangeToGetbill()
skbill.AddGetBill()

# 添加付款单据
fkbill=AddPayBill()
fkbill.ChangeToPaybill()
fkbill.PayBill()
