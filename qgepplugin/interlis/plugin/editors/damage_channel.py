from sqlalchemy.orm import aliased

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QListWidgetItem

from qgis.utils import iface
from qgis.core import QgsProject, QgsFeature

from ...qgep.model_qgep import get_qgep_model
from .base import Editor


class DamageChannelEditor(Editor):

    class_name = 'damage_channel'

    def initially_checked(self):
        """
        Determines if the item must be initially checked. To be overriden by subclasses.
        """
        print(f"Checking {self.obj.channel_damage_code}")
        if self.obj.channel_damage_code == 4076:  # BCD
            print("no")
            return False
        print("yes")
        return True
