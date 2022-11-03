from typing import Optional
from typing_extensions import override

from render import *
from obj import *

import OpenGL.GL as gl
import OpenGL.GLU as glu

import motion_formats.BVH_formats as bvh
from np import *


class BVH_GLRenderer(GLRenderer):
    def __init__(self) -> None:
        super().__init__()

        self.motion: Optional[BVHMotion]
        self.ik: Optional[BVH_IK] = BVH_IK(None)
        self.ik_frame_interval = 10

    def set_object(self, skeleton, motion):
        super().set_object(skeleton, motion)
        self.ik.ik_target_skeleton = skeleton

    def reset_desired_position(self):
        self.ik_desired_position = self.ik.target_joint_transform_matrix.T @ np.array([0,0,0,1], dtype=np.float32)
        self.ik.calculate_ik(self.motion.get_posture_at(self.ik_frame), self.ik_target_joint, self.ik_desired_position)

    def move_desired_position(self, translation: np.ndarray):
        if self.ik_desired_position is not None:
            # print("moved desire:", translation)
            self.ik_desired_position = self.ik_desired_position + translation
            self.ik.calculate_ik(self.motion.get_posture_at(self.ik_frame), self.ik_target_joint, self.ik_desired_position)

    @override
    def gl_render(self, frame: Optional[int]) -> None:
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT|gl.GL_DEPTH_BUFFER_BIT)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)
        self.gl_camera.lookAt()
        if self.render_abs_axis:
            GLRenderer.gl_render_axis(1)
        GLRenderer.gl_render_grid(30,30)
        if self.motion is not None:
            self.gl_render_bvh_recursive(frame, self.skeleton.root)
            if self.ik_enabled:
                tmp_Color = gl.glGetFloatv(gl.GL_CURRENT_COLOR)
                gl.glColor3ub(255,0,0)
                self.gl_render_ik_target_bvh(self.ik_frame, self.skeleton.root)
                # gl.glColor4f(tmp_Color[0], tmp_Color[1], tmp_Color[2], tmp_Color[3])

                if self.ik_desired_position is not None:
                    tmp_point_size = gl.glGetFloat(gl.GL_POINT_SIZE)
                    gl.glColor3ub(0, 0, 255)
                    gl.glPointSize(8)
                    gl.glPushMatrix()
                    gl.glBegin(gl.GL_POINTS)
                    gl.glVertex3f(self.ik_desired_position[0],self.ik_desired_position[1],self.ik_desired_position[2])
                    gl.glEnd()
                    gl.glPopMatrix()
                    gl.glPointSize(tmp_point_size)
                gl.glColor4f(tmp_Color[0], tmp_Color[1], tmp_Color[2], tmp_Color[3])



    def gl_render_ik_target_bvh(self, frame, joint):
        gl.glPushMatrix()
        
        if joint.symbol != bvh.Symbol.root:
            tmp_Color = gl.glGetFloatv(gl.GL_CURRENT_COLOR)
            if self.ik_target_joint is not None and joint.has_child_or_parent(self.ik_target_joint) and joint.parent_depth >= self.ik_target_joint.parent_depth - 1:
                gl.glColor3ub(0,255,0)
                
            gl.glBegin(gl.GL_LINES)
            gl.glVertex3f(joint.offsets[0], joint.offsets[1], joint.offsets[2])
            gl.glVertex3f(0,0,0)
            gl.glEnd()
            gl.glColor4f(tmp_Color[0], tmp_Color[1], tmp_Color[2], tmp_Color[3])

        gl.glTranslatef(joint.offsets[0], joint.offsets[1], joint.offsets[2])

        if frame is not None:
            posture = self.motion.get_posture_at(frame)

            for transformation, amount in posture.get_channels_and_amounts(joint.name):
                transformation.gl_apply(amount)


        if self.render_joint_axis:
            GLRenderer.gl_render_axis(1/10)

        for child in joint.children:
            
            if self.ik_enabled and self.ik_target_joint is not None\
                and child.has_child_or_parent(self.ik_target_joint) and frame is not None:
                    gl.glPushMatrix()
                    if self.ik_target_joint.parent.parent.name == joint.name:
                        self.ik.rotate_tau(1)
                        self.ik.rotate_alpha(1)
                    elif self.ik_target_joint.parent.name == joint.name:
                        self.ik.rotate_beta(1)

                    if self.ik_enabled and self.ik_target_joint.name == joint.name:
                        tmp_Color = gl.glGetFloatv(gl.GL_CURRENT_COLOR)
                        tmp_point_size = gl.glGetFloat(gl.GL_POINT_SIZE)
                        gl.glColor3ub(50, 200, 50)
                        gl.glPointSize(8)
                        gl.glBegin(gl.GL_POINTS)
                        gl.glVertex3f(0,0,0)
                        gl.glEnd()
                        gl.glPointSize(tmp_point_size)
                        gl.glColor4f(tmp_Color[0], tmp_Color[1], tmp_Color[2], tmp_Color[3])
                    self.gl_render_ik_target_bvh(frame, child)
                    gl.glPopMatrix()
            else:
                self.gl_render_ik_target_bvh(frame, child)

        gl.glPopMatrix()


    def gl_render_bvh_recursive(self, frame: Optional[int], joint: Joint):
        gl.glPushMatrix()
        
        if joint.symbol != bvh.Symbol.root:
            gl.glBegin(gl.GL_LINES)
            gl.glVertex3f(joint.offsets[0], joint.offsets[1], joint.offsets[2])
            gl.glVertex3f(0,0,0)
            gl.glEnd()


        gl.glTranslatef(joint.offsets[0], joint.offsets[1], joint.offsets[2])

        if frame is not None:
            posture = self.motion.get_posture_at(frame)

            for transformation, amount in posture.get_channels_and_amounts(joint.name):
                transformation.gl_apply(amount)

        if self.render_joint_axis:
            GLRenderer.gl_render_axis(1/10)

        for child in joint.children:
            if self.ik_enabled and self.ik_target_joint is not None\
                and child.has_child_or_parent(self.ik_target_joint) and frame is not None:
                    frame_diff = np.abs(frame - self.ik_frame)
                    gl.glPushMatrix()
                    if frame_diff <= self.ik_frame_interval:
                        if self.ik_target_joint.parent.parent.name == joint.name:
                            self.ik.rotate_tau(1 - frame_diff / self.ik_frame_interval)
                            self.ik.rotate_alpha(1 - frame_diff / self.ik_frame_interval)
                        elif self.ik_target_joint.parent.name == joint.name:
                            self.ik.rotate_beta(1 - frame_diff / self.ik_frame_interval)

                    if self.ik_enabled and self.ik_target_joint.name == joint.name:
                        tmp_Color = gl.glGetFloatv(gl.GL_CURRENT_COLOR)
                        tmp_point_size = gl.glGetFloat(gl.GL_POINT_SIZE)
                        gl.glColor3ub(50, 200, 50)
                        gl.glPointSize(8)
                        gl.glBegin(gl.GL_POINTS)
                        gl.glVertex3f(0,0,0)
                        gl.glEnd()
                        gl.glPointSize(tmp_point_size)
                        gl.glColor4f(tmp_Color[0], tmp_Color[1], tmp_Color[2], tmp_Color[3])
                    self.gl_render_bvh_recursive(frame, child)
                    gl.glPopMatrix()
            else:
                self.gl_render_bvh_recursive(frame, child)

        gl.glPopMatrix()


    def get_max_frame(self) -> int:
        return self.motion.get_max_frame()

    def get_frame_time(self) -> float:
        return self.motion.frame_interval

    def set_ik_target_frame(self, ik_target_frame):
        self.ik_frame = ik_target_frame
        if self.ik_target_joint is not None:
            self.ik.calculate_ik(self.motion.get_posture_at(self.ik_frame), self.ik_target_joint, self.ik_desired_position)
    
    def set_ik_target_joint(self, ik_target_joint):
        self.ik_target_joint = ik_target_joint
        self.ik_desired_position = None
        self.ik.calculate_ik(self.motion.get_posture_at(self.ik_frame), self.ik_target_joint, self.ik_desired_position)
        self.ik_desired_position = self.ik.target_joint_transform_matrix.T @ np.array([0,0,0,1], dtype=np.float32)