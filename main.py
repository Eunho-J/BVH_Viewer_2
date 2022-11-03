import PySide6
import sys, os

# from PySide6.QtDesigner import QPyDesignerCustomWidgetCollection
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication
from PySide6 import QtCore

from window import MotionViewerWindow, BVHOpenGLWidget

os.environ["PYSIDE_DESIGNER_PLUGINS"] = os.path.dirname(os.path.realpath(__file__))+"/window"

if sys.platform == 'linux':
    os.environ["LLVM_INSTALL_DIR"] = os.path.dirname(os.path.realpath(__file__))+"/../libclang/ubuntu"
elif sys.platform == 'darwin':
    os.environ["LLVM_INSTALL_DIR"] = os.path.dirname(os.path.realpath(__file__))+"/../libclang/macos"

print("LLVM_INSTALL_DIR:", os.environ["LLVM_INSTALL_DIR"])


def main():
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QApplication()
    loader = QUiLoader()
    loader.registerCustomWidget(MotionViewerWindow)
    loader.registerCustomWidget(BVHOpenGLWidget)
    main_window: MotionViewerWindow = loader.load(os.path.dirname(os.path.realpath(__file__)) + '/window/main_window.ui')
    # main_window = MotionViewerWindow()
    main_window.init_ui()
    main_window.show()
    app.exec()



if __name__ == '__main__':
    main()