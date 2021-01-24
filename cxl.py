import requests,time,os,sys
import zipfile36 as zipfile
from shutil import copyfile

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
        url1 = 'https://v1.hitokoto.cn/?encode=text'
        apiget = requests.get(url1)
        apidata = apiget.text
        content='一言：'+str(apidata)
        print(content)

    data={'msg':date+"\n"+city+"当前温度为："+wendu+"\n"+"当前天气:"+type+"\n"+fx+"\n"+"最"+high+"\n"+"最"+low+"\n"+ganmao+"\n"+content,
           'qq':qq}
    print('发送预览：'+'\n'+data['msg'])

def gongao():
    gongaokg=pzwj.split('\n')[4]
    if gongaokg == ("y" or "Y" or "yes"):
        url = 'https://cxl2020mc.github.io/tp/公告.txt'
        gongaoresponse = requests.get(url)
        gongao = gongaoresponse.text
        print("公告："+"\n"+gongao+"\n") 
    else:
        print('您未开启公告')  

def update():
    if pzwj.split('\n')[5] == ("y" or "Y" or "yes"):
        global version,update
        url = 'https://cxl2020mc.github.io/tp/update.txt'
        updateresponse = requests.get(url)
        update = updateresponse.text
        
        #updateText = update.replace('v', '').replace('V', '')
        #当前版本
        version = "v5.0"
        update = update.replace(' ', '').replace('\n', '')
        #去除v和V
        #version = version.replace('v', '').replace('V', '')
        #version1 = int(version.replace('.0', ''))
        #updateText1 = int(updateText.replace('.0', ''))
        if version != update:
            installation()
            exit()
        else:
            print("您使用的是最新版本")
    else:
        print('您未开启更新')

#以下来自网络
#############################################################################################################################
# 这个程序的作用：
# 可以将A目录下的所有文件以及A目录下的文件夹中的文件复制到另外一个目录B里并且保留所有目录结构
# 这个程序的作用等同于windows下直接将一个文件夹复制到另一个文件夹中（windows的复制也是保留目录结构的）
# 但是不同点是：这个程序复制出的所有文件以及文件夹他们的修改日期、访问日期都是当前系统时间
#               而windows系统的复制之后的文件的修改日期、访问日期都和复制前的时间一样
# 目的：我需要修改一个工程内所有代码文件的创建日期，发现直接在windows下复制实现不了，于是用代码试了试，下面是我
#       实现的python代码（如果文件不多的话，要实现该功能也可以用下面的方法：打开文件，然后随便编辑一个
#       文字->保存->删除刚才编辑的文字->保存。这样做之后修改日期会改为当前时间，创建时间依然不变。）
#import os
#from shutil import copyfile  # 复制一个文件到另一个文件夹下    copyfile(src,dst)
# 递归函数
def copy_file(path_read, path_write):
    # 将number设置为全局变量
    global number
    # 输出path_read目录下的所有文件包括文件夹的名称
    names = os.listdir(path_read)
    # 循环遍历所有的文件或文件夹
    for name in names:
        # 定义新的读入路径（就是在原来目录下拼接上文件名）
        path_read_new = path_read + "\\" + name
        # 定义新的写入路径（就是在原来目录下拼接上文件名）
        path_write_new = path_write + "\\" + name
        # 判断该读入路径是否是文件夹，如果是文件夹则执行递归，如果是文件则执行复制操作
        if os.path.isdir(path_read_new):
            # 判断写入路径中是否存在该文件夹，如果不存在就创建该文件夹
            if not os.path.exists(path_write_new):
                # 创建要写入的文件夹
                os.mkdir(path_write_new)
            # 执行递归函数，将文件夹中的文件复制到新创建的文件夹中（保留原始目录结构）
            copy_file(path_read_new, path_write_new)
        else:
            # 每复制一次，number+1
            number += 1
            # 将文件path_read_new复制到path_write_new
            copyfile(path_read_new, path_write_new)


#if __name__ == "__main__":
    # 定义一个变量，用来记录一共进行了多少次复制（也就是一共有多少个文件）
#    number = 0
    # 从该文件夹中复制出来
#    path_read = '.\\update\\weather-helper-update-master'
    # 复制到该文件夹
#    path_write = "."
    # 执行递归函数
#    copy_file(path_read, path_write)
    # 输出一共有多少个文件
#    print(number)

##############################################################################################################################
def installation():
    print("当前版本"+version+"，"+"最新版本"+update+"，需要更新")
    #os.system("update.exe")
    #if int(len(update.split('\n'))) > 1:
    #    for i in update.split('\n'):
    #        print(i)
    #下载更新
    print("下载更新中......")
    start = time.time()
    url = 'https://github.com/cxl2020MC/weather-helper-update/archive/master.zip' 
    r = requests.get(url)
    with open("update.zip","wb")as code:
        code.write(r.content)
    end = time.time()
    print("下载总耗时:"+str(end-start)+"秒")

    print("下载成功，正在解压......")
    zip_file = zipfile.ZipFile(r'.\update.zip')
    # 解压
    zip_extract = zip_file.extractall(r".\update")
    #zip_extract.close()
    #zip_file.getinfo(".\update\")
    zip_file.close()
    print("解压成功")
    print("由于打包EXE的技术问题，暂时不能自动更新，请打开天气助手所在目录下的update文件夹中的weather-helper-update-master文件夹手动复制文件到天气助手所在目录")
    #删除不必要文件
    os.remove(r".\update\weather-helper-update-master\git.sh")
    os.remove("update.zip")
    os.remove(r".\update\weather-helper-update-master\配置文件.txt")
    #测试自动更新代码    
    number = 0
    # 从该文件夹中复制出来
    path_read = '.\\update\\weather-helper-update-master'
    # 复制到该文件夹
    path_write = "."
    # 执行递归函数
    #copy_file(path_read, path_write)
    # 输出一共有多少个文件
    #print(number)
    


gongao()
postdata()
url='https://qmsg.zendee.cn/send/'+apikey
print(url)
r=requests.post(url,data=data)
print(r.text)
update()
