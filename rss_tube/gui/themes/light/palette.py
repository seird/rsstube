from PyQt6 import QtGui


def get_palette() -> QtGui.QPalette:
    palette = QtGui.QPalette()

    palette.setColor(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Window, QtGui.QColor(0xF7F7F7))
    palette.setColor(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Window, QtGui.QColor(0xFCFCFC))
    palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Window, QtGui.QColor(0xEDEDED))

    palette.setColor(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.WindowText, QtGui.QColor(0x1D1D20))
    palette.setColor(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.WindowText, QtGui.QColor(0x252528))
    palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.WindowText, QtGui.QColor(0x8C8C92))

    palette.setColor(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Text, QtGui.QColor(0x1D1D20))
    palette.setColor(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Text, QtGui.QColor(0x252528))
    palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Text, QtGui.QColor(0x8C8C92))

    palette.setColor(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.PlaceholderText, QtGui.QColor(0x71727D))
    palette.setColor(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.PlaceholderText, QtGui.QColor(0x878893))
    palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.PlaceholderText, QtGui.QColor(0xA3A4AC))

    palette.setColor(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.BrightText, QtGui.QColor(0xF3F3F4))
    palette.setColor(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.BrightText, QtGui.QColor(0xEAEAEB))
    palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.BrightText, QtGui.QColor(0xE4E5E7))

    palette.setColor(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Base, QtGui.QColor(0xF9F9F9))
    palette.setColor(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Base, QtGui.QColor(0xFCFCFC))
    palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Base, QtGui.QColor(0xEFEFF2))

    palette.setColor(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.AlternateBase, QtGui.QColor(0xECF3E8))
    palette.setColor(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.AlternateBase, QtGui.QColor(0xF1F6EE))
    palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.AlternateBase, QtGui.QColor(0xE1E9DD))

    palette.setColor(QtGui.QPalette.ColorGroup.All, QtGui.QPalette.ColorRole.ToolTipBase, QtGui.QColor(0x4D7F1A))
    palette.setColor(QtGui.QPalette.ColorGroup.All, QtGui.QPalette.ColorRole.ToolTipText, QtGui.QColor(0xF9F9F9))

    # palette.setColor(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Button, QtGui.QColor(0xD4D5DD))
    # palette.setColor(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Button, QtGui.QColor(0xDCDCE0))
    # palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Button, QtGui.QColor(0xE5E5E6))

    palette.setColor(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.ButtonText, QtGui.QColor(0x181A18))
    palette.setColor(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.ButtonText, QtGui.QColor(0x454A54))
    palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.ButtonText, QtGui.QColor(0x97979B))

    palette.setColor(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Highlight, QtGui.QColor(0x507F1F))
    palette.setColor(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Highlight, QtGui.QColor(0xA6BE8E))
    palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Highlight, QtGui.QColor(0xC3D5B4))

    palette.setColor(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.HighlightedText, QtGui.QColor(0xFFFFFF))
    palette.setColor(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.HighlightedText, QtGui.QColor(0x252528))
    palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.HighlightedText, QtGui.QColor(0x8C8C92))

    palette.setColor(QtGui.QPalette.ColorGroup.All, QtGui.QPalette.ColorRole.Light, QtGui.QColor(0xF9F9F9))
    palette.setColor(QtGui.QPalette.ColorGroup.All, QtGui.QPalette.ColorRole.Midlight, QtGui.QColor(0xE9E9EB))
    palette.setColor(QtGui.QPalette.ColorGroup.All, QtGui.QPalette.ColorRole.Mid, QtGui.QColor(0xC9C9CF))
    palette.setColor(QtGui.QPalette.ColorGroup.All, QtGui.QPalette.ColorRole.Dark, QtGui.QColor(0xBBBBC2))
    palette.setColor(QtGui.QPalette.ColorGroup.All, QtGui.QPalette.ColorRole.Shadow, QtGui.QColor(0x6C6D79))

    palette.setColor(QtGui.QPalette.ColorGroup.All, QtGui.QPalette.ColorRole.Link, QtGui.QColor(0x4B7B19))
    palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Link, QtGui.QColor(0x4F6935))
    palette.setColor(QtGui.QPalette.ColorGroup.All, QtGui.QPalette.ColorRole.LinkVisited, QtGui.QColor(0x507826))
    palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.LinkVisited, QtGui.QColor(0x506935))

    return palette
