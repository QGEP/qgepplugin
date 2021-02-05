import os

from sqlalchemy.orm import Session
from sqlalchemy import inspect
from collections import defaultdict

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QFont
from qgis.PyQt.QtWidgets import QDialog, QTreeWidgetItem, QLineEdit, QWidget, QVBoxLayout, QLabel
from qgis.PyQt.uic import loadUiType, loadUi

from ..qgep.model_qgep import QGEP


def uipath(name):
    return os.path.join(os.path.dirname(__file__), name)


class Gui(QDialog):

    def __init__(self, parent):
        super().__init__(parent)
        loadUi(uipath('gui.ui'), self)

        self.treeWidget.itemChanged.connect(self.item_changed)
        self.treeWidget.currentItemChanged.connect(self.current_item_changed)

    def execute_for_session(self, session: Session):
        """
        Populates the dialog with data from a session, and executes the dialog allowing to filter the rows to import
        """
        self.session = session

        self.category_items = defaultdict(QTreeWidgetItem)
        self.instances_items = defaultdict(QTreeWidgetItem)
        bold_font = QFont(QFont().defaultFamily(), weight=QFont.Weight.Bold)

        # Populate the tree widget
        self.treeWidget.clear()
        for obj in self.session:
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
            for obj in self.session:
                if self.instances_items[obj].checkState(0) != Qt.Checked:
                    self.session.expunge(obj)
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
        current_widget = self.stackedWidget.currentWidget()
        if current_widget:
            self.stackedWidget.removeWidget(current_widget)
            del current_widget

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
        editor = Editor.registry[obj.__class__.__name__](self.session, obj)
        new_widget = editor.make_widget()
        self.stackedWidget.addWidget(new_widget)
        self.stackedWidget.setCurrentWidget(new_widget)


class Editor():
    class_name = 'undefined'

    registry = defaultdict(lambda: Editor)

    def __init_subclass__(cls):
        Editor.registry[cls.class_name] = cls

    def __init__(self, session, obj):
        self.session = session
        self.obj = obj

    def make_widget(self):
        class BaseWidget(QWidget):
            pass
        self.widget = BaseWidget()
        loadUi(uipath(os.path.join('editwidgets',f'{self.class_name}.ui')), self.widget)
        self.init_widget()

    def init_widget(self):
        pass

class ExaminationEditor(Editor):

    class_name = 'examination'

    def init_widget(self):
        self.widget.pushButton.pressed.connect(self.assign_random)
        self.update_widget()

    def update_widget(self):
        self.widget.plainTextEdit.clear()
        for aaa in obj.

    def assign_random(self):
        QGEP.
        self.session.add()
        self.update_widget()

