# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rss_tube/gui/designs\widget_filter_entry.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(466, 23)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.combo_target = QtWidgets.QComboBox(Form)
        self.combo_target.setObjectName("combo_target")
        self.gridLayout.addWidget(self.combo_target, 0, 0, 1, 1)
        self.combo_type = QtWidgets.QComboBox(Form)
        self.combo_type.setObjectName("combo_type")
        self.gridLayout.addWidget(self.combo_type, 0, 1, 1, 1)
        self.line_target = QtWidgets.QLineEdit(Form)
        self.line_target.setObjectName("line_target")
        self.gridLayout.addWidget(self.line_target, 0, 2, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
