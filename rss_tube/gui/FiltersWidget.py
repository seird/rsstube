from PyQt6 import QtCore, QtGui, QtWidgets

from .designs.widget_filter import Ui_Dialog as Ui_Dialog_Filter
from .designs.widget_filters import Ui_Form as Ui_Form_Filters
from .designs.widget_filter_rule import Ui_Form as Ui_Form_FilterRule
from rss_tube.database.feeds import Feeds
from rss_tube.database.filters import Filter, FilterAction, Filters, supported_parameters
from rss_tube.database.settings import Settings
from rss_tube.utils import center_widget


settings = Settings()


class FilterRuleWidget(QtWidgets.QWidget, QtWidgets.QTableWidgetItem, Ui_Form_FilterRule):
    """
    A single filter rule
    """
    def __init__(self, *args, **kwargs):
        super(FilterRuleWidget, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.combo_target.addItems(["Title", "Description", "Author", "Category"])
        self.combo_type.addItems(["contains", "equals", "doesn't contain", "doesn't equal"])


class NewFilterDialog(QtWidgets.QDialog, Ui_Dialog_Filter):
    """
    A dialog to create a new filter
    """
    def __init__(self, mainwindow: QtWidgets.QMainWindow):
        super(NewFilterDialog, self).__init__()
        self.setupUi(self)

        self.mainwindow = mainwindow
        self.feeds = Feeds()
        self.filter_properties = {}

        self.initUI()

    def initUI(self):
        self.line_name.setFocus()

        self.cb_enabled.setChecked(True)

        # Apply to
        self.combo_apply_to_group.addItems(["All", "Category", "Channel"])
        self.combo_apply_to.hide()

        # Action
        self.combo_action.addItems([action.value for action in FilterAction if action is not FilterAction.Nop])
        self.combo_action.setCurrentText("Delete")
        text = "Supported parameters (case sensitive):"
        for p in supported_parameters:
            text += f"\n    {p[0]}: {p[1]}"
        self.label_external_program_parameters.setText(text)
        self.combo_action_changed_callback(self.combo_action.currentText())

        # Match
        match_selected = settings.value("filter_edit_dialog/match", "any", type=str)
        self.cb_match_any.setChecked(match_selected == "any")
        self.cb_match_all.setChecked(match_selected == "all")

        # Rules Table
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setSelectionMode(QtWidgets.QTableWidget.SelectionMode.NoSelection)
        horizontal_header = self.tableWidget.horizontalHeader()
        horizontal_header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        horizontal_header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        horizontal_header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        vertical_header = self.tableWidget.verticalHeader()
        vertical_header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Fixed)
        vertical_header.setDefaultSectionSize(30)
        self.insert_rule()

        self.setWindowTitle("Filter editor")
        center_widget(self.mainwindow, self)

        self.link_callbacks()

    def insert_rule(self):
        """
        Insert a new filter rule
        """
        self.tableWidget.insertRow(self.tableWidget.rowCount())

        fw = FilterRuleWidget(self.tableWidget)

        new_row = self.tableWidget.rowCount()-1

        pb_add = QtWidgets.QPushButton("+")
        pb_delete = QtWidgets.QPushButton("-")

        pb_add.setFixedWidth(30)
        pb_delete.setFixedWidth(30)

        pb_add.clicked.connect(self.insert_rule)
        pb_delete.clicked.connect(lambda: self.remove_rule(self.tableWidget.currentRow()))

        self.tableWidget.setCellWidget(new_row, 0, fw)
        self.tableWidget.setCellWidget(new_row, 1, pb_add)
        self.tableWidget.setCellWidget(new_row, 2, pb_delete)

        self.tableWidget.resizeColumnToContents(1)
        self.tableWidget.resizeColumnToContents(2)

        self.tableWidget.cellWidget(0, 2).setEnabled(self.tableWidget.rowCount() > 1)

    def remove_rule(self, row: int):
        if self.tableWidget.rowCount() <= 1:
            return
        self.tableWidget.removeRow(row)
        self.tableWidget.cellWidget(0, 2).setEnabled(self.tableWidget.rowCount() > 1)

    def combo_apply_to_group_callback(self, *args):
        """
        Show categories/channels depending on the selected item in self.combo_apply_to_group
        """
        selected_group = self.combo_apply_to_group.currentText()
        self.combo_apply_to.clear()
        if selected_group == "All":
            self.combo_apply_to.hide()
        elif selected_group == "Category":
            self.combo_apply_to.show()
            categories = sorted(self.feeds.get_categories(), key=str.casefold)
            self.combo_apply_to.addItems(categories)
        elif selected_group == "Channel":
            self.combo_apply_to.show()
            feeds = sorted([feed["author"] for feed in self.feeds.get_feeds()], key=str.casefold)
            self.combo_apply_to.addItems(feeds)
        self.combo_apply_to.view().setMinimumWidth(self.combo_apply_to.minimumSizeHint().width())
    
    def combo_action_changed_callback(self, text: str):
        self.label_external_program_parameters.setVisible(text == FilterAction.RunExternalProgram.value)
        self.line_external_program.setVisible(text == FilterAction.RunExternalProgram.value)

    def dialog_accept_callback(self):
        """
        Before accepting the dialog, check if the filters are valid
        """
        if self.line_name.text() == "":
            QtWidgets.QToolTip.showText(self.pos() + self.line_name.pos(), "Please supply a filter name.")
            return

        self.filter_properties["rules"] = []
        for row in range(self.tableWidget.rowCount()):
            fw: FilterRuleWidget = self.tableWidget.cellWidget(row, 0)
            if fw.line_target.text():
                self.filter_properties["rules"].append({
                    "target": fw.combo_target.currentText(),
                    "type": fw.combo_type.currentText(),
                    "text": fw.line_target.text()
                })

        action_text = self.combo_action.currentText()
        if self.filter_properties["rules"]:
            self.filter_properties.update({
                "name": self.line_name.text(),
                "apply_to_group": self.combo_apply_to_group.currentText(),
                "apply_to": self.combo_apply_to.currentText() if self.combo_apply_to.isVisible() else "",
                "match": "any" if self.cb_match_any.isChecked() else "all" if self.cb_match_all.isChecked() else "",
                "action": FilterAction(action_text),
                "action_external_program": self.line_external_program.text(),
                "enabled": self.cb_enabled.isChecked(),
            })
            self.accept()
        else:
            QtWidgets.QToolTip.showText(self.pos() + self.tableWidget.pos(), "Please supply at least 1 filter rule.")

    def link_callbacks(self):
        self.combo_apply_to_group.currentIndexChanged.connect(self.combo_apply_to_group_callback)

        self.cb_match_any.toggled.connect(
            lambda checked: settings.setValue(
                "filter_edit_dialog/match", "any" if checked
                else settings.value("filter_edit_dialog/match", type=str))
        )

        self.cb_match_all.toggled.connect(
            lambda checked: settings.setValue(
                "filter_edit_dialog/match", "all" if checked
                else settings.value("filter_edit_dialog/match", type=str))
        )

        self.combo_action.currentTextChanged.connect(self.combo_action_changed_callback)

        self.buttonBox.accepted.connect(self.dialog_accept_callback)


