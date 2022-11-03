from typing import List, Optional

import PySide6
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QLabel, QMenuBar, QStatusBar, QComboBox, QMainWindow, QPushButton, QCheckBox, QSpinBox, QSlider, QTabWidget, QWidget, QTreeWidget, QTreeWidgetItem


from obj import BVHMotion, Skeleton, Joint
from parser import BVHParser
from window import BVHOpenGLWidget
from render import *
from np import *


class MotionViewerWindow(QMainWindow):
    def __init__(self, parent: Optional[PySide6.QtWidgets.QWidget] = None, flags: PySide6.QtCore.Qt.WindowType = None) -> None:
        super().__init__(parent)
        self.pushButton_play: QPushButton
        self.pushButton_stop: QPushButton
        self.slider_frame: QSlider
        self.spinBox_frame: QSpinBox
        self.label_max_frame: QLabel
        
        self.openGLWidget: BVHOpenGLWidget

        self.tabWidget: QTabWidget

        self.tab_ik: QWidget
        self.checkBox_ik_enable: QCheckBox
        self.comboBox_ik_target_joint: QComboBox
        self.spinBox_ik_target_frame: QSpinBox

        self.tab_view: QWidget
        self.pushButton_view_at_x: QPushButton
        self.pushButton_view_at_y: QPushButton
        self.pushButton_view_at_z: QPushButton
        self.checkBox_view_abs_axis: QCheckBox
        self.checkBox_view_joint_axis: QCheckBox
        self.checkBox_view_ortho: QCheckBox

        self.treeWidget: QTreeWidget
        self.menubar: QMenuBar
        self.statusbar: QStatusBar

        # parse objects
        self.bvh_parser: BVHParser = BVHParser()
        # self.parsed_skeleton: Optional[Skeleton] = None
        # self.parsed_bvh_motion: Optional[BVHMotion] = None

        self.frame_time: int = 8
        self.max_frame: int = 0

    def _next_frame(self):
        if self.openGLWidget.frame is not None:
            self.openGLWidget.frame += 1
            if self.max_frame < self.openGLWidget.frame:
                self.openGLWidget.frame = 0
            # self.slider_frame.setSliderPosition(self.openGLWidget.frame)
            # self.spinBox_frame.setValue(self.openGLWidget.frame)

    def _update_glwidget(self):
        self.openGLWidget.update()
        self.spinBox_frame.setValue(self.openGLWidget.frame if self.openGLWidget.frame is not None else 0)

    def _play(self):
        if self.gl_renderer.get_max_frame() == 0:
            return
        if self.openGLWidget.frame is None and self.pushButton_play.isChecked():
            self.openGLWidget.frame = 0
            self.play_timer.start()
        elif not self.pushButton_play.isChecked():
            self.play_timer.stop()
        else:
            self.play_timer.setInterval(self.frame_time)
            self.play_timer.start()

    def _stop(self):
        if self.pushButton_play.isChecked():
            self.pushButton_play.click()
        self.slider_frame.setSliderPosition(0)
        self.spinBox_frame.setValue(0)
        self.openGLWidget.frame = None

    def _ortho(self):
        if self.checkBox_view_ortho.isChecked():
            self.gl_renderer.set_view_ortho(True)
        else:
            self.gl_renderer.set_view_ortho(False)
        # self.openGLWidget.update()

    def _view_at_x(self):
        self.gl_renderer.gl_camera.view_target_at(0, np.radians(90))
        # self.openGLWidget.update()
    
    def _view_at_y(self):
        self.gl_renderer.gl_camera.view_target_at(np.radians(-90), 0)
        # self.openGLWidget.update()
    
    def _view_at_z(self):
        self.gl_renderer.gl_camera.view_target_at(0, 0)
        # self.openGLWidget.update()

    def _abs_axis(self):
        if self.checkBox_view_abs_axis.isChecked():
            self.gl_renderer.show_abs_axis(True)
        else:
            self.gl_renderer.show_abs_axis(False)
        # self.openGLWidget.update()

    def _joint_axis(self):
        if self.checkBox_view_joint_axis.isChecked():
            self.gl_renderer.show_joint_axis(True)
        else:
            self.gl_renderer.show_joint_axis(False)
        # self.openGLWidget.update()

    def _slider_frame(self):
        new_frame = self.slider_frame.value()
        self.openGLWidget.frame = new_frame
        self.spinBox_frame.setValue(new_frame)

    def _spinbox_frame(self):
        new_frame = self.spinBox_frame.value()
        self.openGLWidget.frame = new_frame
        self.slider_frame.setSliderPosition(new_frame)

    def _ik_target_joint(self):
        selected_joint:Optional[Joint] = self.comboBox_ik_target_joint.currentData()
        self.gl_renderer.set_ik_target_joint(selected_joint)
        if selected_joint is not None:
            print("ik target:", selected_joint.name)
        else:
            print("ik target deselected")

    def _ik_target_frame(self):
        selected_frame:int = self.spinBox_ik_target_frame.value()
        self.gl_renderer.set_ik_target_frame(selected_frame)
        print("ik frame:", selected_frame)

    def _ik_enable(self):
        self.gl_renderer.ik_enabled = self.checkBox_ik_enable.isChecked()
        print("ik enabled:", self.gl_renderer.ik_enabled)
    
    def init_ui(self):
        self.gl_renderer: BVH_GLRenderer = BVH_GLRenderer()

        self.opengl_update_timer = QTimer(self)
        self.opengl_update_timer.timeout.connect(self._update_glwidget)
        self.opengl_update_timer.setInterval(20)
        self.opengl_update_timer.start()

        self.camera: GLCamera = self.gl_renderer.gl_camera
        
        self.openGLWidget.init_render(self.gl_renderer)
        self.pushButton_play.clicked.connect(self._play)
        self.pushButton_stop.clicked.connect(self._stop)

        self.checkBox_view_ortho.toggled.connect(self._ortho)
        self.checkBox_view_abs_axis.toggled.connect(self._abs_axis)
        self.checkBox_view_joint_axis.toggled.connect(self._joint_axis)

        self.pushButton_view_at_x.clicked.connect(self._view_at_x)
        self.pushButton_view_at_y.clicked.connect(self._view_at_y)
        self.pushButton_view_at_z.clicked.connect(self._view_at_z)

        self.slider_frame.valueChanged.connect(self._slider_frame)
        self.spinBox_frame.textChanged.connect(self._spinbox_frame)
        self.play_timer = QTimer(self.openGLWidget)
        self.play_timer.timeout.connect(self._next_frame)

        self.comboBox_ik_target_joint.currentIndexChanged.connect(self._ik_target_joint)
        self.spinBox_ik_target_frame.textChanged.connect(self._ik_target_frame)
        self.checkBox_ik_enable.toggled.connect(self._ik_enable)

    
    def keyPressEvent(self, event: PySide6.QtGui.QKeyEvent) -> None:
        key = event.key()
        if key == Qt.Key.Key_Space:
            self.pushButton_play.click()
        elif key == Qt.Key.Key_Escape:
            self.pushButton_stop.click()
        elif key == Qt.Key.Key_V:
            self.checkBox_view_ortho.toggle()
        elif key == Qt.Key.Key_W:
            self.gl_renderer.move_desired_position(np.array([0,0.01,0,0], dtype=np.float32))
        elif key == Qt.Key.Key_S:
            self.gl_renderer.move_desired_position(np.array([0,-0.01,0,0], dtype=np.float32))
        elif key == Qt.Key.Key_Q:
            self.gl_renderer.move_desired_position(np.array([0.01,0,0,0], dtype=np.float32))
        elif key == Qt.Key.Key_A:
            self.gl_renderer.move_desired_position(np.array([-0.01,0,0,0], dtype=np.float32))
        elif key == Qt.Key.Key_E:
            self.gl_renderer.move_desired_position(np.array([0,0,0.01,0], dtype=np.float32))
        elif key == Qt.Key.Key_D:
            self.gl_renderer.move_desired_position(np.array([0,0,-0.01,0], dtype=np.float32))
        elif key == Qt.Key.Key_R:
            self.gl_renderer.reset_desired_position()

    def dragEnterEvent(self, event: PySide6.QtGui.QDragEnterEvent) -> None:
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: PySide6.QtGui.QDropEvent) -> None:
        self.comboBox_ik_target_joint.clear()
        self.comboBox_ik_target_joint.addItem("Select...", None)
        self.pushButton_stop.click()
        print("parse file: ", event.mimeData().urls()[0].path())
        parsed_skeleton, parsed_bvh_motion = self.bvh_parser.parse_file(event.mimeData().urls()[0].path())
        self.gl_renderer.set_object(parsed_skeleton, parsed_bvh_motion)
        self.max_frame = self.gl_renderer.get_max_frame()
        self.frame_time = int(1000 * self.gl_renderer.get_frame_time())
        print("interval:", self.frame_time)
        self.play_timer.setInterval(self.frame_time)
        self.slider_frame.setMaximum(self.max_frame)
        self.spinBox_frame.setMaximum(self.max_frame)

        self.spinBox_ik_target_frame.setMaximum(self.max_frame)
        self.spinBox_ik_target_frame.setValue(0)
        self.label_max_frame.setText("frames: "+str(self.max_frame))

        self.treeWidget.takeTopLevelItem(0)
        self.treeWidget.addTopLevelItem(self.get_skeleton_tree_item_recursive(parsed_skeleton.root))
        # self.openGLWidget.update()
        
    def get_skeleton_tree_item_recursive(self, joint: Joint, parent:Optional[QTreeWidgetItem] = None) -> QTreeWidgetItem:
        if joint.parent_depth >= 2:
            self.comboBox_ik_target_joint.addItem(joint.name, joint)
        if parent is None:
            parent = self.treeWidget
        tree_item = QTreeWidgetItem(parent)
        tree_item.setText(0, joint.name)
        for child in joint.children:
            tree_item.addChild(self.get_skeleton_tree_item_recursive(child, tree_item))
        tree_item.setExpanded(True)
        return tree_item
        
        
        

