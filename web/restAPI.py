#!flask/bin/python
from flask import Flask
from flask import render_template
import os
import json
from webob import Response

app = Flask('testapp')

@app.route('/', methods=['GET'])
@app.route('/OnlineInfo', methods=['GET'])
def indexInfo():
    return render_template('OnlineInfo.html')

@app.route('/OnlineCount', methods=['GET'])
def indexCount():
    return render_template('OnlineCount.html')

#http://localhost:5000/api/v1.0/getCount/0
@app.route('/api/v1.0/getCount/<int:week>', methods=['GET'])
def get_online_count(week):
    online_count = [None]*1440
    #read the file
    if os.path.isfile("../data/totalCount/"+str(week)):
        f = open("../data/totalCount/"+str(week), 'r')
        online_count = f.readlines()
        f.close
    for i in range(len(online_count)):
        online_count[i] = online_count[i].strip("\n")
        temp = online_count[i].split()
        total_count = 0
        total_num = 0
        for online_num in temp:
            total_count += int(online_num)
            total_num += 1
        if total_num is not 0 :
            online_count[i] = str(total_count / total_num)
    body = json.dumps(online_count)
    return Response(content_type='application/json', body=body)


#http://localhost:5000/api/v1.0/getOnlineInfo/2016125
@app.route('/api/v1.0/getOnlineInfo/<string:date>', methods=['GET'])
def get_online_friend(date):
    dailyfriend = []
    if os.path.isfile("../data/dailyFriend/"+date) :
        f = open("../data/dailyFriend/"+date, 'r')
        for line in f.readlines():
            userInfo = line.split()
            dailyfriend.append({"userID" : userInfo[0] , "userName" : userInfo[1]})
        f.close
    body = json.dumps(dailyfriend)
    return Response(content_type='application/json', body=body)


#http://localhost:5000/api/v1.0/getOnlineInfo/2016125/100002030446619
@app.route('/api/v1.0/getOnlineInfo/<string:date>/<string:myuserID>', methods=['GET'])
def get_online_info(myuserID,date):
    onlinedata = ""
    if os.path.isfile("../data/onlineInfo/"+date) :
        f = open("../data/onlineInfo/"+date, 'r')
        for line in f.readlines():
            userInfo = line.split()
            userID = userInfo[0]
            if(userID == myuserID):
                del userInfo[0]
                onlinedata = {"userID" : userID , "online_data" : userInfo}
                break
        f.close
    body = json.dumps(onlinedata)
    return Response(content_type='application/json', body=body)

if __name__ == "__main__":
    app.run(host='0.0.0.0',threaded=True)