class EditFilterDialog(NewFilterDialog):
    """
    A dialog to edit an existing filter
    """
    def __init__(self, mainwindow: QtWidgets.QMainWindow, f: Filter):
        super(EditFilterDialog, self).__init__(mainwindow)

        # Set the initial values based on the existing filter

        # Name
        self.line_name.setText(f["name"])

        # Enabled
        self.cb_enabled.setChecked(f["enabled"])

        # Apply to
        self.combo_apply_to_group.setCurrentText(f["apply_to_group"])
        self.combo_apply_to.setCurrentText(f["apply_to"])

        # Action
        self.combo_action.setCurrentText(f["action"].value)
        self.line_external_program.setText(f["action_external_program"])

        # Match
        if f["match"] == "any":
            self.cb_match_any.setChecked(True)
        elif f["match"] == "all":
            self.cb_match_all.setChecked(True)

        # Rules
        for row, rule in enumerate(f.get_rules_list()):
            fw: FilterRuleWidget = self.tableWidget.cellWidget(row, 0)
            fw.combo_type.setCurrentText(rule["type"])
            fw.combo_target.setCurrentText(rule["target"])
            fw.line_target.setText(rule["text"])
            self.insert_rule()


class FilterTableWidgetItem(QtWidgets.QTableWidgetItem):
    """
    A filter item to add to the table in FiltersWidget
    """
    def __init__(self, f: Filter, *args, **kwargs):
        super(FilterTableWidgetItem, self).__init__(f["name"], *args, **kwargs)
        self.filter_id = f["id"]
        self.name = f["name"]
        self.setToolTip(str(f))
        self.set_enabled_status(f["enabled"])

    def set_enabled_status(self, enabled: bool):
        brush = QtGui.QBrush() if enabled else QtGui.QBrush(QtGui.QColor(115, 115, 115))
        self.setForeground(brush)


