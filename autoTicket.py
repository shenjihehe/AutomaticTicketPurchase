# -*- coding: utf-8 -*-
# @Author: pc
# @Date:   2018-01-05 10:45:55
# @Last Modified by:   pc
# @Last Modified time: 2018-01-25 11:22:04
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import time

# 用户名，密码
username = '******@qq.com'
password = '******'

# 出发地，目的地
fromstation = '莆田'
tostation = '秦皇岛'

# 车次，选择第几趟，0则从上往下依次点击
order = 1

# 乘客名
users = ['乘客1', '乘客2']

# 网址
ticket_url = "https://kyfw.12306.cn/otn/leftTicket/init"
login_url = "https://kyfw.12306.cn/otn/login/init"
initmy_url = "https://kyfw.12306.cn/otn/index/initMy12306"
buy_url="https://kyfw.12306.cn/otn/confirmPassenger/initDc"
login_url='https://kyfw.12306.cn/otn/login/init'

driver = webdriver.Chrome()
driver.get(login_url)
driver.implicitly_wait(10)
driver.maximize_window()
driver.find_element_by_id("username").clear()
driver.find_element_by_id("username").send_keys(username)
driver.find_element_by_id("password").clear()
driver.find_element_by_id("password").send_keys(password)
print('等待验证码，自行输入...')
while True:
	if driver.current_url != initmy_url:
		time.sleep(1)
	else:
		break
print("登录成功")
# 进入购票页面
driver.get(ticket_url)
print("购票页面开始...")
# 加载查询信息
driver.find_element_by_id('fromStationText').clear()
driver.find_element_by_id('fromStationText').click()
driver.find_element_by_id('fromStationText').send_keys(fromstation, Keys.ENTER)
driver.find_element_by_id('toStationText').clear()
driver.find_element_by_id('toStationText').click()
driver.find_element_by_id('toStationText').send_keys(tostation, Keys.ENTER)
# 选择出发日
# driver.find_element_by_id('train_date').click()
# dtimes = driver.find_elements_by_css_selector('div.cal-right div.so')		# 下月
# # dtimes = driver.find_elements_by_css_selector('div.cal div.so')		# 本月
# for dtime in dtimes:
# 	if dtime.text == '20':	# 出发日
# 		dtime.click()

# # 去除readonly属性，直接输入日期
js = "var setDate=document.getElementById('train_date');setDate.removeAttribute('readonly');"
driver.execute_script(js)
driver.find_element_by_id("train_date").clear()
driver.find_element_by_id("train_date").send_keys("2018-02-24")		# 出发日

count = 0
if order != 0:
	while driver.current_url == ticket_url:
		driver.find_element_by_id("query_ticket").click()
		count += 1
		print("循环点击查询... 第 %s 次" % count)
		# time.sleep(3)

		try:
			driver.find_elements_by_class_name("no-br")[order - 1].click()
			time.sleep(0.5)
		except Exception as e:
			print(e)
			print("还没开始预定")
			time.sleep(3)
else:
	while driver.current_url == ticket_url:
		driver.find_element_by_id("query_ticket").click()
		count += 1
		print("循环点击查询... 第 %s 次" % count)
		# time.sleep(3)
		try:
			n = 0
			for i in driver.find_elements_by_class_name("no-br"):
				i.click()
				print("	点击预定... 第 %s 车次" % n)
				n += 1
				time.sleep(0.5)
		except Exception as e:
			print(e)
			print("还没开始预定")
			time.sleep(3)
		# continue
print("开始预定...")
print("开始选择用户...")
userinfos = driver.find_elements_by_css_selector("#normal_passenger_id label")
for user in users:		# 选择乘客
	for userinfo in userinfos:
		if userinfo.text == user:
			userinfo.click()

# 选择席别	硬卧=3  软卧=4  硬座=1  一等座=M  二等座=O
ticketnumber = number = 0
for ticketinfo in driver.find_elements_by_css_selector("tbody#ticketInfo_id select"):
	ticketnumber += 1
	if ticketnumber % 3 == 1:		# 每一行有三个select
		number += 1
		sel = driver.find_element_by_css_selector("select#seatType_%d" % number)

		value_list = []
		option_list = driver.find_elements_by_css_selector("select#seatType_%d option" % number)
		for option_text in option_list:
			value_list.append(option_text.get_attribute("value"))
		if '3' in value_list:
			print("选择硬卧...")
			Select(sel).select_by_value('3')  # 硬卧
		else:
			if '1' in value_list:
				print("硬卧无票，改选择硬座！")
				Select(sel).select_by_value('1')  # 硬座
			else:
				pass

print("提交订单...")
driver.find_element_by_id("submitOrder_id").click()

print("确认选座...")
WebDriverWait(driver, 3, 0.5).until(EC.visibility_of_element_located((By.ID, "qr_submit_id"))).click()
