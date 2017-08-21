import wx

from .locale import rus as locale


def error_message(parent, exception=None, message=None):
    if exception is not None:
        wx.MessageBox(locale.DE[exception.type_num], locale.ERROR,
                      parent=parent)
        print(exception.message)
        return

    if message is not None:
        wx.MessageBox(message, locale.ERROR, parent=parent)
