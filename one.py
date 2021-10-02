# _*_ coding : UTF-8 _*_
# 开发团队 : cooding
# 开发人员 : 小陈
# 开发时间 : 2020/8/24 16:45
# 文件名称 : one.py
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

def choose(url): #分类处理（番剧与普通视频）
    import re
    try:
        modle_video = r'BV\w{10}'
        match = re.findall(modle_video, url, re.I)
        print(match)
        new=match[0]
        new_url='https://www.bilibili.com/video/av'+str(change(new))
    except:
        try:
            modle_video = r'ss\d{5}'
            match = re.findall(modle_video, url, re.I)
            new = match[0]
            new_url='https://www.bilibili.com/bangumi/play/'+new
        except:
            return url
    return new_url

def download(url):#下载。type为视频清晰类型
    import os
    import sys
    import you_get
    adress = os.getcwd()
    directory = str(adress)+'\\download'  # 设置下载目录
    print(url)
    print(directory)
    sys.argv = ['you-get', '--playlist','-o', directory, url]
    you_get.main()
    print('finish download :',url)

while 1:
    download(choose(input('url')))
