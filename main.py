# -*- coding:utf-8 -*-
import urllib
import urllib2
import json
import md5


def encrypted_id(_id):
    byte1 = bytearray('3go8&$8*3*3h0k(2)2')
    byte2 = bytearray(_id)
    byte1_len = len(byte1)
    for i in xrange(len(byte2)):
        byte2[i] = byte2[i] ^ byte1[i % byte1_len]
    m = md5.new()
    m.update(byte2)
    result = m.digest().encode('base64')[:-1]
    result = result.replace('/', '_')
    result = result.replace('+', '-')
    return result


class Util(object):
    @staticmethod
    def request(url):
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        return response.read()

    @staticmethod
    def get(url):
        return Util.request(url)

    @staticmethod
    def download(url, local):
        urllib.urlretrieve(url, local, Util.schedule)

    @staticmethod
    def schedule(a, b, c):
        per = 100.0 * a * b / c
        if per > 100:
            per = 100
        print '%.2f%%' % per


class StealMusic(object):
    detail_api = "http://music.163.com/api/song/detail/?ids=[xx]"
    download_api = "http://m2.music.126.net/xx1/xx2.mp3"

    def get_mp3(self, songid):
        mp3_list = []
        try:
            response = Util.get(self.detail_api.replace("xx", str(songid)))
            response = json.loads(response)
            songs = response['songs']
            if songs:
                for i in songs:
                    h_music = i['hMusic']
                    dfsid = str(h_music['dfsId'])
                    mp3url = self.download_api.replace("xx1", encrypted_id(dfsid)).replace("xx2", dfsid)
                    mp3_list.append({
                        'mp3url': mp3url,
                        'name': i['name']
                    })

        except Exception, e:
            print Exception, ":", e.message

        finally:
            return mp3_list

    def down_music(self, songid):
        mp3_list = self.get_mp3(songid)
        local = "./downloads/"
        for i in mp3_list:
            mp3url = i['mp3url']
            name = i['name']
            temp_local = local + name + '.mp3'
            Util.download(mp3url, temp_local)


StealMusic().down_music(445845796)