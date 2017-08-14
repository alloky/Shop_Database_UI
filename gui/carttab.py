import wx

import model
from .dbview import DbView
from .customerdialog import CustomerDial
from model.db_description import order
from .locale import rus as locale


class CartTab(wx.Panel):
    def __init__(self, parent):
        super(CartTab, self).__init__(parent)

        self.shop = model.Shop()
        self.shop.ui_display_order = self._display_order

        self.column_sizer = wx.BoxSizer(wx.VERTICAL)

        self.customer_text = wx.StaticText(self)
        self.column_sizer.Add(self.customer_text, 0, wx.BOTTOM | wx.EXPAND,
                              border=10)
        self.customer_text.SetLabelText(locale.CUSTOMER_NOT_CHOSEN)

        self._add_left_buttons()

        self.db_list = DbView(self, order)
        self.db_list.SetEmptyListMsg(locale.ORDER_LC)
        self.db_list.InstallCheckStateColumn(self.db_list.columns[0])

        left_sizer = wx.BoxSizer(wx.VERTICAL)
        left_sizer.Add(self.db_list, 1, wx.EXPAND)
        left_sizer.AddSpacer(4)
        left_sizer.Add(self._get_bottom_sizer(), 0, wx.EXPAND)

        self.outer_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.outer_sizer.Add(left_sizer, 1, wx.EXPAND)
        self.outer_sizer.AddSpacer(4)
        self.outer_sizer.Add(self.column_sizer, 0, wx.EXPAND)

        self.SetSizer(self.outer_sizer)

    def _add_left_buttons(self):
        self.customer_btn = wx.Button(self, label=locale.CHOOSE_CUSTOMER_BTN)
        place_order_btn = wx.Button(self, label=locale.PLACE_ORDER_BTN)
        clear_order_btn = wx.Button(self, label=locale.CLEAR_ORDER_BTN)

        self.column_sizer.Add(self.customer_btn, 0, wx.EXPAND)

        self.column_sizer.AddSpacer(50)

        self.column_sizer.Add(place_order_btn, 0, wx.BOTTOM | wx.EXPAND,
                              border=10)
        self.column_sizer.Add(clear_order_btn, 0, wx.EXPAND)

        self.Bind(wx.EVT_BUTTON, self._on_change_customer, self.customer_btn)
        self.Bind(wx.EVT_BUTTON, self._on_place_order, place_order_btn)
        self.Bind(wx.EVT_BUTTON, self._on_clear_order, clear_order_btn)

    def _get_bottom_sizer(self):
        remove_btn = wx.Button(self, label=locale.REMOVE_PRODUCT)
        self.sum_text = wx.StaticText(self)
        self._display_sum()

        bottom_sizer = wx.BoxSizer(wx.HORIZONTAL)
        bottom_sizer.Add(remove_btn, 1, wx.EXPAND)
        bottom_sizer.AddStretchSpacer(4)
        bottom_sizer.Add(self.sum_text, 1, wx.EXPAND)

        self.Bind(wx.EVT_BUTTON, self._on_remove, remove_btn)

        return bottom_sizer

    def _on_change_customer(self, e):
        with CustomerDial(self) as dlg:
            if dlg.ShowModal() == wx.OK:
                self.shop.set_customer(dlg.get_customer())
                self._display_customer()

    def _on_place_order(self, e):
        if self.shop.order.get_customer() is None:
            wx.MessageBox(locale.CUSTOMER_NOT_CHOSEN, locale.ERROR, wx.OK)
            return
        if not self.shop.order.get_cart():
            wx.MessageBox(locale.NO_PRODUCTS, locale.ERROR, wx.OK)
            return

        self.shop.place_order()

    def _on_clear_order(self, e):
        self.shop.clear_order()

    def _on_remove(self, e):
        self.shop.remove_from_cart(self.db_list.GetCheckedObjects())

    def _display_order(self):
        self.shop.ui_display_products()
        self.db_list.SetObjects(self.shop.get_order())
        self._display_customer()
        self._display_sum()

    def _display_customer(self):
        if self.shop.order.get_customer() is None:
            self.customer_text.SetLabelText(locale.CUSTOMER_NOT_CHOSEN)
            self.customer_btn.SetLabelText(locale.CHOOSE_CUSTOMER_BTN)
            return

        self.customer_text.SetLabelText(self.shop.order.get_initials())
        self.customer_btn.SetLabelText(locale.CHANGE_CUSTOMER_BTN)

    def _display_sum(self):
        self.sum_text.SetLabelText('{}{}'.format(locale.SUM,
                                                 self.shop.order.get_sum()))
