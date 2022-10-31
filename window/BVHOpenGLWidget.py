import OpenGL.GL as gl
import sys
import PySide6
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtOpenGLWidgets import QOpenGLWidget

from typing import Optional

from render import *

class BVHOpenGLWidget(QOpenGLWidget):
    def __init__(self, parent: Optional[PySide6.QtWidgets.QWidget] = None, f: PySide6.QtCore.Qt.WindowType = None) -> None:
        super().__init__(parent)
        self.gl_renderer: GLRenderer
        self.frame: Optional[int] = None
        self.enable_orbit: bool = False
        self.enable_panning: bool = False
        self.mouse_pose_x = None
        self.mouse_pose_y = None

    def initializeGL(self) -> None:
        # self.qglClearColor(QtGui.QColor(50, 50, 50)) # initialize the screen to blue
        gl.glClearColor(0.2, 0.2, 0.2, 1.0)
        # gl.glClear(gl.GL_COLOR_BUFFER_BIT|gl.GL_DEPTH_BUFFER_BIT)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)

    def paintGL(self) -> None:
        self.gl_renderer.gl_render(self.frame)
        
    def resizeGL(self, w: int, h: int) -> None:
        if sys.platform == 'linux':
            self.gl_renderer.set_viewport_size(w, h)
        else:
            self.gl_renderer.set_viewport_size(2*w, 2*h)

    def mousePressEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.enable_panning = False
            self.enable_orbit = True
            self.mouse_pose_x = event.x()
            self.mouse_pose_y = event.y()
        elif event.button() == Qt.MouseButton.RightButton:
            self.enable_orbit = False
            self.enable_panning = True
            self.mouse_pose_x = event.x()
            self.mouse_pose_y = event.y()

    def mouseMoveEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        if self.enable_orbit:
            self.gl_renderer.gl_camera.orbit(self.mouse_pose_x - event.x(),
                                             self.mouse_pose_y - event.y(), 0.003)
            self.mouse_pose_x = event.x()
            self.mouse_pose_y = event.y()
            self.update()
        elif self.enable_panning:
            self.gl_renderer.gl_camera.panning(self.mouse_pose_x - event.x(),
                                             self.mouse_pose_y - event.y(), 0.001)
            self.mouse_pose_x = event.x()
            self.mouse_pose_y = event.y()
            self.update()

    def mouseReleaseEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton and self.enable_orbit:
            self.enable_orbit = False
            self.mouse_pose_x = None
            self.mouse_pose_y = None
        elif event.button() == Qt.MouseButton.RightButton and self.enable_panning:
            self.enable_panning = False
            self.mouse_pose_x = None
            self.mouse_pose_y = None

    def init_render(self, gl_renderer:GLRenderer) -> None:
        self.gl_renderer = gl_renderer

    def wheelEvent(self, event: PySide6.QtGui.QWheelEvent) -> None:
        self.gl_renderer.gl_camera.zoomming(event.angleDelta().y()* 0.01)
        self.update()





    

