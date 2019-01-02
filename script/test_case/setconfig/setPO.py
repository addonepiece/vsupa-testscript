# create by yb.c
# coding=utf-8
from selenium import webdriver
from test_case.pagebase import Page
class ActiomPo(object):
    """
    采取PO模式，封装设置页面通用的方法
    """
    def __init__(self):
        global dr,po
        po=Page()
        dr=po.driver()
    def gosetconfig(self):
        dr.find_element_by_xpath("//*[@id='menu_list']/li[10]/a").click()
    def fixalert(i):
        """
        弹框有好几种。
        i=0 提示账套尚未创建的对话框。只有一个“确定”按钮
        i=1 开启进销存时，弹出的提示进销存信息的提示框
        i=2 提交账套时，提示不能修改数据的提示框
        :return:
        """
        if i==0:
            dr.find_element_by_xpath("//*[@id='layui-layer3']/div[2]/a").click()
    def ztaddpage(self):
        # 定位
        ztname=dr.find_element_by_xpath("//*[@id='name']")
        zhidu=dr.find_element_by_xpath("//*[@id='accountSystemId']")
        hangye=dr.find_element_by_xpath("//*[@id='select2-industry-container']")   # 只是行业元素的定位，如果要设置行业，需要点击选择
        zsfs=dr.find_element_by_xpath("//*[@id='levyMode']")
        qydata=dr.find_element_by_xpath("//*[@id='startAccountPeriod']")
        nsrtype=dr.find_element_by_xpath("//*[@id='accountType']")
        # 本位币默认人民币，不设置
        hdl=dr.find_element_by_xpath("//*[@id='approvedRate']")
        jxcqy=dr.find_element_by_xpath("//*[@id='invoicingStartAccountperiod']")

