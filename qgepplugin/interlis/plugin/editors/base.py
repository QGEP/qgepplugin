import os

from collections import defaultdict

from qgis.PyQt.QtWidgets import QWidget
from qgis.PyQt.uic import loadUi


class Editor():
    """
    Base class to manage import options for QGEP classes.

    Editor subclasses are responsible of:
    - providing a widget to edit options
    - change the current session objects according to widget interaction
    - validate objects according to the current session
    """

    INVALID = 'INVALID'
    UNKNOWN = 'UNKNOWN'
    WARNING = 'WARNING'
    VALID = 'VALID'

    class_name = 'base'

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
    def widget(self):
        """
        The editor's widget (created on the fly if needed)
        """
        if not hasattr(self, '_widget'):
            class BaseWidget(QWidget):
                pass
            self._widget = BaseWidget()
            loadUi(os.path.join(os.path.dirname(__file__), f'{self.class_name}.ui'), self._widget)
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
        self.validity = Editor.UNKNOWN
        self.message = "No validity check"
