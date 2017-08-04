import wx
import ObjectListView as olv
import rus_locale as locale

APP_NAME = 'Shop UI'


class DbOlv(olv.ObjectListView):
    def __init__(self, parent):
        super(DbOlv, self).__init__(parent, style=wx.LC_REPORT)

        for (index, name), prop in zip(enumerate(locale.col), [1, 5, 2, 2, 2]):
            new_col = olv.ColumnDefn(name, isSpaceFilling=True,
                                     valueGetter=index, minimumWidth=prop * 40)
            new_col.freeSpaceProportion = prop
            self.AddColumnDefn(new_col)

        self.CreateCheckStateColumn()

        self.SetEmptyListMsg('No items or db is not connected')


class ShopTab(wx.Panel):
    def __init__(self, parent):
        super(ShopTab, self).__init__(parent)

        button_sizer = wx.GridSizer(4, 1, 10, 0)  # rows, cols, vgap, hgap

        buttons = [wx.Button(self, label=locale.add_button),
                   wx.Button(self, label=locale.delete_button),
                   wx.Button(self, label=locale.to_cart_button)]
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


class CustomerTab(wx.Panel):
    def __init__(self, parent):
        super(CustomerTab, self).__init__(parent)


class ShopNotebook(wx.Notebook):
    def __init__(self, parent):
        super(ShopNotebook, self).__init__(parent)

        self.AddPage(ShopTab(self), locale.shop_tab)
        self.AddPage(CustomerTab(self), locale.customer_tab)


class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        super(MainWindow, self).__init__(parent, title=title)

        self.init_menubar()
        self.init_toolbar()

        panel = wx.Panel(self)
        notebook = ShopNotebook(panel)

        sizer = wx.BoxSizer()
        sizer.Add(notebook, 1, wx.EXPAND)
        panel.SetSizer(sizer)

        self.SetSize((900, 500))  # TODO: make constant
        self.Show(True)

    def init_menubar(self):
        menu_bar = wx.MenuBar()

        # file_menu = wx.Menu() # TODO: add compatibility for non-mac
        # quit_item = file_menu.Append(wx.ID_CLOSE, "Quit {}".format(APP_NAME))
        # menu_bar.Append(file_menu, "File")

        help_menu = wx.Menu()
        about_item = help_menu.Append(wx.ID_ABOUT, "About {}".format(APP_NAME))
        menu_bar.Append(help_menu, "Help")

        self.SetMenuBar(menu_bar)

        self.Bind(wx.EVT_MENU, self.on_about, about_item)

    def init_toolbar(self):
        tb = self.CreateToolBar()
        # set_tool = toolbar.AddTool(wx.ID_ANY, '', wx.Bitmap('set.png'))
        set_tool = tb.AddTool(wx.ID_ANY, '',
                              wx.Image('set.png',
                                       wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        tb.Realize()

        self.Bind(wx.EVT_TOOL, self.on_set, set_tool)

    def on_about(self, event):
        dlg = wx.MessageDialog(self, "About {}".format(APP_NAME), APP_NAME)
        dlg.ShowModal()
        dlg.Destroy()

    def on_set(self, event):
        print('on set')


def main():
    app = wx.App(False)
    MainWindow(None, APP_NAME)
    app.MainLoop()


if __name__ == '__main__':
    main()
