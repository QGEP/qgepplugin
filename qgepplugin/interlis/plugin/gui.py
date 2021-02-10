import os

from sqlalchemy.orm import Session
from sqlalchemy import inspect
from collections import defaultdict

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QFont
from qgis.PyQt.QtWidgets import QDialog, QTreeWidgetItem
from qgis.PyQt.uic import loadUi
from qgis.utils import iface
from qgis.core import Qgis

from .editors.base import Editor

class Gui(QDialog):

    def __init__(self, parent):
        super().__init__(parent)
        loadUi(os.path.join(os.path.dirname(__file__), 'gui.ui'), self)

        self.accepted.connect(self.commit_session)
        self.rejected.connect(self.rollback_session)

    def init_with_session(self, session: Session):
        """
        Shows the dialog with data from a session, and executes the dialog allowing to filter the rows to import
        """
        self.session = session

        self.category_items = defaultdict(QTreeWidgetItem)  # keys are instances' classes
        self.instances_items = defaultdict(QTreeWidgetItem)  # keys are instances

        self.treeWidget.itemChanged.connect(self.item_changed)
        self.treeWidget.currentItemChanged.connect(self.current_item_changed)

        self.treeWidget.clear()
        self.update_tree()

        # Execute the dialog
        self.show()

    def update_tree(self):
        """
        Populates the tree, creating/updating items
        """

        for obj in self.session:
            cls = obj.__class__

            if cls not in self.category_items:
                self.category_items[cls].setText(0, cls.__name__)
                self.category_items[cls].setCheckState(0, Qt.Checked)
                self.category_items[cls].setFont(0, QFont(QFont().defaultFamily(), weight=QFont.Weight.Bold))
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
        for cls, category_item in self.category_items.items():
            category_item.setText(0, f"{cls.__name__} ({category_item.childCount()})")

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
        current_widget = self.stackedWidget.currentWidget()
        if current_widget:
            self.stackedWidget.removeWidget(current_widget)
            del current_widget

        if not current_item:
            return

        obj = None
        for obj, item in self.instances_items.items():
            if item == current_item:
                break

        if obj is None:
            self.debugTextEdit.append("Not found")
            return

        # Show all attributes in the debug text edit
        for c in inspect(obj).mapper.column_attrs:
            val = getattr(obj, c.key)
            self.debugTextEdit.append(f"{c.key}: {val}")

        # Instantiate the specific widget
        editor = Editor.registry[obj.__class__.__name__](self, self.session, obj)
        self.stackedWidget.addWidget(editor.widget)
        self.stackedWidget.setCurrentWidget(editor.widget)

    def commit_session(self):
        # Expunge unchecked objects form the session
        for obj in self.session:
            if self.instances_items[obj].checkState(0) != Qt.Checked:
                self.session.expunge(obj)

        # TODO : rollback to pre-commit state, allowing user to try to fix issues
        # probably a matter of creating a savepoint before saving with
        # session.begin_nested() and one additionnal self.session.commit()
        self.session.commit()
        self.session.close()
        iface.messageBar().pushMessage("Sucess", "Data successfully imported", level=Qgis.Success)

    def rollback_session(self):
        self.session.rollback()
        self.session.close()
        iface.messageBar().pushMessage("Error", "Import was canceled", level=Qgis.Warning)
