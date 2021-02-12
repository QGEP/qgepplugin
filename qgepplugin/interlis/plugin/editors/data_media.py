from sqlalchemy.orm import aliased

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QListWidgetItem

from qgis.utils import iface
from qgis.core import QgsProject, QgsFeature

from ...qgep.model_qgep import get_qgep_model
from .base import Editor


class DataMediaEditor(Editor):

    class_name = 'data_media'

    def __init__(self, *args, **kwargs):
        self._path_was_changed = False
        super().__init__(*args, **kwargs)

    def init_widget(self):
        self.widget.pushButton.pressed.connect(lambda: self.button_clicked())
        self.update_widget()

    def update_widget(self):
        self.widget.lineEdit.setText(self.obj.path)

    def button_clicked(self):
        self.obj.path = self.widget.lineEdit.text()
        self._path_was_changed = True

        self.validate()
        self.main_dialog.refresh_widget_for_obj(self.obj)
        self.main_dialog.update_tree()

    def validate(self):
        if not self._path_was_changed:
            self.validity = Editor.WARNING
            self.message = 'Path was not adapted.'
        else:
            self.validity = Editor.VALID
            self.message = 'No warning'
