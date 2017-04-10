# -*- coding:utf-8 -*-
import urllib
import urllib2


class Util(object):
    default_music_header = {
        'Host': 'music.163.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Connection': 'keep-alive'
    }

    @staticmethod
    def request(url, data, header):
        if header:
            req = urllib2.Request(url, headers=header)
        else:
            req = urllib2.Request(url)

        if data:
            d = urllib.urlencode(data)
            response = urllib2.urlopen(req, d)
        else:
            response = urllib2.urlopen(req)
        return response.read()

    @staticmethod
    def get(url, header=None):
        if not header:
            header = Util.default_music_header
        return Util.request(url, None, header)

    @staticmethod
    def post(url, params=None, header=None):
        if not params:
            params = {}
        return Util.request(url, params, header)

    @staticmethod
    def download(url, local):
        urllib.urlretrieve(url, local, Util.schedule)

    @staticmethod
    def schedule(a, b, c):
        per = 100.0 * a * b / c
        if per > 100:
            per = 100
        print '%.2f%%' % per