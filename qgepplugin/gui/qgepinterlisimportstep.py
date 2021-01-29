from sqlalchemy.orm import Session
from sqlalchemy import inspect
from collections import defaultdict

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QFont
from qgis.PyQt.QtWidgets import QDialog, QTreeWidgetItem


from ..utils import get_ui_class


class QgepInterlisImportStepDialog(QDialog, get_ui_class('qgepinterlisimportstep.ui')):

    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)

        self.treeWidget.itemChanged.connect(self.propagate_item_changed)

    def execute_for_session(self, session: Session):
        self.treeWidget.clear()

        category_items = defaultdict(QTreeWidgetItem)
        instances_items = defaultdict(QTreeWidgetItem)

        bold_font = QFont(QFont().defaultFamily(), weight=QFont.Weight.Bold)

        for obj in session:
            cls = obj.__class__

            if cls not in category_items:
                category_items[cls].setText(0, cls.__name__)
                category_items[cls].setCheckState(0, Qt.Checked)
                category_items[cls].setFont(0, bold_font)
                self.treeWidget.addTopLevelItem(category_items[cls])

            status_names = []
            for status_name in ['transient', 'pending', 'persistent', 'deleted', 'detached', 'modified', 'expired']:
                if getattr(inspect(obj), status_name):
                    status_names.append(status_name)
            status_disp = ' '.join(status_names)

            instances_items[obj].setText(0, obj.obj_id)
            instances_items[obj].setText(1, status_disp)
            instances_items[obj].setCheckState(0, Qt.Checked)
            category_items[cls].addChild(instances_items[obj])

        # Show counts
        for category_item in category_items.values():
            category_item.setText(0, f"{category_item.text(0)} ({category_item.childCount()})")

        # Exectute
        accepted = self.exec_()
        if accepted:
            # Expunge unchecked objects form the session
            for obj in session:
                if instances_items[obj].checkState(0) != Qt.Checked:
                    session.expunge(obj)
            return True
        else:
            return False

    def propagate_item_changed(self, item, column):
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
