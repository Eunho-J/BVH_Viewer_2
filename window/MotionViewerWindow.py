from typing import List, Optional

import PySide6
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QLabel, QMenuBar, QStatusBar, QComboBox, QMainWindow, QPushButton
from PySide6.QtWidgets import QCheckBox, QSpinBox, QSlider, QTabWidget, QWidget, QTreeWidget, QTreeWidgetItem
from PySide6.QtWidgets import QToolButton, QDoubleSpinBox


from obj import *
from customparser import BVHParser
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

        #Particle
        self.checkBox_particle_enable: QCheckBox
        self.checkBox_particle_step: QCheckBox

        #Particle: delete
        self.comboBox_particle_delete: QComboBox
        self.toolButton_particle_delete: QToolButton

        #Particle: Simple
        self.doubleSpinBox_particle_simple_mass: QDoubleSpinBox
        self.doubleSpinBox_particle_simple_x: QDoubleSpinBox
        self.doubleSpinBox_particle_simple_y: QDoubleSpinBox
        self.doubleSpinBox_particle_simple_z: QDoubleSpinBox
        self.checkBox_particle_simple_collision: QCheckBox
        self.checkBox_particle_simple_pinned: QCheckBox
        self.comboBox_particle_simple_write: QComboBox
        self.toolButton_particle_simple_write: QToolButton

        #Particle: Cube
        self.doubleSpinBox_particle_cube_mass: QDoubleSpinBox
        self.doubleSpinBox_particle_cube_size: QDoubleSpinBox
        self.doubleSpinBox_particle_cube_x: QDoubleSpinBox
        self.doubleSpinBox_particle_cube_y: QDoubleSpinBox
        self.doubleSpinBox_particle_cube_z: QDoubleSpinBox
        self.checkBox_particle_cube_collision: QCheckBox
        self.comboBox_particle_cube_write: QComboBox
        self.toolButton_particle_cube_write: QToolButton
        self.doubleSpinBox_particle_cube_kd: QDoubleSpinBox
        self.doubleSpinBox_particle_cube_ks: QDoubleSpinBox

        #Collider: Plane
        self.doubleSpinBox_particle_plane_norm_x: QDoubleSpinBox
        self.doubleSpinBox_particle_plane_norm_y: QDoubleSpinBox
        self.doubleSpinBox_particle_plane_norm_z: QDoubleSpinBox
        self.doubleSpinBox_particle_plane_passpoint_x: QDoubleSpinBox
        self.doubleSpinBox_particle_plane_passpoint_y: QDoubleSpinBox
        self.doubleSpinBox_particle_plane_passpoint_z: QDoubleSpinBox
        self.doubleSpinBox_particle_plane_k: QDoubleSpinBox
        self.doubleSpinBox_particle_plane_myu: QDoubleSpinBox
        self.checkBox_particle_plane_collision: QCheckBox
        self.checkBox_particle_plane_contact: QCheckBox
        self.comboBox_particle_plane_write: QComboBox
        self.toolButton_particle_plane_write: QToolButton

        #Particle: Spring
        self.comboBox_particle_spring_p1: QComboBox
        self.comboBox_particle_spring_p2: QComboBox
        self.doubleSpinBox_particle_spring_length: QDoubleSpinBox
        self.doubleSpinBox_particle_spring_ks: QDoubleSpinBox
        self.doubleSpinBox_particle_spring_kd: QDoubleSpinBox
        self.comboBox_particle_spring_write: QComboBox
        self.toolButton_particle_spring_write: QToolButton
        
        self.particles: List[Particle] = []
        self.cubes: List[List[Particle]] = []
        self.springs: List[Damped_Spring_Force] = []
        self.planes: List[Infinite_Plane_Collider] = []
        # parse objects
        self.bvh_parser: BVHParser = BVHParser()

        self.frame_time: int = 8
        self.max_frame: int = 0

    def _next_frame(self):
        if self.openGLWidget.frame is not None:
            self.openGLWidget.frame += 1
            if self.max_frame < self.openGLWidget.frame:
                self.openGLWidget.frame = 0

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

    def _particle_simple_write(self):
        particle: Optional[Particle] = self.comboBox_particle_simple_write.currentData()
        mass: float = self.doubleSpinBox_particle_simple_mass.value()
        pos_x: float = self.doubleSpinBox_particle_simple_x.value()
        pos_y: float = self.doubleSpinBox_particle_simple_y.value()
        pos_z: float = self.doubleSpinBox_particle_simple_z.value()
        position: np.ndarray = np.array([pos_x, pos_y, pos_z, 1], dtype=np.float64)
        collision = self.checkBox_particle_simple_collision.isChecked()
        pinned = self.checkBox_particle_simple_pinned.isChecked()
        if particle is None:
            self._particle_add(Particle(mass, position, collision, pinned))
        else:
            particle.overwrite(mass, position, collision, pinned)
        
    def _particle_cube_write(self):
        cube: Optional[List[Particle]] = self.comboBox_particle_cube_write.currentData()
        mass: float = self.doubleSpinBox_particle_cube_mass.value()
        size: float = self.doubleSpinBox_particle_cube_size.value()
        pos_x: float = self.doubleSpinBox_particle_cube_x.value()
        pos_y: float = self.doubleSpinBox_particle_cube_y.value()
        pos_z: float = self.doubleSpinBox_particle_cube_z.value()
        
        ks = self.doubleSpinBox_particle_cube_ks.value()
        kd = self.doubleSpinBox_particle_cube_kd.value()
        collision = self.checkBox_particle_cube_collision.isChecked()
        # pinned = self.checkBox_particle_cube_pinned.isChecked()
        
        mass_per_particle = mass / 8.0
        
        if cube is None:
            cube = []
            for i in range(8):
                position = np.array([pos_x + (i//4 - 0.5) * size,
                                 pos_y + (i%4//2 - 0.5) * size,
                                 pos_z + (i%2 - 0.5) * size,
                                 1], dtype=np.float64)
                self._particle_add(Particle(mass_per_particle, position, collision, False), cube)
            for i in range(7):
                for j in range(i+1,8):
                    self._spring_add(cube[i], cube[j], ks, kd, None, cube)
            name = f"cube {len(self.cubes)}"
            self.cubes.append(cube)
            self._cube_comboBox_add_item(name, cube)
        else:
            # update existing
            pass
                

    def _particle_plane_write(self):
        plane: Optional[Infinite_Plane_Collider] = self.comboBox_particle_plane_write.currentData()
        
        norm_x = self.doubleSpinBox_particle_plane_norm_x.value()
        norm_y = self.doubleSpinBox_particle_plane_norm_y.value()
        norm_z = self.doubleSpinBox_particle_plane_norm_z.value()
        norm = np.array([norm_x, norm_y, norm_z, 0], np.float64)
        
        passpoint_x = self.doubleSpinBox_particle_plane_passpoint_x.value()
        passpoint_y = self.doubleSpinBox_particle_plane_passpoint_y.value()
        passpoint_z = self.doubleSpinBox_particle_plane_passpoint_z.value()
        passpoint = np.array([passpoint_x, passpoint_y, passpoint_z, 1], dtype=np.float64)
        
        k = self.doubleSpinBox_particle_plane_k.value()
        myu = self.doubleSpinBox_particle_plane_myu.value()
        
        collision = self.checkBox_particle_plane_collision.isChecked()
        contact = self.checkBox_particle_plane_contact.isChecked()
        
        if plane is None:
            self._plane_add(norm, passpoint, k, myu, collision, contact)
            pass
        else:
            # update existing
            pass
        

    def _particle_spring_write(self):
        spring = self.comboBox_particle_spring_write.currentData()
        p1 = self.comboBox_particle_spring_p1.currentData()
        p2 = self.comboBox_particle_spring_p2.currentData()
        r = self.doubleSpinBox_particle_spring_length.value()
        if r == 0.0:
            # set r to initial distance (defalut value)
            r = None
        ks = self.doubleSpinBox_particle_spring_ks.value()
        kd = self.doubleSpinBox_particle_spring_kd.value()
        
        if spring is None:
            self._spring_add(p1, p2, ks, kd, r)
        else:
            # update existing
            pass
        
    def _particle_delete(self):
        pass
    
    def _particle_add(self, particle, parent:Optional[List[Particle]]=None):
        name: str
        particle_id = len(self.particles)
        if parent is None:
            self.particles.append(particle)
            name = f"particle {particle_id}"
        else:
            cube_id = len(self.cubes)
            parent.append(particle)
            name = f"cube {cube_id} - particle {particle_id}"
        
        self.particle_system.append_particle(particle)
        self._particle_comboBox_add_item(name, particle)
            
    def _particle_comboBox_add_item(self, name, particle):
        self.comboBox_particle_spring_p1.addItem(name, particle)
        self.comboBox_particle_spring_p2.addItem(name, particle)
        self.comboBox_particle_simple_write.addItem(name, particle)
        if particle is not None:
            self._particle_dynamics_add_delete(name, particle)
        
    def _cube_comboBox_add_item(self, name, cube):
        self.comboBox_particle_cube_write.addItem(name, cube)
        if cube is not None:
            self._particle_dynamics_add_delete(name, cube)
        
    def _spring_comboBox_add_item(self, name, spring):
        self.comboBox_particle_spring_write.addItem(name, spring)
        if spring is not None:
            self._particle_dynamics_add_delete(name, spring)
        
    def _plane_comboBox_add_item(self, name, plane):
        self.comboBox_particle_plane_write.addItem(name, plane)
        if plane is not None:
            self._particle_dynamics_add_delete(name, plane)
        
    def _particle_dynamics_add_delete(self, name, target):
        self.comboBox_particle_delete.addItem(name, target)
    
    def _spring_add(self, p1, p2, ks, kd, r=None, parent=None):
        spring = Damped_Spring_Force(p1, self.particle_system, p2, ks, kd, r)
        name = ''
        spring_id = len(self.springs)
        if parent is None:
            name = f"spring {spring_id}"
        else:
            cube_id = len(self.cubes)
            name = f"cube {cube_id} - spring {spring_id}"
            
        self.springs.append(spring)
        self.particle_system.append_force(spring)
        self._spring_comboBox_add_item(name, spring)
    
    def _plane_add(self, norm, passpoint, k, myu, collision, contact):
        plane = Infinite_Plane_Collider(norm, passpoint, k, myu, collision, contact)
        plane_id = len(self.planes)
        name = f"plane {plane_id}"
        
        self._plane_comboBox_add_item(name, plane)
        self.planes.append(plane)
        self.particle_system.append_collider(plane)
        
    def _update_particle_dynamics(self):
        if self.checkBox_particle_enable.isChecked():
            if self.checkBox_particle_step.isChecked():
                self.particle_system.semi_implicit_euler_step(self.particle_update_dt)
            else:
                self.particle_system.euler_step(self.particle_update_dt)

    def init_ui(self):
        self.gl_renderer: BVH_GLRenderer = BVH_GLRenderer()
        self.particle_system: Particle_System = self.gl_renderer.particle_system

        self.opengl_update_timer = QTimer(self)
        self.opengl_update_timer.timeout.connect(self._update_glwidget)
        self.opengl_update_timer.setInterval(20)
        self.opengl_update_timer.start()
        
        self.particle_update_timer = QTimer(self)
        self.particle_update_dt = 8
        self.particle_update_timer.timeout.connect(self._update_particle_dynamics)
        self.particle_update_timer.setInterval(self.particle_update_dt)
        self.particle_update_timer.start()

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

        self.toolButton_particle_delete.clicked.connect(self._particle_delete)
        self.toolButton_particle_simple_write.clicked.connect(self._particle_simple_write)
        self.toolButton_particle_cube_write.clicked.connect(self._particle_cube_write)
        self.toolButton_particle_plane_write.clicked.connect(self._particle_plane_write)
        self.toolButton_particle_spring_write.clicked.connect(self._particle_spring_write)
        
        self._particle_comboBox_add_item("None", None)
        self._cube_comboBox_add_item("None", None)
        self._spring_comboBox_add_item("None", None)
        self._plane_comboBox_add_item("None", None)
    
    def keyPressEvent(self, event: PySide6.QtGui.QKeyEvent) -> None:
        key = event.key()
        if key == Qt.Key.Key_Space:
            self.pushButton_play.click()
        elif key == Qt.Key.Key_Escape:
            self.pushButton_stop.click()
        elif key == Qt.Key.Key_V:
            self.checkBox_view_ortho.toggle()
        elif key == Qt.Key.Key_W:
            self.gl_renderer.move_desired_position(np.array([0,0.01,0,0], dtype=np.float64))
        elif key == Qt.Key.Key_S:
            self.gl_renderer.move_desired_position(np.array([0,-0.01,0,0], dtype=np.float64))
        elif key == Qt.Key.Key_Q:
            self.gl_renderer.move_desired_position(np.array([0.01,0,0,0], dtype=np.float64))
        elif key == Qt.Key.Key_A:
            self.gl_renderer.move_desired_position(np.array([-0.01,0,0,0], dtype=np.float64))
        elif key == Qt.Key.Key_E:
            self.gl_renderer.move_desired_position(np.array([0,0,0.01,0], dtype=np.float64))
        elif key == Qt.Key.Key_D:
            self.gl_renderer.move_desired_position(np.array([0,0,-0.01,0], dtype=np.float64))
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
        if joint.parent_depth >= 3:
            self.comboBox_ik_target_joint.addItem(joint.name, joint)
        if parent is None:
            parent = self.treeWidget
        tree_item = QTreeWidgetItem(parent)
        tree_item.setText(0, joint.name)
        for child in joint.children:
            tree_item.addChild(self.get_skeleton_tree_item_recursive(child, tree_item))
        tree_item.setExpanded(True)
        return tree_item
        
        

