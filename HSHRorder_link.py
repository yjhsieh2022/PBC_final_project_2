# 一般訂票
from selenium import webdriver

# setting
StartStationName = '南港站'
EndStationName = '左營站'
DepartureSearchDate = '2020/01/08'
DepartueSearchTime = '18:30'
TrainNumber = '675'

# 用的是宜蓁電腦裡的路徑，如果要跑要確保有pip install selenium & download chromedriver(https://sites.google.com/a/chromium.org/chromedriver/downloads)
driver = webdriver.Chrome(executable_path = "C:/Users/宜蓁/Documents/大五/python/chromedriver_win32/chromedriver")
driver.get("https://irs.thsrc.com.tw/IMINT/")

# 點選個資使用同意
AgreeButton = driver.find_element_by_id("btn-confirm")
AgreeButton.click()

# 輸入起訖站, 訂位方式(直接輸入車次號碼), 日期, 車次號碼

# 起站 = 南港站，之後根據google map 爬出的資料輸入
startpoint = driver.find_element_by_name("selectStartStation")
startpoint.send_keys(StartStationName)
# 訖站 = 左營站，之後根據google map 爬出的資料輸入
destination = driver.find_element_by_name("selectDestinationStation")
destination.send_keys(EndStationName)
# 訂位方式: 兩個選項的name都是bookingMethod，所以用id = bookingMethod_0 or id = bookingMethod_1
how_to_order = driver.find_element_by_id("bookingMethod_1")
how_to_order.click()
# 日期
date = driver.find_element_by_name("toTimeInputField")
date.clear()
date.send_keys(DepartureSearchDate)
# 車次號碼
TrainNumber_input = driver.find_element_by_name("toTrainIDInputField")
TrainNumber_input.send_keys(TrainNumber)




