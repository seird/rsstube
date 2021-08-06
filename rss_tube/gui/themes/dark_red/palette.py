from PyQt5 import QtGui


def get_palette() -> QtGui.QPalette:
    palette = QtGui.QPalette()

    palette.setColor(QtGui.QPalette.Active, QtGui.QPalette.Window, QtGui.QColor(0x3B3B3D))
    palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.Window, QtGui.QColor(0x404042))
    palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Window, QtGui.QColor(0x424242))

    palette.setColor(QtGui.QPalette.Active, QtGui.QPalette.WindowText, QtGui.QColor(0xCACBCE))
    palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, QtGui.QColor(0xC8C8C6))
    palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, QtGui.QColor(0x707070))

    palette.setColor(QtGui.QPalette.Active, QtGui.QPalette.Text, QtGui.QColor(0xCACBCE))
    palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.Text, QtGui.QColor(0xC8C8C6))
    palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Text, QtGui.QColor(0x707070))

    palette.setColor(QtGui.QPalette.Active, QtGui.QPalette.PlaceholderText, QtGui.QColor(0x7D7D82))
    palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.PlaceholderText, QtGui.QColor(0x87888C))
    palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.PlaceholderText, QtGui.QColor(0x737373))

    palette.setColor(QtGui.QPalette.Active, QtGui.QPalette.BrightText, QtGui.QColor(0x252627))
    palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, QtGui.QColor(0x2D2D2F))
    palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, QtGui.QColor(0x333333))

    palette.setColor(QtGui.QPalette.Active, QtGui.QPalette.Base, QtGui.QColor(0x27272A))
    palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.Base, QtGui.QColor(0x2A2A2D))
    palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Base, QtGui.QColor(0x343437))

    palette.setColor(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, QtGui.QColor(0x2C2C30))
    palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, QtGui.QColor(0x2B2B2F))
    palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, QtGui.QColor(0x36363A))

    palette.setColor(QtGui.QPalette.All, QtGui.QPalette.ToolTipBase, QtGui.QColor(0x532D2D))
    palette.setColor(QtGui.QPalette.All, QtGui.QPalette.ToolTipText, QtGui.QColor(0xBFBFBF))

    palette.setColor(QtGui.QPalette.Active, QtGui.QPalette.Button, QtGui.QColor(0x28282B))
    palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.Button, QtGui.QColor(0x28282B))
    palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Button, QtGui.QColor(0x2B2A2A))

    palette.setColor(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, QtGui.QColor(0xB9B9BE))
    palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, QtGui.QColor(0x9E9FA5))
    palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, QtGui.QColor(0x73747E))

    palette.setColor(QtGui.QPalette.Active, QtGui.QPalette.Highlight, QtGui.QColor(0x532D2D))
    palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.Highlight, QtGui.QColor(0x463535))
    palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Highlight, QtGui.QColor(0x3D2929))

    palette.setColor(QtGui.QPalette.Active, QtGui.QPalette.HighlightedText, QtGui.QColor(0xCCCCCC))
    palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.HighlightedText, QtGui.QColor(0xCECECE))
    palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.HighlightedText, QtGui.QColor(0x707070))

    palette.setColor(QtGui.QPalette.All, QtGui.QPalette.Light, QtGui.QColor(0x414145))
    palette.setColor(QtGui.QPalette.All, QtGui.QPalette.Midlight, QtGui.QColor(0x39393C))
    palette.setColor(QtGui.QPalette.All, QtGui.QPalette.Mid, QtGui.QColor(0x2F2F32))
    palette.setColor(QtGui.QPalette.All, QtGui.QPalette.Dark, QtGui.QColor(0x202022))
    palette.setColor(QtGui.QPalette.All, QtGui.QPalette.Shadow, QtGui.QColor(0x19191A))

    palette.setColor(QtGui.QPalette.All, QtGui.QPalette.Link, QtGui.QColor(0xB66868))
    palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Link, QtGui.QColor(0xA47474))
    palette.setColor(QtGui.QPalette.All, QtGui.QPalette.LinkVisited, QtGui.QColor(0xB87575))
    palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.LinkVisited, QtGui.QColor(0xA67777))

    return palette
