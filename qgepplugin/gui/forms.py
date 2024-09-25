import qgis
from qgis.core import QgsProject
from qgis.PyQt.QtWidgets import QPushButton

from ..tools.qgepmaptooladdfeature import QgepMapToolDigitizeDrainageChannel


def geometryDigitized(fid, layer, tool):
    layer.changeGeometry(fid, tool.geometry)
    layer.triggerRepaint()
    tool.deactivate()


def mapToolDeactivated(tool):
    tool.deactivated.disconnect()
    qgis.utils.plugins["qgepplugin"].iface.mapCanvas().unsetMapTool(tool)
    tool.deleteLater()


def digitizeDrainageChannel(fid, layerid):
    layer = QgsProject.instance().mapLayer(layerid)
    layer.startEditing()
    tool = QgepMapToolDigitizeDrainageChannel(qgis.utils.plugins["qgepplugin"].iface, layer)
    qgis.utils.plugins["qgepplugin"].iface.mapCanvas().setMapTool(tool)

    def on_geometry_digitized():
        geometryDigitized(fid, layer, tool)

    def on_tool_deactivated():
        mapToolDeactivated(tool)

    tool.geometryDigitized.connect(on_geometry_digitized)
    # form.window().hide()
    tool.deactivated.connect(on_tool_deactivated)


def manholeOpen(form, layer, feature):
    button = form.findChild(QPushButton, "btn_digitize_drainage_channel")

    try:
        button.clicked.disconnect()
    except TypeError:
        pass

    def digitize():
        digitizeDrainageChannel(form, feature, layer)

    def enable_button():
        button.setEnabled(True)

    def disable_button():
        button.setEnabled(False)

    if feature.isValid():
        button.clicked.connect(digitize)
        button.setEnabled(layer.isEditable())

        layer.editingStarted.connect(enable_button)
        layer.editingStopped.connect(disable_button)

        def cleanup():
            layer.editingStarted.disconnect(enable_button)
            layer.editingStopped.disconnect(disable_button)

        form.destroyed.connect(cleanup)
    else:
        button.setEnabled(False)
