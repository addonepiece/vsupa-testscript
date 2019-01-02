"""
test_case里面的所有脚本，只适用于会计制度是beta版本的。如果选用民间制度，可能很多字段不一样，尤其是单据，导致脚本
无法顺利执行
"""


import unittest
from HTMLTestRunner import HTMLTestRunner
import time


# 加载测试文件
from test_case import login
from test_case import order
from test_case.Bill import feiyongbill
from test_case.Bill import billsearchlist
from test_case.Bill import salebill
from test_case.Bill import caigoubill
from test_case.Bill import fukuanbill,shoukuanbill
from test_case.Bill import jtgz
from test_case.Bill import jtsb
from test_case.Bill import jtgjj
from test_case.Bill import zfgz
from test_case.Bill import zfsbgjj
from test_case.Bill import jtsf
from test_case.Bill import zfsf
from test_case.Bill.zichan import zichanadd
from test_case.Bill.zichan import zichanjs
from test_case.Bill.qita import xjcq
from test_case.enterprise import fuwuqiye
from test_case.ordermanage import orderdaike
from test_case.Bill.forwhile import saleforwhile
from test_case.setconfig import zhangtao
from test_case.setconfig import spmanage
from test_case.setconfig import fzhs
if __name__=='__main__':
    # 构造测试集
    suite = unittest.TestSuite()
    # 登录
    #suite.addTest(login.Login("login"))
    # 订单
    """
    suite.addTest(order.Order("orderBuy"))
    # 单据模块列表搜索
    suite.addTest(billsearchlist.billsearchlist("search"))
    # 录制费用单据
    suite.addTest(feiyongbill.fyBill("AddFy"))
    # 录制销售单据
    suite.addTest(salebill.Addsale("salebilladd"))
    # 录制采购单据
    suite.addTest(caigoubill.Addcg("cgbilladd"))
    # 录制收款单据
    suite.addTest(shoukuanbill.shoukuanbill("skbilladd"))
    # 录制付款单据
    suite.addTest(fukuanbill.fukuanbill("fkbilladd"))
    # 录制计提工资
    suite.addTest(jtgz.JitiBill("jtgzadd"))
    # 录制计提社保
    suite.addTest(jtsb.Jtsb("jtsbadd"))
    # 录制计提公积金
    suite.addTest(jtgjj.JtGjj("jtgjjadd"))
    # 录制支付工资
    suite.addTest(zfgz.ZfGz("zfgz"))
    # 录制支付社保，公积金
    suite.addTest(zfsbgjj.ZfSbGjj("zfsbgjj"))
    # 录制计提税费
    suite.addTest(jtsf.JtSf("jtsfadd"))
    # 录制支付税费
    suite.addTest(zfsf.ZfSf("zfsfadd"))
    # 录制资产增加单据
    suite.addTest(zichanadd.ZhiChan("zcadd"))
    # 录制资产减少单据
    suite.addTest(zichanjs.ZcJs("jsbill"))
    # 录制现金存取，内部转账，对账单
    suite.addTest(xjcq.xjnbdz("add"))

    # 添加服务企业
    suite.addTest(fuwuqiye.Enterprise("AddEnterprise"))
"""
    # 代客下单
    suite.addTest(orderdaike.Daike("dkxd"))
    """
    # 循环录制销售单

    #suite.addTest(saleforwhile.saleforwhile("saleforwhilewhile"))

    # 添加账套
    suite.addTest(zhangtao.zhangtaoset("addzt"))

    # 添加商品
    suite.addTest(spmanage.SPadd("SPaddnormal"))
    suite.addTest(spmanage.SPadd("SPaddwhile"))

    # 添加辅助核算
    suite.addTest(fzhs.Fzhsadd("zkgqgadd"))
    """
    # 输出测试报告
    # 获取当前时间
    now=time.strftime("%Y-%m-%d %H_%M_%S")
    # 定义报告存放路径
    filename='E:\\script\\report'+'./.'+now+'result.html'
    fp=open(filename,'wb')
    # 运行测试
    runner=HTMLTestRunner(stream=fp,title='云算盘测试报告',description='用例执行情况：')
    runner.run(suite)
    fp.close()