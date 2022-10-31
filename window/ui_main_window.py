# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.4.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QComboBox,
    QFormLayout, QGridLayout, QHBoxLayout, QHeaderView,
    QLabel, QLayout, QMenuBar, QPushButton,
    QSizePolicy, QSlider, QSpinBox, QStatusBar,
    QTabWidget, QTreeWidget, QTreeWidgetItem, QWidget)

from bvhopenglwidget import BVHOpenGLWidget
from motionviewerwindow import MotionViewerWindow

class Ui_MotionViewerWindow(object):
    def setupUi(self, MotionViewerWindow):
        if not MotionViewerWindow.objectName():
            MotionViewerWindow.setObjectName(u"MotionViewerWindow")
        MotionViewerWindow.resize(1206, 721)
        MotionViewerWindow.setFocusPolicy(Qt.StrongFocus)
        MotionViewerWindow.setAcceptDrops(True)
        self.centralwidget = QWidget(MotionViewerWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setGeometry(QRect(0, 0, 1128, 686))
        self.centralwidget.setLayoutDirection(Qt.LeftToRight)
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.layout_status = QHBoxLayout()
        self.layout_status.setObjectName(u"layout_status")
        self.layout_status.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.layout_status.setContentsMargins(0, 0, -1, -1)
        self.pushButton_play = QPushButton(self.centralwidget)
        self.pushButton_play.setObjectName(u"pushButton_play")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_play.sizePolicy().hasHeightForWidth())
        self.pushButton_play.setSizePolicy(sizePolicy)
        self.pushButton_play.setMinimumSize(QSize(36, 36))
        self.pushButton_play.setMaximumSize(QSize(36, 36))
        self.pushButton_play.setFocusPolicy(Qt.NoFocus)
        self.pushButton_play.setCheckable(True)

        self.layout_status.addWidget(self.pushButton_play)

        self.pushButton_stop = QPushButton(self.centralwidget)
        self.pushButton_stop.setObjectName(u"pushButton_stop")
        sizePolicy.setHeightForWidth(self.pushButton_stop.sizePolicy().hasHeightForWidth())
        self.pushButton_stop.setSizePolicy(sizePolicy)
        self.pushButton_stop.setMinimumSize(QSize(36, 36))
        self.pushButton_stop.setMaximumSize(QSize(36, 36))
        self.pushButton_stop.setFocusPolicy(Qt.NoFocus)

        self.layout_status.addWidget(self.pushButton_stop)

        self.slider_frame = QSlider(self.centralwidget)
        self.slider_frame.setObjectName(u"slider_frame")
        self.slider_frame.setMinimumSize(QSize(0, 36))
        self.slider_frame.setMaximumSize(QSize(16777215, 36))
        self.slider_frame.setFocusPolicy(Qt.NoFocus)
        self.slider_frame.setOrientation(Qt.Horizontal)

        self.layout_status.addWidget(self.slider_frame)

        self.spinBox_frame = QSpinBox(self.centralwidget)
        self.spinBox_frame.setObjectName(u"spinBox_frame")
        self.spinBox_frame.setFocusPolicy(Qt.ClickFocus)

        self.layout_status.addWidget(self.spinBox_frame)


        self.gridLayout.addLayout(self.layout_status, 3, 0, 1, 2)

        self.openGLWidget = BVHOpenGLWidget(self.centralwidget)
        self.openGLWidget.setObjectName(u"openGLWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(1)
        sizePolicy1.setHeightForWidth(self.openGLWidget.sizePolicy().hasHeightForWidth())
        self.openGLWidget.setSizePolicy(sizePolicy1)
        self.openGLWidget.setMinimumSize(QSize(640, 640))
        self.openGLWidget.setFocusPolicy(Qt.NoFocus)
        self.openGLWidget.setLayoutDirection(Qt.LeftToRight)

        self.gridLayout.addWidget(self.openGLWidget, 0, 0, 2, 1)

        self.treeWidget = QTreeWidget(self.centralwidget)
        self.treeWidget.setObjectName(u"treeWidget")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.treeWidget.sizePolicy().hasHeightForWidth())
        self.treeWidget.setSizePolicy(sizePolicy2)
        self.treeWidget.setMinimumSize(QSize(280, 0))
        self.treeWidget.setFocusPolicy(Qt.NoFocus)
        self.treeWidget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.treeWidget.setAutoExpandDelay(-1)
        self.treeWidget.setIndentation(10)

        self.gridLayout.addWidget(self.treeWidget, 0, 1, 1, 1)

        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy3)
        self.tabWidget.setFocusPolicy(Qt.NoFocus)
        self.tab_view = QWidget()
        self.tab_view.setObjectName(u"tab_view")
        self.formLayout_view = QFormLayout(self.tab_view)
        self.formLayout_view.setObjectName(u"formLayout_view")
        self.checkBox_view_ortho = QCheckBox(self.tab_view)
        self.checkBox_view_ortho.setObjectName(u"checkBox_view_ortho")
        sizePolicy4 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.checkBox_view_ortho.sizePolicy().hasHeightForWidth())
        self.checkBox_view_ortho.setSizePolicy(sizePolicy4)
        self.checkBox_view_ortho.setFocusPolicy(Qt.NoFocus)

        self.formLayout_view.setWidget(0, QFormLayout.FieldRole, self.checkBox_view_ortho)

        self.label_view_ortho = QLabel(self.tab_view)
        self.label_view_ortho.setObjectName(u"label_view_ortho")

        self.formLayout_view.setWidget(0, QFormLayout.LabelRole, self.label_view_ortho)

        self.label_view_abs_axis = QLabel(self.tab_view)
        self.label_view_abs_axis.setObjectName(u"label_view_abs_axis")

        self.formLayout_view.setWidget(1, QFormLayout.LabelRole, self.label_view_abs_axis)

        self.checkBox_view_abs_axis = QCheckBox(self.tab_view)
        self.checkBox_view_abs_axis.setObjectName(u"checkBox_view_abs_axis")
        sizePolicy4.setHeightForWidth(self.checkBox_view_abs_axis.sizePolicy().hasHeightForWidth())
        self.checkBox_view_abs_axis.setSizePolicy(sizePolicy4)
        self.checkBox_view_abs_axis.setFocusPolicy(Qt.NoFocus)
        self.checkBox_view_abs_axis.setChecked(True)

        self.formLayout_view.setWidget(1, QFormLayout.FieldRole, self.checkBox_view_abs_axis)

        self.label_view_joint_axis = QLabel(self.tab_view)
        self.label_view_joint_axis.setObjectName(u"label_view_joint_axis")

        self.formLayout_view.setWidget(2, QFormLayout.LabelRole, self.label_view_joint_axis)

        self.checkBox_view_joint_axis = QCheckBox(self.tab_view)
        self.checkBox_view_joint_axis.setObjectName(u"checkBox_view_joint_axis")
        sizePolicy4.setHeightForWidth(self.checkBox_view_joint_axis.sizePolicy().hasHeightForWidth())
        self.checkBox_view_joint_axis.setSizePolicy(sizePolicy4)
        self.checkBox_view_joint_axis.setFocusPolicy(Qt.NoFocus)

        self.formLayout_view.setWidget(2, QFormLayout.FieldRole, self.checkBox_view_joint_axis)

        self.label_view_at = QLabel(self.tab_view)
        self.label_view_at.setObjectName(u"label_view_at")

        self.formLayout_view.setWidget(3, QFormLayout.LabelRole, self.label_view_at)

        self.horizontalLayout_view_at = QHBoxLayout()
        self.horizontalLayout_view_at.setObjectName(u"horizontalLayout_view_at")
        self.pushButton_view_at_x = QPushButton(self.tab_view)
        self.pushButton_view_at_x.setObjectName(u"pushButton_view_at_x")
        sizePolicy.setHeightForWidth(self.pushButton_view_at_x.sizePolicy().hasHeightForWidth())
        self.pushButton_view_at_x.setSizePolicy(sizePolicy)
        self.pushButton_view_at_x.setMinimumSize(QSize(32, 18))
        self.pushButton_view_at_x.setMaximumSize(QSize(32, 18))
        self.pushButton_view_at_x.setFocusPolicy(Qt.NoFocus)

        self.horizontalLayout_view_at.addWidget(self.pushButton_view_at_x)

        self.pushButton_view_at_y = QPushButton(self.tab_view)
        self.pushButton_view_at_y.setObjectName(u"pushButton_view_at_y")
        sizePolicy.setHeightForWidth(self.pushButton_view_at_y.sizePolicy().hasHeightForWidth())
        self.pushButton_view_at_y.setSizePolicy(sizePolicy)
        self.pushButton_view_at_y.setMinimumSize(QSize(32, 18))
        self.pushButton_view_at_y.setMaximumSize(QSize(32, 18))
        self.pushButton_view_at_y.setFocusPolicy(Qt.NoFocus)

        self.horizontalLayout_view_at.addWidget(self.pushButton_view_at_y)

        self.pushButton_view_at_z = QPushButton(self.tab_view)
        self.pushButton_view_at_z.setObjectName(u"pushButton_view_at_z")
        sizePolicy.setHeightForWidth(self.pushButton_view_at_z.sizePolicy().hasHeightForWidth())
        self.pushButton_view_at_z.setSizePolicy(sizePolicy)
        self.pushButton_view_at_z.setMinimumSize(QSize(32, 18))
        self.pushButton_view_at_z.setMaximumSize(QSize(32, 18))
        self.pushButton_view_at_z.setFocusPolicy(Qt.NoFocus)

        self.horizontalLayout_view_at.addWidget(self.pushButton_view_at_z)


        self.formLayout_view.setLayout(3, QFormLayout.FieldRole, self.horizontalLayout_view_at)

        self.tabWidget.addTab(self.tab_view, "")
        self.tab_ik = QWidget()
        self.tab_ik.setObjectName(u"tab_ik")
        self.formLayout_ik = QFormLayout(self.tab_ik)
        self.formLayout_ik.setObjectName(u"formLayout_ik")
        self.label_ik_enable = QLabel(self.tab_ik)
        self.label_ik_enable.setObjectName(u"label_ik_enable")

        self.formLayout_ik.setWidget(0, QFormLayout.LabelRole, self.label_ik_enable)

        self.checkbox_ik_enable = QCheckBox(self.tab_ik)
        self.checkbox_ik_enable.setObjectName(u"checkbox_ik_enable")
        sizePolicy4.setHeightForWidth(self.checkbox_ik_enable.sizePolicy().hasHeightForWidth())
        self.checkbox_ik_enable.setSizePolicy(sizePolicy4)
        self.checkbox_ik_enable.setFocusPolicy(Qt.NoFocus)
        self.checkbox_ik_enable.setLayoutDirection(Qt.LeftToRight)

        self.formLayout_ik.setWidget(0, QFormLayout.FieldRole, self.checkbox_ik_enable)

        self.label_ik_target_joint = QLabel(self.tab_ik)
        self.label_ik_target_joint.setObjectName(u"label_ik_target_joint")

        self.formLayout_ik.setWidget(1, QFormLayout.LabelRole, self.label_ik_target_joint)

        self.comboBox_ik_target_joint = QComboBox(self.tab_ik)
        self.comboBox_ik_target_joint.setObjectName(u"comboBox_ik_target_joint")
        sizePolicy5 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.comboBox_ik_target_joint.sizePolicy().hasHeightForWidth())
        self.comboBox_ik_target_joint.setSizePolicy(sizePolicy5)
        self.comboBox_ik_target_joint.setFocusPolicy(Qt.NoFocus)
        self.comboBox_ik_target_joint.setLayoutDirection(Qt.LeftToRight)

        self.formLayout_ik.setWidget(1, QFormLayout.FieldRole, self.comboBox_ik_target_joint)

        self.label_ik_target_frame = QLabel(self.tab_ik)
        self.label_ik_target_frame.setObjectName(u"label_ik_target_frame")

        self.formLayout_ik.setWidget(2, QFormLayout.LabelRole, self.label_ik_target_frame)

        self.spinBox_ik_target_frame = QSpinBox(self.tab_ik)
        self.spinBox_ik_target_frame.setObjectName(u"spinBox_ik_target_frame")
        sizePolicy5.setHeightForWidth(self.spinBox_ik_target_frame.sizePolicy().hasHeightForWidth())
        self.spinBox_ik_target_frame.setSizePolicy(sizePolicy5)
        self.spinBox_ik_target_frame.setFocusPolicy(Qt.ClickFocus)

        self.formLayout_ik.setWidget(2, QFormLayout.FieldRole, self.spinBox_ik_target_frame)

        self.tabWidget.addTab(self.tab_ik, "")

        self.gridLayout.addWidget(self.tabWidget, 1, 1, 1, 1)

        self.menubar = QMenuBar(MotionViewerWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 869, 22))
        self.statusbar = QStatusBar(MotionViewerWindow)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setGeometry(QRect(0, 0, 3, 22))

        self.retranslateUi(MotionViewerWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MotionViewerWindow)
    # setupUi

    def retranslateUi(self, MotionViewerWindow):
        MotionViewerWindow.setWindowTitle(QCoreApplication.translate("MotionViewerWindow", u"BVH Viewer v0.0.1", None))
        self.pushButton_play.setText(QCoreApplication.translate("MotionViewerWindow", u"Play", None))
        self.pushButton_stop.setText(QCoreApplication.translate("MotionViewerWindow", u"Stop", None))
        ___qtreewidgetitem = self.treeWidget.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MotionViewerWindow", u"Skeleton", None));
        self.checkBox_view_ortho.setText("")
        self.label_view_ortho.setText(QCoreApplication.translate("MotionViewerWindow", u"Orthogonal", None))
        self.label_view_abs_axis.setText(QCoreApplication.translate("MotionViewerWindow", u"Show abs axis", None))
        self.checkBox_view_abs_axis.setText("")
        self.label_view_joint_axis.setText(QCoreApplication.translate("MotionViewerWindow", u"Show joint axis", None))
        self.checkBox_view_joint_axis.setText("")
        self.label_view_at.setText(QCoreApplication.translate("MotionViewerWindow", u"Show at", None))
        self.pushButton_view_at_x.setText(QCoreApplication.translate("MotionViewerWindow", u"X", None))
        self.pushButton_view_at_y.setText(QCoreApplication.translate("MotionViewerWindow", u"Y", None))
        self.pushButton_view_at_z.setText(QCoreApplication.translate("MotionViewerWindow", u"Z", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_view), QCoreApplication.translate("MotionViewerWindow", u"View", None))
        self.label_ik_enable.setText(QCoreApplication.translate("MotionViewerWindow", u"Enable IK", None))
        self.checkbox_ik_enable.setText("")
        self.label_ik_target_joint.setText(QCoreApplication.translate("MotionViewerWindow", u"Target Joint", None))
        self.label_ik_target_frame.setText(QCoreApplication.translate("MotionViewerWindow", u"Target Frame", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_ik), QCoreApplication.translate("MotionViewerWindow", u"IK", None))
    # retranslateUi

