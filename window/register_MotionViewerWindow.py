
import os
from PySide6.QtDesigner import QPyDesignerCustomWidgetCollection
from window import MotionViewerWindow, BVHOpenGLWidget

if __name__ == '__main__':
    ui_file = open(os.path.dirname(os.path.realpath(__file__)) + '/window/main_window.ui', 'r')
    xml = ui_file.read()
    ui_file.close()
    # print(xml)
    QPyDesignerCustomWidgetCollection.registerCustomWidget(MotionViewerWindow, xml=xml)
    # QPyDesignerCustomWidgetCollection.registerCustomWidget(BVHOpenGLWidget, xml=xml)