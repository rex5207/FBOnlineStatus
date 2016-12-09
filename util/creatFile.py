import os

def creat_onlineCount(week):
    if not os.path.isfile("./data/totalCount/"+week):
        f = open("./data/totalCount/"+week, 'w+')
        for i in range (24*60):
            f.write('\n')
        f.close
    else:
        f = open("./data/totalCount/"+week, 'r')
        num_lines = sum(1 for line in f)
        if(num_lines < 24*60):
            f = open("./data/totalCount/"+week, 'w')
            for i in range (24*60):
                f.write('\n')
        f.close


def creat_onlineInfo(year,month,day):
    if not os.path.isfile("./data/onlineInfo/"+year+month+day):
        f = open("./data/onlineInfo/"+year+month+day, 'w+')
        f.close


def creat_dailyFriend(year,month,day):
    if not os.path.isfile("./data/dailyFriend/"+year+month+day):
        f = open("./data/dailyFriend/"+year+month+day, 'w+')
        f.close
