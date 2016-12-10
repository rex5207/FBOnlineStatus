import time
from util import setting
from util import creatFile
from web import restAPI
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from pyvirtualdisplay import Display

#store for user and count

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

online_info = dict()
daily_friend = dict()
online_count = [None]*1440
display = Display(visible=0, size=(800, 600))
display.start()
driver = webdriver.Chrome("./chromedriver")
file_name_week = ""
file_name_year = ""
file_name_month = ""
file_name_day = ""


def read_onlineInfo():
    global online_info
    global file_name_year
    global file_name_month
    global file_name_day
    online_info = dict()
    localtime = time.localtime(time.time())
    year = (str)(localtime.tm_year)
    month = (str)(localtime.tm_mon).zfill(2)
    day = (str)(localtime.tm_mday).zfill(2)
    file_name_year = year
    file_name_month = month
    file_name_day = day
    #check the file is exist or not
    creatFile.creat_onlineInfo(year,month,day)
    #read the file
    f = open("./data/onlineInfo/"+year+month+day, 'r')
    for line in f.readlines():
        userInfo = line.split()
        userID = userInfo[0]
        del userInfo[0]
        online_info[userID] = userInfo
    f.close

def write_onlineInfo(year,month,day):
    #update the file
    f = open("./data/onlineInfo/"+year+month+day, 'w')
    for key, value in online_info.items():
        f.write(key)
        for detailtime in value:
            f.write(" "+str(detailtime))
        f.write("\n")
    f.close

def read_onlineCount():
    global online_count
    global file_name_week
    online_count = [None]*1440
    localtime = time.localtime(time.time())
    week = (str)(localtime.tm_wday)
    file_name_week = week
    #check the file is exist or not
    creatFile.creat_onlineCount(week)
    #read the file
    f = open("./data/totalCount/"+week, 'r')
    file_name_now = week
    online_count = f.readlines()
    f.close

def write_onlineCount(week):
    #update the file
    f = open("./data/totalCount/"+week, 'w')
    f.writelines(online_count)
    f.close

def read_dailyfriend():
    global daily_friend
    global file_name_year
    global file_name_month
    global file_name_day
    daily_friend = dict()
    localtime = time.localtime(time.time())
    year = (str)(localtime.tm_year)
    month = (str)(localtime.tm_mon).zfill(2)
    day = (str)(localtime.tm_mday).zfill(2)
    #check the file is exist or not
    creatFile.creat_dailyFriend(year,month,day)
    #read the file
    f = open("./data/dailyFriend/"+year+month+day, 'r')
    for line in f.readlines():
        userInfo = line.split()
        userID = userInfo[0]
        userName = userInfo[1]
        daily_friend[userID] = userName
    f.close

def write_dailyfriend(year,month,day):
    #update the file
    f = open("./data/dailyFriend/"+year+month+day, 'w')
    for key, value in daily_friend.items():
        f.write(key + " " + value+ "\n")
    f.close

def login_with_driver():
    global driver
    driver.get('https://www.facebook.com/?locale=zh_TW')
    username = setting.account #change here
    password = setting.password #change here
    usr = driver.find_element_by_xpath("//*[@id='email']")
    passw = driver.find_element_by_xpath("//*[@id='pass']")
    logbtn = driver.find_element_by_xpath("//*[@id='u_0_l']")
    usr.send_keys(username)
    passw.send_keys(password)
    logbtn.click()

def run_app():
    restAPI.app.run(host='0.0.0.0',theaded=True)


if __name__ == "__main__":

    # restAPI.app.run(debug=True)
    # restAPI.app.run(threaded=True)
    # p = multiprocessing.Process(target=run_app())
    # p.start()


    print "Read the former file"
    read_onlineInfo()
    read_onlineCount()
    read_dailyfriend()

    print("Login Start ...")
    login_with_driver()


    while True:
        print("=====Refreshing!====")
        driver.get('https://www.facebook.com/me')
        time.sleep(50)
        print("After Waiting")
        soup = BeautifulSoup(driver.page_source, "html.parser")
        div_lotstars = soup.find_all('li', {'class': '_42fz'})
        print("Store the output.")
        localtime = time.localtime(time.time())
        year_now = (str)(localtime.tm_year)
        month_now = (str)(localtime.tm_mon).zfill(2)
        day_now = (str)(localtime.tm_mday).zfill(2)
        week_now = (str)(localtime.tm_wday)
        hour_now = (int)(localtime.tm_hour)
        min_now = (int)(localtime.tm_min)
        if (file_name_week != week_now):
            write_onlineCount(file_name_week)
            write_onlineInfo(file_name_year,file_name_month,file_name_day)
            write_dailyfriend(file_name_year,file_name_month,file_name_day)
            read_onlineCount()
            read_onlineInfo()
            read_dailyfriend()
        now_count=0
        for friend_list in div_lotstars:
            #online(_568-) and not group(_55ls)
            temp = friend_list.find('div', {'class': '_568z'})
            if temp is not None and temp.find('span') is not None and friend_list.find('div', {'class': '_55ls'}).get_text() == "":
                #name(_55lr)
                # print friend_list.find('div', {'class': '_55lr'}).get_text().encode('utf-8')
                #user(id)
                # print friend_list['data-id']
                daily_friend[friend_list['data-id']] = friend_list.find('div', {'class': '_55lr'}).get_text()
                if friend_list['data-id'] not in online_info:
                    online_info[friend_list['data-id']] = [hour_now*60+min_now]
                else:
                    (online_info[friend_list['data-id']]).append(hour_now*60+min_now)
                now_count = now_count+1
        online_count[hour_now*60 + min_now] = online_count[hour_now*60 + min_now][:-1] + " "+str(now_count)+'\n'

        if(int(min_now)%10 == 0):
            write_onlineInfo(year_now,month_now,day_now)
            write_dailyfriend(year_now,month_now,day_now)
            write_onlineCount(week_now)
    driver.close()
