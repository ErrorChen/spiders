import json
import requests

class you_get_down:
    def change(x):  # BV号转AV号
        tr = {}
        table = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
        s = [11, 10, 3, 8, 4, 6]
        xor = 177451812
        add = 8728348608
        r = 0
        for i in range(58):
            tr[table[i]] = i
        for i in range(6):
            r += tr[x[s[i]]] * 58 ** i
        return (r - add) ^ xor

    def choose(url):  # 分类处理（番剧与普通视频）
        import re
        try:
            modle_video = r'BV\w{10}'
            match = re.findall(modle_video, url, re.I)
            print(match)
            new = match[0]
            new_url = 'https://www.bilibili.com/video/av' + str(new)
        except:
            try:
                modle_video = r'ss\d{5}'
                match = re.findall(modle_video, url, re.I)
                new = match[0]
                new_url = 'https://www.bilibili.com/bangumi/play/' + new
            except:
                return url
        return new_url

    def download(url,directory):  # 下载。type为视频清晰类型
        import sys
        import you_get
        print(url)
        print(directory)
        sys.argv = ['you-get', '--playlist', '-o', directory, url]
        you_get.main()
        print('finish download :', url)


class Channel_down:
    dict_bvID = {}
    list_cid = []

    def __init__(self, UA, up_id, path='/.'):
        self.up_id = up_id
        self.UA = UA
        self.path = path

        self.get_cid(self.UA, self.up_id)
        for i in self.list_cid:
            self.get_bvID(self.UA, self.up_id, i)

        # 把获取BV号存入本地磁盘，下次就不用重新爬获
        with open('Channel_BVid.json', 'w', encoding='utf-8') as fp:
            json.dump(self.dict_bvID, fp=fp, ensure_ascii=False)

        # 从本地json文件读取BV号
        # with open('Channel_BVid.json', 'r', encoding='utf-8') as fp:
        #     self.dict_bvID = json.load(fp)

        # 用you-get下载
        # 选择一个收藏夹
        Channel_name = input('\n选择一个分类或all\n')
        while (Channel_name not in self.dict_bvID.keys() and Channel_name != 'all'):
            Channel_name = input('\n选择一个分类或all\n')
        for key, value in self.dict_bvID.items():
            # 选择一个分类
            if key == Channel_name or Channel_name == 'all':
                print(key, value)
                num = 1
                for i in value:

                    try:
                        print('第' + str(num) + '/' + str(len(value)) + '个视频：' + i['title'])
                        you_url = 'https://www.bilibili.com/video/' + i['bvid']
                        # 视频输出的位置
                        path = self.path + key
                        you_get_down.download(you_url, path)
                        num += 1
                    except Exception as e:
                        print('异常：', e)
                        num += 1

    def get_cid(self, UA, up_id):
        header = {
            'user-agent': UA,
        }
        param = {
            'mid': up_id,
            'guest': 'false',
            'jsonp': 'jsonp',
            # 'callback': '__jp3'
        }
        url = 'https://api.bilibili.com/x/space/channel/list?'
        response = requests.get(url=url, headers=header, params=param,verify=False)
        dict_ = response.json()['data']
        list_ = response.json()['data']['list']
        for i in list_:
            d = {}
            d['cid'] = i['cid']
            d['name'] = i['name']
            d['count'] = i['count']
            self.list_cid.append(d)
        # print(dict_)
        # print(self.list_cid)

    def get_bvID(self, UA, up_id, cid_i):
        # global dict_bvID

        pn = 0
        pn += cid_i['count'] // 30
        if cid_i['count'] % 30 != 0:
            pn += 1
        cid = cid_i['cid']
        list_bvID = []
        url = 'https://api.bilibili.com/x/space/channel/video?'
        header = {
            'user-agent': UA,
        }
        for n in range(1, pn + 1):

            param = {
                'mid': up_id,
                'cid': cid,
                'pn': str(n),
                'ps': '30',
                'order': '0',
                'jsonp': 'jsonp',
                # 'callback': '__jp3'
            }

            response = requests.get(url=url, headers=header, params=param,verify=False)
            list_ = response.json()['data']['list']['archives']
            for i in list_:
                d = {}
                d['title'] = i['title']
                d['bvid'] = i['bvid']
                list_bvID.append(d)
        self.dict_bvID[cid_i['name']] = list_bvID
        print(cid_i['name'], len(list_bvID))
        # print(cid_i)
        # print(len(list_bvID))
        # print('\n')


