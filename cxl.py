import requests,time,os,sys
#import zipfile36 as zipfile
#from shutil import copyfile
print('weather-helper（天气助手）\nby 陈鑫磊')
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

def if_getToday(city1):
    if pzwj.split('\n')[1] == 'xx区' or pzwj.split('\n')[1] == '':
        #获取ip
        url = 'https://api.live.bilibili.com/client/v1/Ip/getInfoNew'
        response = requests.get(url)
        ipDict = response.json()
        print(ipDict)
        if ipDict['code'] == 0:
            ip=ipDict['data']['addr']
            print('你的ip为:'+ip)
            #拼接地址
            add = ipDict['data']['country']+ipDict['data']['province']+ipDict['data']['city']+ipDict['data']['isp']
            print('欢迎'+add+'用户')
            city1 = ipDict['data']['city']
        
    if pzwj.split('\n')[6] == '1' or pzwj.split('\n')[6] == 1:
        getToday(city1)
    else:
        getToday2(city1)

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
        
#定义高德地图天气api
def getToday2(cityName):
    global data,watherdata
    #获取ip
    url = 'https://api.live.bilibili.com/client/v1/Ip/getInfoNew'
    response = requests.get(url)
    ipDict = response.json()
    print(ipDict)
    if ipDict['code'] == 0:
        ip=ipDict['data']['addr']
        print('你的ip为:'+ip)
        #拼接地址
        add = ipDict['data']['country']+ipDict['data']['province']+ipDict['data']['city']+ipDict['data']['isp']
        print('欢迎'+add+'用户')
        #返回高德地图城市编码
        if cityName == '' or cityName == 'xx区':
            url='https://restapi.amap.com/v3/ip?key=17f5a20a3538770bb35d639d0353787e&ip='+ip
            response = requests.get(url)
            cityDict = response.json()
            print(cityDict)
        else:
            url='https://restapi.amap.com/v3/place/text?key=17f5a20a3538770bb35d639d0353787e&citylimit=true&city='+cityName
            response = requests.get(url)
            cityDict = response.json()
            print(cityDict)
        if cityDict['status'] == 0:
            code=cityDict['adcode']
            print('城市编码请求成功，编码为：'+code)
            url = 'https://restapi.amap.com/v3/weather/weatherInfo?key=17f5a20a3538770bb35d639d0353787e&city='+code
            response = requests.get(url)
            weatherDict = response.json()
            print(weatherDict)
            if weatherDict['status'] == 1:
                #实况天气数据信息
                lives=watherDict['lives']
                #当前时间
                month = time.strftime('%m')
                date = month + '月' + forecast[0]['date']
                #城市名
                city=ipDict['data']['city']
                #天气
                wather=lives['weather']
                #实时气温
                wendu=lives['temperature']
                #风向
                fx=lives['temperature']
                #风力
                windpower=lives['windpower']
                #湿度
                sd=lives['humidity']
                #数据发布时间
                end_time=lives['reporttime']
                watherdata=date+ctiy+'天气\n现在'+wather+'\n'+'当前'+wendo+'\n'+fx+windpower+'\n湿度'+sd+'\n数据截止之'+end_time
            else:
                print('天气获取失败')
        else:
            print('ip获取失败')

def postdata():
    #getToday(city1)
    if_getToday(city1)
    global data
    if int(xzqdapi) == 1:
        url1 = 'https://api.uixsj.cn/hitokoto/get?type=hitokoto&code=json'
        apiget = requests.get(url1)
        apidata = apiget.json()
        print(apidata)
        content=apidata["type"]+"："+apidata['content']
    else:
        url1 = 'https://v1.hitokoto.cn/?encode=text'
        apiget = requests.get(url1)
        apidata = apiget.text
        content='一言：'+str(apidata)
        print(content)
    if pzwj.split('\n')[6] == 1 or pzwj.split('\n')[6] == '1':
        data={'msg':date+"\n"+city+"当前温度为："+wendu+"\n"+"当前天气:"+type+"\n"+fx+"\n"+"最"+high+"\n"+"最"+low+"\n"+ganmao+"\n"+content,
              'qq':qq}
    else:
        data={'msg':watherdata,'qq':qq}
    print('发送预览：'+'\n'+data['msg'])

def gongao():
    gongaokg=pzwj.split('\n')[4]
    if gongaokg == ("y" or "Y" or "yes"):
        #url = 'https://cxl2020mc.github.io/tp/公告.txt'
        url = 'https://cxl2020mc.vercel.app/tp/公告.txt'
        gongaoresponse = requests.get(url)
        if gongaoresponse.status_code == requests.codes.ok:
            gongao = gongaoresponse.text
            print("公告："+"\n"+gongao+"\n") 
        else:
            print("暂未设置公告")
    else:
        print('您未开启公告')  

def update():
    if pzwj.split('\n')[5] == ("y" or "Y" or "yes"):
        global version,update
        #url = 'https://cxl2020mc.github.io/tp/update.txt'
        url = 'https://cxl2020mc.vercel.app/tp/update.txt'
        updateresponse = requests.get(url)
        if updateresponse.status_code == requests.codes.ok:
            
            update = updateresponse.text
            #当前版本
            version = "v7.0"
            update = update.replace(' ', '').replace('\n', '')
            #比对版本号
            if version != update:
                installation()
                #退出程序
                exit()
            else:
                print("您使用的是最新版本")
        else:
            print("自动更新出现问题，请及时成功查看是否有更新，响应代码为："+updateresponse.status_code)
    else:
        print('您未开启更新')


def installation():
    print("当前版本"+version+"，"+"最新版本"+update+"，需要更新")
    #打印手动更新链接
    print("gitee手动更新链接：https://gitee.com/cxl2020/weather-helper/repository/archive/master.zip")
    a=input("是否更新（是y，否n）:")
    if a == 'y' or a == 'Y':
        #下载更新
        print("下载更新中......")
        start = time.time()
        url = 'https://github.com/cxl2020MC/weather-helper-update/archive/master.zip' 
        r = requests.get(url)
        with open("update.zip","wb")as code:
            code.write(r.content)
        end = time.time()
        print("下载总耗时:"+str(end-start)+"秒")
        #打印下载完成信息
        print("下载成功，正在解压......")
        zip_file = zipfile.ZipFile(r'.\update.zip')
        # 解压
        zip_extract = zip_file.extractall(r".\update")
        #zip_extract.close()
        #zip_file.getinfo(".\update\")
        zip_file.close()
        print("解压成功")
        #删除不必要文件
        os.remove(r".\update\weather-helper-update-master\git.sh")
        os.remove("update.zip")
        os.remove(r".\update\weather-helper-update-master\配置文件.txt")
        #打开自动更新文件
        os.system("start 自动更新.bat")
        print("正在启动复制文件脚本，本程序将在5秒后关闭")
        time.sleep(5)
    else:
        print('手动更新gitee地址：https://gitee.com/cxl2020/weather-helper/repository/archive/master.zip'+'/n'+"手动更新github下载地址https://github.com/cxl2020MC/weather-helper-update/archive/master.zip")
    


gongao()
postdata()
url='https://qmsg.zendee.cn/send/'+apikey
print("请核对请求链接："+url)
r=requests.post(url,data=data)
#print(r.text)
QmsgData=r.json()
print(QmsgData)
if QmsgData["success"] == True:
    print(QmsgData["reason"])
else:
    print("操作失败，原因："+QmsgData["reason"])
update()