class FiltersWidget(QtWidgets.QDialog, Ui_Form_Filters):
    """
    Widget that lists the existing filters in a table,
    allows creating new, editing and deleting filters.
    """
    def __init__(self, mainwindow: QtWidgets.QMainWindow):
        super(FiltersWidget, self).__init__()
        self.setupUi(self)

        self.mainwindow = mainwindow
        self.filters = Filters()

        self.initUI()

    def initUI(self):
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        horizontal_header = self.tableWidget.horizontalHeader()
        horizontal_header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        vertical_header = self.tableWidget.verticalHeader()
        vertical_header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Fixed)
        vertical_header.setDefaultSectionSize(30)

        self.list_filters()

        self.setWindowTitle("Filters")
        center_widget(self.mainwindow, self)

        self.link_callbacks()

    def list_filters(self):
        self.tableWidget.setRowCount(0)
        # Retrieve existing filters and fill the table
        for f in self.filters.get_filters():
            self.table_insert_filter(f)

    def table_insert_filter(self, f: Filter) -> int:
        new_row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(new_row)
        self.tableWidget.setItem(new_row, 0, FilterTableWidgetItem(f))
        return new_row

    def new_filter_callback(self):
        filter_dialog = NewFilterDialog(self.mainwindow)
        accepted = filter_dialog.exec()
        if accepted:
            # store the new filter entry
            f = Filter(
                name=filter_dialog.filter_properties["name"],
                enabled=filter_dialog.filter_properties["enabled"],
                apply_to_group=filter_dialog.filter_properties["apply_to_group"],
                apply_to=filter_dialog.filter_properties["apply_to"],
                match=filter_dialog.filter_properties["match"],
                action=filter_dialog.filter_properties["action"],
                rules=filter_dialog.filter_properties["rules"],
                action_external_program=filter_dialog.filter_properties["action_external_program"],
            )
            self.filters.store_filter(f)

            self.tableWidget.selectRow(self.table_insert_filter(f))

    def edit_filter_callback(self, fw: FilterTableWidgetItem = None):
        if not fw:
            fw: FilterTableWidgetItem = self.tableWidget.item(self.tableWidget.currentRow(), 0)
            if not fw:
                return
        filter_dialog = EditFilterDialog(self.mainwindow, self.filters.get_filter(fw.filter_id))
        accepted = filter_dialog.exec()
        if accepted:
            # update the filter entry
            f = Filter(
                name=filter_dialog.filter_properties["name"],
                enabled=filter_dialog.filter_properties["enabled"],
                apply_to_group=filter_dialog.filter_properties["apply_to_group"],
                apply_to=filter_dialog.filter_properties["apply_to"],
                match=filter_dialog.filter_properties["match"],
                action=filter_dialog.filter_properties["action"],
                rules=filter_dialog.filter_properties["rules"],
                action_external_program=filter_dialog.filter_properties["action_external_program"],
                filter_id=fw.filter_id
            )
            self.filters.update_filter(f)

            self.list_filters()

    def delete_filter_callback(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row >= 0:
            tw: FilterTableWidgetItem = self.tableWidget.item(selected_row, 0)

            response = QtWidgets.QMessageBox.warning(
                self.mainwindow,
                "Are you sure?",
                f"Delete filter \"{tw.name}\"?",
                QtWidgets.QMessageBox.StandardButton.Ok | QtWidgets.QMessageBox.StandardButton.Cancel,
                defaultButton=QtWidgets.QMessageBox.StandardButton.Cancel
            )
            if response != QtWidgets.QMessageBox.StandardButton.Ok:
                return

            # Delete from database
            self.filters.delete_filter(tw.filter_id)

            # Delete from the table
            self.tableWidget.removeRow(selected_row)

    def keyPressEvent(self, e: QtGui.QKeyEvent) -> None:
        if e.key() == QtCore.Qt.Key.Key_Delete:
            self.delete_filter_callback()
        elif e.key() == QtCore.Qt.Key.Key_Escape:
            pass
        else:
            e.accept()

    def link_callbacks(self):
        self.pb_new.clicked.connect(self.new_filter_callback)
        self.pb_edit.clicked.connect(self.edit_filter_callback)
        self.pb_delete.clicked.connect(self.delete_filter_callback)

        self.tableWidget.itemDoubleClicked.connect(self.edit_filter_callback)
        self.tableWidget.keyPressEvent = self.keyPressEvent


class FiltersDialog(QtWidgets.QDialog):
    def __init__(self, mainwindow: QtWidgets.QMainWindow):
        super(FiltersDialog, self).__init__()

        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setFrameStyle(QtWidgets.QFrame.Shape.NoFrame)
        self.scrollArea.setWidget(FiltersWidget(self))

        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.addWidget(self.scrollArea)

        self.setWindowTitle("Filters")
        self.setMinimumWidth(250)
        center_widget(mainwindow, self)
