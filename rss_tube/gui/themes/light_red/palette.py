from PyQt5 import QtGui


def get_palette() -> QtGui.QPalette:
    palette = QtGui.QPalette()

    palette.setColor(QtGui.QPalette.Active, QtGui.QPalette.Window, QtGui.QColor(0xF7F7F7))
    palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.Window, QtGui.QColor(0xFCFCFC))
    palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Window, QtGui.QColor(0xEDEDED))

    palette.setColor(QtGui.QPalette.Active, QtGui.QPalette.WindowText, QtGui.QColor(0x1D1D20))
    palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, QtGui.QColor(0x252528))
    palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, QtGui.QColor(0x8C8C92))

    palette.setColor(QtGui.QPalette.Active, QtGui.QPalette.Text, QtGui.QColor(0x1D1D20))
    palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.Text, QtGui.QColor(0x252528))
    palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Text, QtGui.QColor(0x8C8C92))

    palette.setColor(QtGui.QPalette.Active, QtGui.QPalette.PlaceholderText, QtGui.QColor(0x71727D))
    palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.PlaceholderText, QtGui.QColor(0x878893))
    palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.PlaceholderText, QtGui.QColor(0xA3A4AC))

    palette.setColor(QtGui.QPalette.Active, QtGui.QPalette.BrightText, QtGui.QColor(0xF3F3F4))
    palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, QtGui.QColor(0xEAEAEB))
    palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, QtGui.QColor(0xE4E5E7))

    palette.setColor(QtGui.QPalette.Active, QtGui.QPalette.Base, QtGui.QColor(0xF9F9F9))
    palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.Base, QtGui.QColor(0xFCFCFC))
    palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Base, QtGui.QColor(0xEFEFF2))

    palette.setColor(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, QtGui.QColor(0xF3E8E8))
    palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, QtGui.QColor(0xF6EEEE))
    palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, QtGui.QColor(0xE9DDDD))

    palette.setColor(QtGui.QPalette.All, QtGui.QPalette.ToolTipBase, QtGui.QColor(0x4D7F1A))
    palette.setColor(QtGui.QPalette.All, QtGui.QPalette.ToolTipText, QtGui.QColor(0xF9F9F9))

    # palette.setColor(QtGui.QPalette.Active, QtGui.QPalette.Button, QtGui.QColor(0xD4D5DD))
    # palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.Button, QtGui.QColor(0xDCDCE0))
    # palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Button, QtGui.QColor(0xE5E5E6))

    palette.setColor(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, QtGui.QColor(0x181A18))
    palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, QtGui.QColor(0x454A54))
    palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, QtGui.QColor(0x97979B))

    palette.setColor(QtGui.QPalette.Active, QtGui.QPalette.Highlight, QtGui.QColor(0xB82C2C))
    palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.Highlight, QtGui.QColor(0xBE8E8E))
    palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Highlight, QtGui.QColor(0xD5B4B4))

    palette.setColor(QtGui.QPalette.Active, QtGui.QPalette.HighlightedText, QtGui.QColor(0xFFFFFF))
    palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.HighlightedText, QtGui.QColor(0x252528))
    palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.HighlightedText, QtGui.QColor(0x8C8C92))

    palette.setColor(QtGui.QPalette.All, QtGui.QPalette.Light, QtGui.QColor(0xF9F9F9))
    palette.setColor(QtGui.QPalette.All, QtGui.QPalette.Midlight, QtGui.QColor(0xE9E9EB))
    palette.setColor(QtGui.QPalette.All, QtGui.QPalette.Mid, QtGui.QColor(0xC9C9CF))
    palette.setColor(QtGui.QPalette.All, QtGui.QPalette.Dark, QtGui.QColor(0xBBBBC2))
    palette.setColor(QtGui.QPalette.All, QtGui.QPalette.Shadow, QtGui.QColor(0x6C6D79))

    palette.setColor(QtGui.QPalette.All, QtGui.QPalette.Link, QtGui.QColor(0xB66868))
    palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Link, QtGui.QColor(0xA47474))
    palette.setColor(QtGui.QPalette.All, QtGui.QPalette.LinkVisited, QtGui.QColor(0xB87575))
    palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.LinkVisited, QtGui.QColor(0xA67777))

    return palette
