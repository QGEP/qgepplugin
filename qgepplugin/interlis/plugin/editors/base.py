import os

from collections import defaultdict

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QFont, QBrush, QColor
from qgis.PyQt.QtWidgets import QWidget, QTreeWidgetItem
from qgis.PyQt.uic import loadUi


class Editor():
    """
    Base class to manage import options for QGEP classes.

    Editor subclasses are responsible of:
    - managing a listwidgetitem
    - providing a widget to edit options
    - change the current session objects according to widget interaction
    - validate objects according to the current session
    """

    INVALID = 'INVALID'
    UNKNOWN = 'UNKNOWN'
    WARNING = 'WARNING'
    VALID = 'VALID'

    class_name = 'base'
    widget_name = 'base.ui'

    registry = defaultdict(lambda: Editor)

    def __init_subclass__(cls):
        """
        Populates Editor.registry
        """
        Editor.registry[cls.class_name] = cls

    @staticmethod
    def factory(main_dialog, session, obj):
        """
        Creates an Editor instance, choosing the correct subclass from the registry
        """
        editor_class = Editor.registry[obj.__class__.__name__]
        return editor_class(main_dialog, session, obj)

    def __init__(self, main_dialog, session, obj):
        self.main_dialog = main_dialog
        self.session = session
        self.obj = obj

        self.validate()

    @property
    def listitem(self):
        """
        The editor's listitem (created on the fly if needed)
        """
        if not hasattr(self, '_listitem'):
            self._listitem = QTreeWidgetItem()
            self._listitem.setCheckState(0, Qt.Checked if self.initially_checked() else Qt.Unchecked)
            self.update_listitem()
        return self._listitem

    def update_listitem(self):
        self.listitem.setText(0, getattr(self.obj, "identifier", self.obj.obj_id))
        self.listitem.setText(1, self.validity)
        if self.validity == Editor.INVALID:
            color = "red"
        elif self.validity == Editor.WARNING:
            color = "orange"
        elif self.validity == Editor.VALID:
            color = "lightgreen"
        else:
            color = "lightgray"
        self.listitem.setToolTip(0, str(self.obj.obj_id))
        self.listitem.setBackground(1, QBrush(QColor(color)))

    @property
    def widget(self):
        """
        The editor's widget (created on the fly if needed)
        """
        if not hasattr(self, '_widget'):
            class BaseWidget(QWidget):
                pass
            self._widget = BaseWidget()
            loadUi(os.path.join(os.path.dirname(__file__), self.widget_name), self._widget)
            self.init_widget()
        return self._widget

    def init_widget(self):
        """
        Initialize the widget here, for things like connecting signals... To be overriden by subclasses.
        """
        pass

    def update_widget(self):
        """
        Update the widget here, for things like repopulating from session... To be overriden by subclasses.
        """
        pass

    def validate(self):
        """
        Updates validity and message. To be overriden by subclasses.
        """
        self.validity = Editor.VALID
        self.message = "No validity check"

    def initially_checked(self):
        """
        Determines if the item must be initially checked. To be overriden by subclasses.
        """
        return True
