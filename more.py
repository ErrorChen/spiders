# _*_ coding : UTF-8 _*_
# 开发团队 : cooding
# 开发人员 : 小陈
# 开发时间 : 2020/11/9 17:15
# 文件名称 : more.py
# 开发工具 : PyCharm

def change(x):  #BV号转AV号
    tr = {}
    table = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
    s = [11, 10, 3, 8, 4, 6]
    xor = 177451812
    add = 8728348608
    r = 0
    for i in range(58):
        tr[table[i]] = i
    for i in range(6):
    	r+=tr[x[s[i]]]*58**i
    return (r-add)^xor

def download(url):#下载。type为视频清晰类型
    import os
    import sys
    import you_get
    adress = os.getcwd()
    directory = str(adress)+'\\download'  # 设置下载目录
    print(url)
    print(directory)
    sys.argv = ['you-get', '--playlist','-i', '-o', directory, url]
    you_get.main()
    try:
        sys.argv = ['you-get','--format=dash-flv', '--playlist','-o', directory, url]
        you_get.main()
    except:
        try:
            sys.argv=['you-get','--format=dash-flv720', '--playlist','-o', directory, url]
            you_get.main()
        except:
            try:
                sys.argv = ['you-get', '--format=dash-flv360', '--playlist', '-o', directory, url]
                you_get.main()
            except:
                sys.argv = ['you-get', '--playlist', '-o', directory, url]
                you_get.main()
    print('finish download :',url)

print('-'*20+'program start'+'-'*20)
import getpass
user_name = getpass.getuser() #获取计算机用户名
print('you should put all\"bv_code\"on',r'C:\Users\\' + user_name + '\Desktop\down.txt')

avcode=[] # 将读取到的每行数据保存
filename=r'C:\Users\\' + user_name + '\Desktop\down.txt'
with open(filename) as read_file:
    for line in read_file:
        avcode.append(change(line.rstrip()))
n=0
c=len(avcode)
print('program will print these videos:',avcode,'total:',c,'videos')
print('-'*20+'Now start downloading'+'-'*20)

while n<c:
    a='av'+str(avcode[n])
    number = n + 1
    print('NO.' + str(number) + ':',a)
    url = 'https://www.bilibili.com/video/'+a      #需要下载的视频地址
    download(url)
    n=n+1
print('both all were download,you can find it on '+r'C:\Users\\' + user_name + '\Desktop\Bili'  )