class Classify_down:
    dict_bvID = {}
    dict_tid = {}

    def __init__(self, UA, up_id, path='./'):

        self.up_id = up_id
        self.tid = '0'
        self.UA = UA
        self.path = path

        if self.dict_tid == {}:
            self.get_dict_bvID(self.up_id, self.tid)
        print(self.dict_tid)
        for k, v in self.dict_tid.items():
            list_bv = self.get_dict_bvID(self.up_id, k, int(v['count']))
            print(self.dict_tid[k]['name'], len(list_bv))
            self.dict_bvID[self.dict_tid[k]['name']] = list_bv

        # 把获取BV号存入本地磁盘，下次就不用重新爬获
        with open('Classify_BVid.json', 'w', encoding='utf-8') as fp:
            json.dump(self.dict_bvID, fp=fp, ensure_ascii=False)

        # 从本地json文件读取BV号
        # with open('Classify_BVid.json', 'r', encoding='utf-8') as fp:
        #     self.dict_bvID = json.load(fp)

        # 用you-get下载
        # 选择一个收藏夹
        Classify_name = input('\n选择一个分类或all\n')
        while (Classify_name not in self.dict_bvID.keys() and Classify_name != 'all'):
            Classify_name = input('\n选择一个分类或all\n')
        for key, value in self.dict_bvID.items():
            # 选择一个分类
            if key == Classify_name or Classify_name == 'all':
                print(key, value)
                num = 1
                for i in value:
                    try:
                        print('第' + str(num) + '/' + str(len(value)) + '个视频：' + i['title'])
                        you_url = 'https://www.bilibili.com/video/' + you_get_down.change( i['bvid'])
                        # 视频输出的位置
                        path = self.path + key
                        you_get_down(you_url, path)
                        num += 1
                    except Exception as e:
                        print('异常：', e)
                        num += 1

    def get_dict_bvID(self, up_id, tid, count=30):

        pn = 0
        pn += count // 30
        if count % 30 != 0:
            pn += 1
        list_bv = []
        header = {
            'user-agent': self.UA
        }
        for i in range(1, pn + 1):
            param = {
                'mid': up_id,
                'ps': '30',
                'tid': tid,
                'pn': str(i),
                'keyword': '',
                'order': 'pubdate',
                'jsonp': 'jsonp',
            }
            url = 'https://api.bilibili.com/x/space/arc/search?'
            response = requests.get(url=url, headers=header, params=param,verify=False)
            dict_ = response.json()
            self.dict_tid = dict_['data']['list']['tlist']
            vlist_ = dict_['data']['list']['vlist']
            for i in vlist_:
                d = {}
                d['title'] = i['title']
                d['bvid'] = i['bvid']
                list_bv.append(d)

        return list_bv


class Favorite_down:
    dict_name = {}
    list_name = []
    dict_BV = {}

    def __init__(self, UA, up_id, cookie, path='./'):
        self.UA = UA
        self.cookie = cookie
        self.up_mid = up_id
        self.path = path

        # 获取所有收藏夹
        # 获取TA的创建
        self.get_favorite_lsit(self.up_mid)
        # 获取TA的收藏
        self.get_favorite_collected(self.up_mid)

        # 获取所有收藏夹中视频的BV号
        for kv in self.dict_name['list']:
            kv_key = kv.keys()
            # 选择公开且存在的收藏夹，23为私密收藏夹，1为已删除
            # 如果是下载自己的收藏夹，则可以删除筛选条件kv['attr'] == 22 and
            if ('state' not in kv_key or kv['state'] == 0):
                media_id, media_count = str(kv['id']), kv['media_count']
                print(kv['title'], end=':')
                self.dict_BV[kv['title']] = self.get_favorite_BV(media_id, media_count)
                self.list_name.append({kv['title']: len(self.dict_BV[kv['title']])})

        with open('收藏夹名称&视频数量.txt', 'w', encoding='utf-8') as fp:
            json.dump(self.list_name, fp=fp, ensure_ascii=False)

        # 把获取BV号存入本地磁盘，下次就不用重新爬获
        with open('Favorite_BVid.json', 'w', encoding='utf-8') as fp:
            json.dump(self.dict_BV, fp=fp, ensure_ascii=False)

        # 从本地json文件读取BV号
        # with open('Favorite_BVid.json', 'r', encoding='utf-8') as fp:
        #     self.dict_BV = json.load(fp)

        # 用you-get下载
        # 选择一个收藏夹
        Favorite_name = input('\n选择一个收藏夹或all\n')
        while (Favorite_name not in self.dict_BV.keys() and Favorite_name != 'all'):
            Favorite_name = input('\n选择一个收藏夹或all\n')
        for key, value in self.dict_BV.items():
            # 选择一个收藏夹
            if key == Favorite_name or Favorite_name == 'all':
                print(self.dict_BV[key])
                num = 1
                for i in value:
                    try:
                        print('第' + str(num) + '/' + str(len(value)) + '个视频：' + i['title'])
                        you_url = 'https://www.bilibili.com/video/av' +str( you_get_down.change(i['bv_id']))
                        # 视频输出的位置
                        path = self.path + key
                        you_get_down.download(you_url, path)
                        num += 1
                    except Exception as e:
                        print('异常：', e)
                        num += 1

    def get_favorite_lsit(self, up_mid):
        url = 'https://api.bilibili.com/x/v3/fav/folder/created/list-all?'
        param = {
            'up_mid': up_mid,
            'jsonp': 'jsonp'
        }

        header = {
            'user-agent': self.UA,
            'cookie': self.cookie
        }
        response = requests.get(url=url, params=param)

        dict_ = response.json()
        self.dict_name['count'] = dict_['data']['count']
        self.dict_name['list'] = dict_['data']['list']
        print('TA的创建', self.dict_name)

    def get_favorite_collected(self, up_mid):
        pn = 1
        url = 'https://api.bilibili.com/x/v3/fav/folder/collected/list?'
        param = {
            'up_mid': up_mid,
            'jsonp': 'jsonp',
            'pn': '1',
            'ps': '20'
        }

        header = {
            'user-agent': self.UA,
            'cookie': self.cookie
        }
        response = requests.get(url=url, params=param)

        dict_ = response.json()
        self.dict_name['count'] += dict_['data']['count']
        self.dict_name['list'].extend(dict_['data']['list'])
        if dict_['data']['count'] > 20:
            pn = dict_['data']['count'] // 20
            if dict_['data']['count'] % 20 != 0:
                pn += 1
        for i in range(2, pn + 1):
            param = {
                'up_mid': up_mid,
                'jsonp': 'jsonp',
                'pn': str(i),
                'ps': '20'
            }
            response = requests.get(url=url, params=param)

            dict_ = response.json()
            self.dict_name['list'].extend(dict_['data']['list'])
        print('TA的收藏', self.dict_name)

    def get_favorite_BV(self, media_id, media_count):
        list_BV = []
        url = 'https://api.bilibili.com/x/v3/fav/resource/list?'
        n = media_count // 20
        if media_count % 20 != 0:
            n += 1
        for i in range(1, n + 1):
            param = {
                'media_id': media_id,
                'pn': str(i),
                'ps': '20',
                'keyword': '',
                'order': 'mtime',
                'type': '0',
                'tid': '0',
                'jsonp': 'jsonp',
            }

            header = {
                'user-agent': self.UA,
                'cookie': self.cookie
            }

            response = requests.get(headers=header, params=param, url=url,verify=False)

            dict_js = response.json()
            for i in dict_js['data']['medias']:
                # 跳过已失效视频
                if i['title'] != '已失效视频':
                    d = {}
                    d['upper'] = i['upper']
                    d['bv_id'] = i['bv_id']
                    d['title'] = i['title']
                    list_BV.append(d)

        print(len(list_BV))
        return list_BV


