import platform
import os
import pickle

import wx

import model
from model import enums as en
from . import carttab
from . import dbdialog
from . import shoptab
from .locale import rus as locale

DEFAULT_DB_PATH = '.shop_db_cache'


class ShopNotebook(wx.Notebook):
    def __init__(self, parent):
        super(ShopNotebook, self).__init__(parent)

        self.AddPage(shoptab.ShopTab(self), locale.SHOP_TAB)
        self.AddPage(carttab.CartTab(self), locale.CART_TAB)


class MainFrame(wx.Frame):
    def __init__(self, parent, path_to_icons):
        super(MainFrame, self).__init__(parent, title=locale.APP_NAME)

        self.path_to_icons = path_to_icons

        self._init_menubar()
        self._init_toolbar()

        panel = wx.Panel(self)
        self.notebook = ShopNotebook(panel)
        self.notebook.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self._refresh)

        sizer = wx.BoxSizer()
        sizer.Add(self.notebook, 1, wx.EXPAND)
        panel.SetSizer(sizer)

        self.shop = model.Shop()
        self._open_default_db()

        self.SetSize((900, 500))
        self.Show(True)

    def _init_menubar(self):
        menu_bar = wx.MenuBar()

        # file_menu = wx.Menu() # TODO: add compatibility for non-mac
        # quit_item = file_menu.Append(wx.ID_CLOSE, "Quit {}".format(APP_NAME))
        # menu_bar.Append(file_menu, "File")

        help_menu = wx.Menu()
        about_item = help_menu.Append(wx.ID_ABOUT, locale.ABOUT_ITEM)
        menu_bar.Append(help_menu, locale.HELP)

        self.SetMenuBar(menu_bar)
        self.Bind(wx.EVT_CLOSE, self._on_close)

        self.Bind(wx.EVT_MENU, self._on_about, about_item)

    def _init_toolbar(self):
        toolbar = self.CreateToolBar()

        refresh_tool = toolbar.AddTool(wx.ID_REFRESH, locale.REFRESH,
                                       self._get_icon('refresh'))
        set_tool = toolbar.AddTool(wx.ID_SETUP, locale.SETTINGS,
                                   self._get_icon('set'))

        toolbar.Realize()

        self.Bind(wx.EVT_TOOL, self._refresh, refresh_tool)
        self.Bind(wx.EVT_TOOL, self._on_set, set_tool)

    def _on_about(self, event):
        wx.MessageBox(locale.ABOUT_DIAL, locale.ABOUT_ITEM, parent=self)

    def _on_set(self, event):
        with dbdialog.DbSetDial(self) as dlg:
            if dlg.ShowModal() == wx.OK:
                self.shop.connect_db(*dlg.get_data())

                with open(DEFAULT_DB_PATH, 'wb') as f:
                    data = dlg.get_data()
                    pickle.dump((data[0], en.Action.OPEN, data[2]), f)

    def _refresh(self, e):
        self.shop.ui_display_products()
        self.shop.ui_display_order()

    def _get_icon(self, filename):
        path = '{}{}.png'.format(self.path_to_icons, filename)
        if platform.system() == 'Darwin':
            return wx.Bitmap(path)
        return (wx.Image(path).Rescale(40, 40)).ConvertToBitmap()

    def _on_close(self, e):
        print('closed correctly')
        self.shop.close_connection()
        self.Destroy()

    def _open_default_db(self):
        if os.path.isfile(DEFAULT_DB_PATH):
            with open(DEFAULT_DB_PATH, 'rb') as f:
                self.shop.connect_db(*pickle.load(f))
