import wx
import ObjectListView as Olv

import model
from db import exception as ex
from .dbview import DbView
from gui.locale import rus as locale


class DbPanel(wx.Panel):
    def __init__(self, parent, table, add_label, border=0):
        super(DbPanel, self).__init__(parent)

        self.table = table
        self.shop = model.Shop()

        self.button_sizer = wx.BoxSizer(wx.VERTICAL)
        self.button_sizer.Add(self._get_view_buttons(add_label), 0)

        self.db_list = DbView(self, table)

        self.db_list.cellEditMode = self.db_list.CELLEDIT_DOUBLECLICK
        for i, col in enumerate(table.columns):
            self.db_list.columns[i].isEditable = col.user_init
        self.db_list.Bind(Olv.EVT_CELL_EDIT_FINISHING, self._update_checker)

        outer_sizer = wx.BoxSizer(wx.HORIZONTAL)

        outer_sizer.Add(self.db_list, 1, wx.LEFT | wx.TOP | wx.BOTTOM |
                        wx.EXPAND, border=border)
        outer_sizer.AddSpacer(4)
        outer_sizer.Add(self.button_sizer, 0, wx.RIGHT | wx.TOP | wx.BOTTOM |
                        wx.EXPAND, border=border)

        self.SetSizer(outer_sizer)

    def _get_view_buttons(self, add_label):
        sizer = wx.GridSizer(2, 1, 10, 0)

        buttons = [wx.Button(self, label=add_label),
                   wx.Button(self, label=locale.DELETE_BUTTON)]

        for func, button in zip([self._on_add, self._on_delete], buttons):
            sizer.Add(button, 1, wx.EXPAND)
            self.Bind(wx.EVT_BUTTON, func, button)

        return sizer

    def _update_checker(self, evt):
        col_name = evt.objectListView.columns[evt.subItemIndex].valueGetter
        upd_id = evt.rowModel.id
        value = evt.editor.Value

        try:
            self.shop.update(self.table.name, col_name, upd_id, value)
        except ex.DbException as e:
            print('_update_checker: ', e.message)
            evt.Veto()
        except ex.ConstraintException as e:
            print('_update_checker: ', locale.CE[e.type_num])
            evt.Veto()

    def _on_add(self, e):
        print('on add')

    def _on_delete(self, e):
        print('on delete')
