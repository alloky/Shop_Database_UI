import wx

from . import shoptab
from . import customertab
from .locale import rus as locale


class ShopNotebook(wx.Notebook):
    def __init__(self, parent):
        super(ShopNotebook, self).__init__(parent)

        self.AddPage(shoptab.ShopTab(self), locale.SHOP_TAB)
        self.AddPage(customertab.CustomerTab(self), locale.CUSTOMER_TAB)


class MainFrame(wx.Frame):
    def __init__(self, parent, path_to_icons):
        super(MainFrame, self).__init__(parent, title=locale.APP_NAME)

        self.path_to_icons = path_to_icons

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
        about_item = help_menu.Append(wx.ID_ABOUT, locale.ABOUT_ITEM)
        menu_bar.Append(help_menu, locale.HELP)

        self.SetMenuBar(menu_bar)

        self.Bind(wx.EVT_MENU, self.on_about, about_item)

    def init_toolbar(self):
        toolbar = self.CreateToolBar()
        # set_tool = toolbar.AddTool(wx.ID_ANY, '', wx.Bitmap('set.png'))
        set_tool = toolbar.AddTool(wx.ID_ANY, locale.SET, self.get_icon('set'))
        toolbar.Realize()

        self.Bind(wx.EVT_TOOL, self.on_set, set_tool)

    def on_about(self, event):
        dlg = wx.MessageDialog(self, locale.ABOUT_DIAL, locale.ABOUT_ITEM)
        dlg.ShowModal()
        dlg.Destroy()

    def on_set(self, event):
        print('on set')

    def get_icon(self, filename):
        return wx.Image('{}{}.png'.format(self.path_to_icons, filename),
                        wx.BITMAP_TYPE_PNG).ConvertToBitmap()
