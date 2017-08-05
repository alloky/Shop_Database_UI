import wx

import ObjectListView as Olv

from .locale import rus as locale


class DbOlv(Olv.ObjectListView):
    def __init__(self, parent):
        super(DbOlv, self).__init__(parent, style=wx.LC_REPORT)

        for (index, name), prop in zip(enumerate(locale.COL), [1, 5, 2, 2, 2]):
            new_col = Olv.ColumnDefn(name, isSpaceFilling=True,
                                     valueGetter=index, minimumWidth=prop * 40)
            new_col.freeSpaceProportion = prop
            self.AddColumnDefn(new_col)

        self.CreateCheckStateColumn()

        self.SetEmptyListMsg('No items or db is not connected')


class ShopTab(wx.Panel):
    def __init__(self, parent):
        super(ShopTab, self).__init__(parent)

        button_sizer = wx.GridSizer(4, 1, 10, 0)  # rows, cols, vgap, hgap

        buttons = [wx.Button(self, label=locale.ADD_BUTTON),
                   wx.Button(self, label=locale.DELETE_BUTTON),
                   wx.Button(self, label=locale.TO_CART_BUTTON)]
        for button in buttons:
            button_sizer.Add(button, 1, wx.EXPAND)

        for func, button in zip([self.on_add, self.on_delete, self.on_to_cart],
                                buttons):
            self.Bind(wx.EVT_BUTTON, func, button)

        db_list = DbOlv(self)

        test_data = [(0, 'toy', 5, 100),
                     (1, 'car', 10, 200),
                     (2, 'plane', 100, 5000)]
        db_list.SetObjects(test_data)

        outer_sizer = wx.BoxSizer(wx.HORIZONTAL)

        outer_sizer.Add(db_list, 1, wx.EXPAND)
        outer_sizer.AddSpacer(4)
        outer_sizer.Add(button_sizer, 0, wx.TOP)

        self.SetSizer(outer_sizer)

    def on_add(self, e):
        print('on add')

    def on_delete(self, e):
        print('on delete')

    def on_to_cart(self, e):
        print('on to cart')