class All_down:
    list_bvID = []

    def __init__(self, UA, up_id, path='./'):
        self.biz_id = ''
        self.up_id = up_id
        self.UA = UA
        self.path = path

        self.get_list_bvID(self.UA, self.up_id, self.biz_id)
        self.list_bvID = list(filter(None, self.list_bvID))

        # 下载
        l = len(self.list_bvID)
        num = 1
        for i in self.list_bvID:
            # if i['title']=='':
            try:
                print('第%s/%s个视频：%s' % (str(num), str(l), i['title']))
                you_url = 'https://www.bilibili.com/video/' + i['bv_id']
                # 视频输出的位置
                path = self.path
                you_get_down(you_url, path)
                num += 1
            except Exception as e:
                print('异常：', e)
                num += 1

    def get_list_bvID(self, UA, up_id, biz_id):

        header = {
            'user-agent': UA
        }
        param = {
            'type': '1',
            'biz_id': up_id,
            'bvid': biz_id,
            'mobi_app': 'web',
            'ps': '100',
            'direction': 'false',
        }
        url = 'https://api.bilibili.com/x/v2/medialist/resource/list?'
        response = requests.get(url=url, headers=header, params=param,verify=False)
        for i in response.json()['data']['media_list']:
            self.list_bvID.append({'title': i['title'], 'bv_id': i['bv_id']})

        if len(self.list_bvID) % 100 == 0:
            biz_id = self.list_bvID.pop()['bv_id']
            self.list_bvID.append(None)
            self.get_list_bvID(UA, up_id, biz_id)


if __name__ == '__main__':
    up_id = '409647592'
    UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    cookie = 'buvid3=C73A6EC3-5997-4121-581C-5390DD7791C570110infoc; CURRENT_FNVAL=80; blackside_state=1; sid=6gxox1b0; DedeUserID=409647592; DedeUserID__ckMd5=b583d5e7d5c46e47; SESSDATA=1ffe94e1%2C1623057913%2Ca297a*c1; bili_jct=6fbe796f30c61c3ecf983a5198a83876; _uuid=B5353E74-3CA6-0118-5939-A6033D789DAF75239infoc; rpdid=|(u~JlYY~lu|0J\'uY|)||kulk; CURRENT_QUALITY=120; bp_t_offset_409647592=483067951181271329; bp_video_offset_409647592=491502399361488396'
    path = 'C:\\Users\\Dr.chen\\Desktop\\bili\\'

    # a = Channel_down(UA, up_id, path)         #按频道下载
    b = Favorite_down(UA,up_id,cookie,path)   #下载收藏夹
    # c = All_down(UA, up_id, path)             #下载所有
    # d = Classify_down(UA, up_id, path)        #按分类下载
