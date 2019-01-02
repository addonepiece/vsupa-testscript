#此段脚本实现如下功能：登录系统，点击财税托管进入购买页面，
#判断纳税人类型，如果是小规模的选一般，如果是一般，选小规模
#提交订单，如果有弹出框（提示纳税人类型与之前不一致），点关闭
#提交订单

#coding=utf-8
import sys
from selenium import webdriver
from time import*
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


driver=webdriver.Chrome()
#跳转到云算盘
driver.get("http://test.vsupa.com/homepage/login.html")
print("打开云算盘")
driver.maximize_window()
#登录系统
driver.find_element_by_id("loginName").send_keys("cybtest")


sleep(2)



password=driver.find_element_by_id("password")
password.send_keys("123456")


driver.find_element_by_id("loginBtn").click()
print("登录成功")

sleep(10)
#购买财税托管
tt=driver.find_element_by_id("service")
tt02=tt.find_element_by_xpath("//div[@data-index='0']")


tt03=tt02.find_element_by_xpath("//li[@data-intro-url='/homepage/product/account.html?id=account_agency']")

ActionChains(driver).move_to_element(tt03).perform()
sleep(3)
tt03.find_element_by_xpath("//a[@href='/homepage/purchase/buy-account.html']").click()
print("进入购买财税托管页面")
sleep(6)

#跳转页面后要重新定位
driver.switch_to_window(driver.window_handles[1])

#判断纳税人类型，如果原来是小规模，购买一般，如果是一般，购买小规模
xiao=driver.find_element_by_xpath("//li[@value='account_agency_01']")
yiban=driver.find_element_by_xpath("//li[@value='account_agency_02']")
dd=xiao.get_attribute("class")
if dd =='active':
    yiban.click()
else:
    xiao.click()



#提交订单
driver.find_element_by_id("submitOrder").click()
#操作弹出框
#判断是否弹出框

driver.switch_to_window(driver.window_handles[1])
#判断框是否存在
if driver.find_element_by_xpath("//a[@class='cancel-btn']"):
    sleep(2)
    driver.find_element_by_xpath("//a[@class='confirm-btn']").click()
else:
    print("无")



print("提交订单")
