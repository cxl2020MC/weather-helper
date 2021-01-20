import requests,time

with open('配置文件.txt','r',encoding="utf-8") as f:
   pzwj=f.read()  #文件的读操作
#pzwj=pzwj.replace('\n', '').replace('\r', '')
pzwj=pzwj.replace(' ', '')
qq=pzwj.split('\n')[2]
#print(qq)
city1=pzwj.split('\n')[1]
#print(city1)
apikey=pzwj.split('\n')[0]
#print(apikey)
xzqdapi=pzwj.split('\n')[3]
print('qq:'+qq+','+'city:'+city1+','+'apikey:'+apikey+'你选择的api序号：'+xzqdapi)
def getData(cityName):
    getToday(cityName)
    # 获取未来天气信息
    global dates,types,highs,lows
    dates = []
    types = []
    highs = []
    lows = []
    for info in forecast:
        dates.append(month + '月' + info['date'])
        types.append(info['type'])
        highs.append(info['high'])
        lows.append(info['low'])
def getToday(cityName):
    url = 'http://wthrcdn.etouch.cn/weather_mini?city=' + cityName
    response = requests.get(url)
    weatherDict = response.json()
    print(weatherDict)
    if weatherDict['desc'] == 'OK':
        print('你输入的城市是正确的')
        # 获取城市名
        global city, wendu,month,forecast,fx,ganmao,fl
        city = weatherDict['data']['city']
        print('城市名称', city)
        # 获取当前温度
        wendu = weatherDict['data']['wendu'] + '℃ '
        # 获取月份
        month = time.strftime('%m')
        #print(month)
        forecast = weatherDict['data']['forecast']
        # 获取日期
        global date, type, high, low, data
        date = month + '月' + forecast[0]['date']
        # 获取天气类型
        type = forecast[0]['type']
        # 获取最高温度
        high = forecast[0]['high']
        # 获取最低温度
        low = forecast[0]['low']
        ganmao=weatherDict['data']['ganmao']
        # 获取风向(v2.0更新)和风力(v3.0更新)
        fl=weatherDict['data']['yesterday']['fl']
        fx=weatherDict['data']['yesterday']['fx']+fl.replace('<![CDATA[', '').replace(']]>', '')
    else:
        print('你输入的城市是错误的')

def postdata():
    getToday(city1)
    global data
    if int(xzqdapi) == 1:
        url1 = 'https://api.uixsj.cn/hitokoto/get?type=hitokoto&code=json'
        apiget = requests.get(url1)
        apidata = apiget.json()
        print(apidata)
        content=apidata["type"]+"："+apidata['content']
    else:
        url1 = 'https://v1.hitokoto.cn/?c=f&encode=text'
        apiget = requests.get(url1)
        apidata = apiget.text
        content='一言：'+str(apidata)
        print(content)

    data={'msg':date+"\n"+city+"当前温度为："+wendu+"\n"+"当前天气:"+type+"\n"+fx+"\n"+"最"+high+"\n"+"最"+low+"\n"+ganmao+"\n"+content,
           'qq':qq}
    print('发送预览：'+'\n'+data['msg'])

def gongao():
    gongaokg=pzwj.split('\n')[4]
    if gongaokg == "y":
        url2 = 'https://cxl2020mc.github.io/tp/公告.txt'
        gongaoresponse = requests.get(url2)
        gongao = gongaoresponse.text
        print("公告："+"\n"+gongao) 
    else:
        print('您未开启公告')  
gongao()
postdata()
url='https://qmsg.zendee.cn/send/'+apikey
print(url)
r=requests.post(url,data=data)
print(r.text)

