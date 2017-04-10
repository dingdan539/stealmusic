# -*- coding:utf-8 -*-
import wx
import wx.grid

import process.music as music


class GridData(wx.grid.PyGridTableBase):
    _highlighted = set()

    def __init__(self, cols, data):
        super(GridData, self).__init__()
        self._cols = cols
        self._data = data

    def GetColLabelValue(self, col):
        return self._cols[col]

    def GetNumberRows(self):
        return len(self._data)

    def GetNumberCols(self):
        return len(self._cols)

    def GetValue(self, row, col):
        return self._data[row][col]

    def SetValue(self, row, col, val):
        self._data[row][col] = val

    def GetAttr(self, row, col, kind):
        attr = wx.grid.GridCellAttr()
        attr.SetBackgroundColour(wx.GREEN if row in self._highlighted else wx.WHITE)
        return attr

    def set_value(self, row, col, val):
        self._highlighted.add(row)
        self.SetValue(row, col, val)


class Frame(wx.Frame):
    def __init__(self, parent, title):
        self.music_instance = music.StealMusic()
        wx.Frame.__init__(self, None, -1, title, size=(1000, 500))
        self.panel = wx.Panel(self)
        self.text = wx.TextCtrl(self.panel, -1, value='', pos=(400, 10), size=(200, 30))
        self.button = wx.Button(self.panel, -1, label=u'搜索', pos=(610, 10), size=(60, 30))

        self.Bind(wx.EVT_BUTTON, self.search)
        # self.Bind(wx.EVT_TEXT, self.search, self.text)

    def init_grid(self, _cols, _data):
        self.data = GridData(_cols, _data)
        self.grid = wx.grid.Grid(self.panel, pos=(100, 60), size=(800, 300))
        self.grid.SetTable(self.data)
        self.grid.SetColSize(0, 150)
        self.grid.SetColSize(1, 568)

    def search(self, event):
        try:
            search_value = self.text.GetValue()
            data = self.music_instance.get_album_list(search_value)

            _data = []
            if data:
                for i in data:
                    _data.append(
                        [i['name'], i['artist_name']]
                    )

            _cols = [u'类型', u'内容']
            _data = _data

            self.init_grid(_cols, _data)
            # self.data.set_value(2, 0, "x")

        except Exception, e:
            pass


class App(wx.App):
    def OnInit(self):
        self.frame = Frame(parent=None, title=u'dINgGoMusiC(偷音乐)')
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True

if __name__ == "__main__":
    app = App()
    app.MainLoop()
    # music.StealMusic().down_music(445845796)