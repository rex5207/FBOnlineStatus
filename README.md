# FBOnlineStatus
You can crawl your friends' online information without Graph API

#Requirement
Python

# Setup
1.Set your account/password in /util/setting.py  
2-a.(For Windows/MacOS/Ubuntu Deskop)Download [Chromedriver](https://chromedriver.storage.googleapis.com/index.html?path=2.26/) according to your OS and put it in root folder.

2-b.(Ubuntu Server), Using the following command.
```
sudo apt-get install chromium-chromedriver
sudo ln -s /usr/lib/chromium-browser/chromedriver /usr/bin/chromedriver
```

3.Install the Python library
```
sudo pip install selenium
sudo pip install bs4
sudo pip install pyvirtualdisplay
sudo pip install flask (Option! For Web)
sudo pip install webob (Option! For Web)

```
4.python main.py
5.python restAPI.py (Option! Run your Web)
6.Enjoy your crawling!
  

#Web UI
1.[localhost:5000/OnlineInfo](http:localhost:5000/OnlineInfo)
You can use Web to see your friends' online information.

2.[localhost:5000/OnlineCount](http:localhost:5000/OnlineCount)
You can use Web to see your friends' online amount.

#Restful API
1.[localhost:5000/api/v1.0/getCount/\<week>]()
Get the average number of your online frineds by 0~6(Mon~Sun).

2.[localhost:5000/api/v1.0/getOnlineInfo/\<date>]()
Get the list of your online frineds by date (ex.20161210).

3.[localhost:5000/api/v1.0/getOnlineInfo/\<date>/\<userID>]()
Get the information of your specific frineds by date (ex.20161210/10231233232).

