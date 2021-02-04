import os

from sqlalchemy.orm import Session
from sqlalchemy import inspect
from collections import defaultdict

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QFont
from qgis.PyQt.QtWidgets import QDialog, QTreeWidgetItem
from qgis.PyQt.uic import loadUiType


UI_FILE = os.path.join(os.path.dirname(__file__), 'gui.ui')


class Gui(QDialog, loadUiType(UI_FILE)[0]):

    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)

        self.treeWidget.itemChanged.connect(self.item_changed)
        self.treeWidget.currentItemChanged.connect(self.current_item_changed)

    def execute_for_session(self, session: Session):
        """
        Populates the dialog with data from a session, and executes the dialog allowing to filter the rows to import
        """

        self.category_items = defaultdict(QTreeWidgetItem)
        self.instances_items = defaultdict(QTreeWidgetItem)
        bold_font = QFont(QFont().defaultFamily(), weight=QFont.Weight.Bold)

        # Populate the tree widget
        self.treeWidget.clear()
        for obj in session:
            cls = obj.__class__

            if cls not in self.category_items:
                self.category_items[cls].setText(0, cls.__name__)
                self.category_items[cls].setCheckState(0, Qt.Checked)
                self.category_items[cls].setFont(0, bold_font)
                self.treeWidget.addTopLevelItem(self.category_items[cls])

            status_names = []
            for status_name in ['transient', 'pending', 'persistent', 'deleted', 'detached', 'modified', 'expired']:
                if getattr(inspect(obj), status_name):
                    status_names.append(status_name)
            status_disp = ' '.join(status_names)

            self.instances_items[obj].setText(0, obj.obj_id)
            self.instances_items[obj].setText(1, status_disp)
            self.instances_items[obj].setCheckState(0, Qt.Checked)
            self.category_items[cls].addChild(self.instances_items[obj])

        # Show counts
        for category_item in self.category_items.values():
            category_item.setText(0, f"{category_item.text(0)} ({category_item.childCount()})")

        # Execute the dialog
        if self.exec_():
            # Expunge unchecked objects form the session
            for obj in session:
                if self.instances_items[obj].checkState(0) != Qt.Checked:
                    session.expunge(obj)
            # User confirmed, we return True to indicate we want a commit
            return True
        else:
            # User canceled, we return False to indicate we want a rollback
            return False

    def item_changed(self, item, column):
        """
        Propagate checkboxes to parent/children
        """

        checked_state = item.checkState(0)

        if checked_state == Qt.PartiallyChecked:
            return

        # propagate to children
        for child in [item.child(i) for i in range(item.childCount())]:
            child.setCheckState(0, checked_state)

        # propagate to parent
        parent = item.parent()
        if parent:
            has_checked = False
            has_unchecked = False
            for sibling in [parent.child(i) for i in range(parent.childCount())]:
                if sibling.checkState(0) == Qt.Checked:
                    has_checked = True
                if sibling.checkState(0) == Qt.Unchecked:
                    has_unchecked = True
                if has_checked and has_unchecked:
                    break

            if has_checked and has_unchecked:
                parent.setCheckState(0, Qt.PartiallyChecked)
            elif has_checked:
                parent.setCheckState(0, Qt.Checked)
            elif has_unchecked:
                parent.setCheckState(0, Qt.Unchecked)
            else:
                # no children at all !!
                parent.setCheckState(0, Qt.PartiallyChecked)

    def current_item_changed(self, current_item, previous_item):
        """
        Populates the details pane
        """

        self.debugTextEdit.clear()
        obj = None
        for obj, item in self.instances_items.items():
            if item == current_item:
                break

        if obj:
            for c in inspect(obj).mapper.column_attrs:
                val = getattr(obj, c.key)
                self.debugTextEdit.append(f"{c.key}: {val}")
        else:
            self.debugTextEdit.append("Not found")
