import wx
import ObjectListView as Olv


class DbView(Olv.ObjectListView):
    def __init__(self, parent, table):
        super(DbView, self).__init__(parent,
                                     style=wx.BORDER_SUNKEN | wx.LC_REPORT)

        for column in table.columns:
            new_col = Olv.ColumnDefn(column.display_name, isSpaceFilling=True,
                                     valueGetter=column.name, align='right',
                                     minimumWidth=column.proportion * 40,
                                     isEditable=False)
            new_col.freeSpaceProportion = column.proportion
            self.AddColumnDefn(new_col)
