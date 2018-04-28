from PyQt4.QtGui import QPushButton
import qgis
from qgis.core import QgsProject

from ..tools.qgepmaptooladdfeature import QgepMapToolDigitizeDrainageChannel

DEBUGMODE = 1


def geometryDigitized(fid, layer, tool):
    layer.changeGeometry(fid, tool.geometry)
    layer.triggerRepaint()
    tool.deactivate()


def mapToolDeactivated(tool):
    if qgis.utils.plugins['qgepplugin'].iface.mapCanvas().mapTool() == tool:
        qgis.utils.plugins['qgepplugin'].iface.mapCanvas().unsetMapTool(tool)

    tool.deleteLater()


def digitizeDrainageChannel(fid, layerid):
    layer = QgsProject.instance().mapLayer(layerid)
    layer.startEditing()
    tool = QgepMapToolDigitizeDrainageChannel(
        qgis.utils.plugins['qgepplugin'].iface, layer)
    qgis.utils.plugins['qgepplugin'].iface.mapCanvas().setMapTool(tool)
    tool.geometryDigitized.connect(
        lambda: geometryDigitized(fid, layer, tool)
    )
    # form.window().hide()
    tool.deactivated.connect(
        lambda: mapToolDeactivated(tool)
    )


def manholeOpen(form, layer, feature):
    btn = form.findChild(QPushButton, 'btn_digitize_drainage_channel')

    try:
        btn.clicked.disconnect()
    except TypeError:
        pass

    if feature.isValid():
        btn.clicked.connect(
            lambda: digitizeDrainageChannel(form, feature, layer)
        )
        btn.setEnabled(layer.isEditable())

        enable_button = lambda: btn.setEnabled(True)  # NOQA
        disable_button = lambda: btn.setEnabled(False)  # NOQA

        layer.editingStarted.connect(
            enable_button
        )
        layer.editingStopped.connect(
            disable_button
        )
        form.destroyed.connect(
            lambda: layer.editingStarted.disconnect(enable_button))
        form.destroyed.connect(
            lambda: layer.editingStopped.disconnect(disable_button))
    else:
        btn.setEnabled(False)
