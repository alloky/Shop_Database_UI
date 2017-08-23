import wx

import model
from db import exception as ex
from .error_message import error_message
from .adddialog import AddDialog
from .dbpanel import DbPanel
from model.db_description import storage
from .locale import rus as locale


class CustomerTab(DbPanel):
    def __init__(self, parent):
        super(CustomerTab, self).__init__(parent, storage['customers'],
                                          locale.ADD_CUSTOMER, 5)

        self.choose_btn = wx.Button(self, label=locale.CHOOSE)
        self.cancel_btn = wx.Button(self, label=locale.CANCEL)

        self.button_sizer.AddSpacer(50)
        self.button_sizer.Add(self.choose_btn, 0, wx.BOTTOM | wx.EXPAND,
                              border=10)
        self.button_sizer.Add(self.cancel_btn, 0, wx.EXPAND)

        self._display_data()

    def _on_delete(self, e):
        select = self.db_list.GetSelectedObject()
        if select is None:
            return

        try:
            self.shop.delete_from('customers', [select.id])
            self.db_list.RemoveObject(select)
        except ex.DbException as e:
            error_message(self, exception=e)

    def _on_add(self, e):
        with AddDialog(self, locale.NEW_CUSTOMER, storage['customers'],
                       self.shop.add_customer) as dlg:
            if dlg.ShowModal() == wx.OK:
                self._display_data()

    def _display_data(self):
        self.db_list.SetObjects([model.Customer(x) for x in
                                 self.shop.get_from('customers')])


class CustomerDial(wx.Dialog):
    def __init__(self, parent):
        super(CustomerDial, self).__init__(parent)

        self._customer = None

        self.panel = CustomerTab(self)
        self.panel.db_list.SetEmptyListMsg(locale.CUSTOMER_LC)

        self.Bind(wx.EVT_BUTTON, self._on_choose, self.panel.choose_btn)
        self.Bind(wx.EVT_BUTTON, self._on_cancel, self.panel.cancel_btn)

        self.SetSize((900, 300))
        self.SetTitle(locale.CHOOSE_CUSTOMER_TITLE)

    def _on_choose(self, e):
        selected = self.panel.db_list.GetSelectedObject()
        if selected is None:
            return

        self._customer = selected
        self.EndModal(wx.OK)

    def _on_cancel(self, e):
        self.EndModal(wx.CANCEL)

    def get_customer(self):
        return self._customer
