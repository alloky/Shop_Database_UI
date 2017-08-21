import wx

import model
import model.exception as vex
import db.exception as ex
from .error_message import error_message
from .locale import rus as locale


class CenterText(wx.StaticText):
    def __init__(self, parent, label=''):
        super(CenterText, self).__init__(parent, label=label,
                                         style=wx.ALIGN_CENTER_VERTICAL |
                                               wx.ALIGN_LEFT)


class AddDialog(wx.Dialog):
    def __init__(self, parent, title, table, add_func):
        super(AddDialog, self).__init__(parent, title=title)

        self.table = table
        self.add_func = add_func
        columns = [x.name for x in table.columns if x.user_init]

        input_sizer = wx.FlexGridSizer(2 * len(columns), 2, 10, 10)
        self.warning_label = dict()
        self.text_ctrl = list()

        for col in columns:
            self.warning_label[col] = CenterText(self)
            self.warning_label[col].SetForegroundColour(wx.RED)

            self.text_ctrl.append(wx.TextCtrl(self))

            input_sizer.AddStretchSpacer(1)
            input_sizer.AddMany([(self.warning_label[col], 1, wx.EXPAND),
                                 (CenterText(self, table.display_source[col]),
                                  1, wx.EXPAND),
                                 (self.text_ctrl[-1], 1, wx.EXPAND)])

        input_sizer.AddGrowableCol(0, 0)
        input_sizer.AddGrowableCol(1, 1)

        outer_sizer = wx.BoxSizer(wx.VERTICAL)
        outer_sizer.Add(input_sizer, 0, wx.ALL | wx.EXPAND, border=5)
        outer_sizer.Add(self._get_buttons(), 0, wx.ALL | wx.EXPAND, border=5)
        self.SetSizerAndFit(outer_sizer)

        self.shop = model.Shop()

        self.SetSize(500, -1)
        self.Center()

    def _get_buttons(self):
        ok_btn = wx.Button(self, label=locale.OK)
        cancel_btn = wx.Button(self, label=locale.CANCEL)

        sizer = wx.GridSizer(1, 2, 0, 10)

        sizer.Add(ok_btn, 1, wx.EXPAND)
        sizer.Add(cancel_btn, 1, wx.EXPAND)

        ok_btn.Bind(wx.EVT_BUTTON, self._on_ok)
        cancel_btn.Bind(wx.EVT_BUTTON, self._on_cancel)

        return sizer

    def _on_ok(self, e):
        for warn in self.warning_label.values():
            warn.SetLabel('')

        try:
            new_row = self.table.row_class.add(
                [x.GetValue() for x in self.text_ctrl])
            self.add_func(new_row)
            self.EndModal(wx.OK)
        except vex.ValidationException as e:
            for col, type_num in e.column_dict.items():
                self.warning_label[col].SetLabel(locale.CE[type_num])
        except ex.DbException as e:
            error_message(self, exception=e)
        except ex.ConstraintException as e:
            self.warning_label[e.column_name].SetLabel(locale.CE[e.type_num])

    def _on_cancel(self, e):
        self.EndModal(wx.CANCEL)
