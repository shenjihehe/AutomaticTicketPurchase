
from configparser import ConfigParser

class AutomaticTicketPurchase(object):

    def __init__(self):
        # 读取配置文件
        self.cp = ConfigParser()
        self.cp.read('config.ini', encoding='UTF-8')
        self.username = self.cp.get('login', 'username')
        self.password = self.cp.get('login', 'password')
        self.fromStation = self.cp.get('queryInfo', 'fromStation')
        self.toStation = self.cp.get('queryInfo', 'toStation')
        self.train_date = self.cp.get('queryInfo', 'train_date')
        self.number = self.cp.get('trainNumber', 'number')

        # 初始化驱动、默认等待时间、浏览器大小等
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()


    def login(self):
        print("开始登录...")
        self.driver.get(login_url)
        self.driver.find_element_by_id("username").clear()
        self.driver.find_element_by_id("username").send_keys(username)
        self.driver.find_element_by_id("password").clear()
        self.driver.find_element_by_id("password").send_keys(password)
        print('等待自行输入验证码，并点击登录...')
        while True:
            if driver.current_url != initmy_url:
                continue
            else:
                break
        print("登录成功...")

    def queryInfo(self):
        # 输入查询信息
        self.driver.find_element_by_id('fromStationText').clear()
        self.driver.find_element_by_id('fromStationText').click()
        self.driver.find_element_by_id('fromStationText').send_keys(fromstation, Keys.ENTER)
        self.driver.find_element_by_id('toStationText').clear()
        self.driver.find_element_by_id('toStationText').click()
        self.driver.find_element_by_id('toStationText').send_keys(tostation, Keys.ENTER)
        # 选择出发日
        # 去除readonly属性，直接输入日期
        js = "var setDate=document.getElementById('train_date');setDate.removeAttribute('readonly');"
        self.driver.execute_script(js)
        self.driver.find_element_by_id("train_date").clear()
        self.driver.find_element_by_id("train_date").send_keys(train_date)  # 出发日

    def specifyTrain(self):
        # 指定车次
        count = 0
        if order != 0:
            while self.driver.current_url == ticket_url:
                self.driver.find_element_by_id("query_ticket").click()
                count += 1
                print("循环点击查询... 第 %s 次" % count)

                order_obj = self.driver.find_elements_by_class_name('no-br')[order - 1]
                if order_obj.text == '预订':
                    try:
                        order_obj.click()
                    except Exception as e:
                        print(e)
                    time.sleep(0.2)
                else:
                    # next_time = 3
                    print('还没开始预订，等待 %d 秒后再次查询！\n' % next_time)
                    time.sleep(next_time)

        else:
            while self.driver.current_url == ticket_url:
                self.driver.find_element_by_id("query_ticket").click()
                count += 1
                print("循环点击查询... 第 %s 次" % count)
                # try:
                # 	n = 0
                # 	for i in self.driver.find_elements_by_class_name("no-br"):
                # 		i.click()
                # 		print("	点击预定... 第 %s 车次" % n)
                # 		n += 1
                # 		time.sleep(0.5)
                # except Exception as e:
                # 	print(e)
                # 	print("还没开始预定")
                # 	time.sleep(4)
                order_objs = self.driver.find_elements_by_class_name('no-br')
                if order_objs[order].text == '预订':
                    for order_obj in order_objs:
                        order_obj.click()
                        order += 1
                        print("	点击预订... 第 %d 车次" % order)
                else:
                    print('还没开始预订，等待 %d 秒后再次查询！\n' % next_time)
                    time.sleep(next_time)

    def selUser(self):
        userinfos = self.driver.find_elements_by_css_selector("#normal_passenger_id label")
        for user in users:  # 选择乘客
            for userinfo in userinfos:
                if userinfo.text == user:
                    userinfo.click()
                    break