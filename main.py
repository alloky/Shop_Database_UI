import wx

import gui.mainframe


def main():
    app = wx.App(False)
    gui.mainframe.MainFrame(None, 'gui/icon/')
    app.MainLoop()


if __name__ == '__main__':
    main()
