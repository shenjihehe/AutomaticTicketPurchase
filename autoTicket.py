# -*- coding: utf-8 -*-
# @Author: pc
# @Date:   2018-01-05 10:45:55
# @Last Modified by:   hwijew
# @Last Modified time: 2019-01-15 17:54:06
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import time

# 用户名，密码
username = '317620333@qq.com'
password = 'zj152232'

# 出发地，目的地
# fromstation = '厦门'
fromstation = '莆田'
tostation = '秦皇岛'

# 车次，选择第几趟，0则从上往下依次点击
order = 1

# 乘客名
users = ['林淑莺', '林天奇']
# users = ['林天奇']

# 出发日
train_date = "2019-02-16"

# 查询间隔时间
next_time = 0.1

# 网址
# ticket_url = "https://kyfw.12306.cn/otn/leftTicket/init"
ticket_url = "https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc"
login_url = "https://kyfw.12306.cn/otn/login/init"
# initmy_url = "https://kyfw.12306.cn/otn/index/initMy12306"
initmy_url = "https://kyfw.12306.cn/otn/view/index.html"
buy_url="https://kyfw.12306.cn/otn/confirmPassenger/initDc"

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
		continue
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
# # 去除readonly属性，直接输入日期
js = "var setDate=document.getElementById('train_date');setDate.removeAttribute('readonly');"
driver.execute_script(js)
driver.find_element_by_id("train_date").clear()
driver.find_element_by_id("train_date").send_keys(train_date)		# 出发日

count = 0
if order != 0:
	while driver.current_url == ticket_url:
		driver.find_element_by_id("query_ticket").click()
		count += 1
		print("循环点击查询... 第 %s 次" % count)

		order_obj = driver.find_elements_by_class_name('no-br')[order - 1]
		if order_obj.text == '预订':
			try:
				order_obj.click()
			except Exception as e:
				print(e)
			time.sleep(0.5)
		else:
			# next_time = 3
			print('还没开始预订，等待 %d 秒后再次查询！\n' % next_time)
			time.sleep(next_time)

else:
	while driver.current_url == ticket_url:
		driver.find_element_by_id("query_ticket").click()
		count += 1
		print("循环点击查询... 第 %s 次" % count)
		# try:
		# 	n = 0
		# 	for i in driver.find_elements_by_class_name("no-br"):
		# 		i.click()
		# 		print("	点击预定... 第 %s 车次" % n)
		# 		n += 1
		# 		time.sleep(0.5)
		# except Exception as e:
		# 	print(e)
		# 	print("还没开始预定")
		# 	time.sleep(4)
		order_objs = driver.find_elements_by_class_name('no-br')
		if order_objs[order].text == '预订':
			for order_obj in order_objs:
				order_obj.click()
				order += 1
				print("	点击预订... 第 %d 车次" % order)
		else:
			print('还没开始预订，等待 %d 秒后再次查询！\n' % next_time)
			time.sleep(next_time)

print("开始预定...")
print("开始选择用户...")

userinfos = driver.find_elements_by_css_selector("#normal_passenger_id label")
# userinfo_list = []
# for userinfo in userinfos:
# 	userinfo_list.append(userinfo.text)
# print(userinfo_list)
# for user in users:      # 选择乘客

for user in users:		# 选择乘客
	for userinfo in userinfos:
		if userinfo.text == user:
			userinfo.click()
			break

# 选择席别	
# 商务座(9),特等座(P),一等座(M),二等座(O),高级软卧(6),软卧(4),硬卧(3),软座(2),硬座(1),无座(1)
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

			print("提交订单...")
			driver.find_element_by_id("submitOrder_id").click()

			print("确认选座...")
			WebDriverWait(driver, 5, 1).until(EC.visibility_of_element_located((By.ID, "qr_submit_id"))).click()
		elif '4' in value_list:
			print("硬卧无票，改选择软卧！")
			Select(sel).select_by_value('4')  # 软卧

			print("提交订单...")
			driver.find_element_by_id("submitOrder_id").click()

			print("确认选座...")
			WebDriverWait(driver, 5, 1).until(EC.visibility_of_element_located((By.ID, "qr_submit_id"))).click()
		else:
			print("硬卧 软卧无票，抢下一波的吧！！！")
