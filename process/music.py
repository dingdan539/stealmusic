# -*- coding:utf-8 -*-
import json
import os
import md5
from util.common import Util


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


class StealMusic(object):
    detail_api = "http://music.163.com/api/song/detail/?ids=[xx]"
    download_api = "http://m2.music.126.net/xx1/xx2.mp3"
    search_api = "http://music.163.com/api/search/get/"

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

    def search(self, s, _type=10, limit=5, offset=0):
        """1 单曲 10 专辑 100 歌手 1000 歌单 1002 用户"""
        result = Util.post(self.search_api, {
            's': s,
            'type': _type,
            'limit': limit,
            'offset': offset
        })
        result = json.loads(result)
        return result

    def get_album_list(self, s):
        result = self.search(s)
        album = result['result']['albums']
        album_count = result['result']['albumCount']

        data = []
        if album_count:
            for i in album:
                name = i['name']
                album_id = i['id']
                artist_name = i['artist']['name']
                data.append({
                    'name': name,
                    'album_id': album_id,
                    'artist_name': artist_name
                })
        return data

    def down_music(self, songid):
        mp3_list = self.get_mp3(songid)
        local = "./downloads/"

        if not os.path.exists(local):
            os.makedirs(local)

        for i in mp3_list:
            mp3url = i['mp3url']
            name = i['name']
            temp_local = local + name + '.mp3'
            if not os.path.exists(temp_local):
                Util.download(mp3url, temp_local)