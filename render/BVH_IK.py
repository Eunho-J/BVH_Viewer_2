from typing import Optional

import OpenGL.GL as gl
from motion_formats.Common_formats import Rotation

from np import *
import utils
from obj import *
import motion_formats.BVH_formats as bvh

class BVH_IK:
    def __init__(self, ik_target_skeleton:Skeleton) -> None:
        self.ik_target_skeleton = ik_target_skeleton

        self.target_joint_transform_matrix: Optional[np.ndarray] = None
        self.target_joint_parent_transform_matrix: Optional[np.ndarray] = None
        self.target_joint_grandparent_transform_matrix: Optional[np.ndarray] = None

        self.global_alpha_axis: Optional[np.ndarray] = None
        self.local_alpha_axis: Optional[np.ndarray] = None
        self.alpha_degree: float = 0.0

        self.global_beta_axis: Optional[np.ndarray] = None
        self.local_beta_axis: Optional[np.ndarray] = None
        self.beta_degree: float = 0.0

        self.global_tau_axis: Optional[np.ndarray] = None
        self.local_tau_axis: Optional[np.ndarray] = None
        self.tau_degree: float = 0.0


    def rotate_tau(self, scale):
        gl.glRotatef(self.tau_degree * scale, self.local_tau_axis[0], self.local_tau_axis[1], self.local_tau_axis[2])

    def rotate_alpha(self, scale):
        gl.glRotatef(self.alpha_degree * scale, self.local_alpha_axis[0], self.local_alpha_axis[1], self.local_alpha_axis[2])

    def rotate_beta(self, scale):
        gl.glRotatef(self.beta_degree* scale, self.local_beta_axis[0], self.local_beta_axis[1], self.local_beta_axis[2])
    
    def get_and_set_local_transformation_recursive(self, posture:BVHPosture, ik_target_joint:Joint, joint:Joint) -> None:

        gl.glPushMatrix()
        
        if joint.symbol == bvh.Symbol.root:
            gl.glLoadIdentity()

        gl.glTranslatef(joint.offsets[0], joint.offsets[1], joint.offsets[2])

        for transformation, amount in posture.get_channels_and_amounts(joint.name):
            transformation.gl_apply(amount)

        if ik_target_joint.parent.name == joint.name:
            self.local_beta_axis = np.reshape(np.array(gl.glGetFloatv(gl.GL_MODELVIEW_MATRIX)), (4,4)) @ self.global_beta_axis
        elif ik_target_joint.parent.parent.name == joint.name:
            self.local_tau_axis = self.target_joint_grandparent_transform_matrix @ self.global_tau_axis
            # gl.glRotatef(self.tau_degree, self.local_tau_axis[0], self.local_tau_axis[1], self.local_tau_axis[2])
            self.local_alpha_axis = np.reshape(np.array(gl.glGetFloatv(gl.GL_MODELVIEW_MATRIX)), (4,4)) @ self.global_alpha_axis
            gl.glRotatef(self.alpha_degree, self.local_alpha_axis[0], self.local_alpha_axis[1], self.local_alpha_axis[2])

        if ik_target_joint.name != joint.name:
            for child in joint.children:
                # if child.has_child_or_parent(ik_target_joint):
                self.get_and_set_local_transformation_recursive(posture, ik_target_joint, child)
                    # break

        gl.glPopMatrix()


    def get_and_set_transformation_matrix_recursive(self, posture:BVHPosture, ik_target_joint:Joint, joint:Joint) -> None:

        gl.glPushMatrix()
        
        if joint.symbol == bvh.Symbol.root:
            gl.glLoadIdentity()

        gl.glTranslatef(joint.offsets[0], joint.offsets[1], joint.offsets[2])

        for transformation, amount in posture.get_channels_and_amounts(joint.name):
            transformation.gl_apply(amount)

        if ik_target_joint.name == joint.name:
            self.target_joint_transform_matrix = np.reshape(np.array(gl.glGetFloatv(gl.GL_MODELVIEW_MATRIX)), (4,4))
        elif ik_target_joint.parent.name == joint.name:
            self.target_joint_parent_transform_matrix = np.reshape(np.array(gl.glGetFloatv(gl.GL_MODELVIEW_MATRIX)), (4,4))
        elif ik_target_joint.parent.parent.name == joint.name:
            self.target_joint_grandparent_transform_matrix = np.reshape(np.array(gl.glGetFloatv(gl.GL_MODELVIEW_MATRIX)), (4,4))
        
        if ik_target_joint.name != joint.name:
            for child in joint.children:
                if child.has_child_or_parent(ik_target_joint):
                    self.get_and_set_transformation_matrix_recursive(posture, ik_target_joint, child)
                    break

        gl.glPopMatrix()

    def calculate_ik(self, posture:BVHPosture, ik_target_joint:Joint, desired_position:Optional[np.ndarray]) -> None:
        self.get_and_set_transformation_matrix_recursive(posture, ik_target_joint, self.ik_target_skeleton.root)

        if desired_position is None:
            desired_position = self.target_joint_transform_matrix.T @ np.array([0,0,0,1], dtype=np.float32)
        
        global_pos_a: np.ndarray = self.target_joint_grandparent_transform_matrix.T @ np.array([0,0,0,1], dtype=np.float32)
        global_pos_b: np.ndarray = self.target_joint_parent_transform_matrix.T @ np.array([0,0,0,1], dtype=np.float32)
        global_pos_c: np.ndarray = self.target_joint_transform_matrix.T @ np.array([0,0,0,1], dtype=np.float32)
        
        # print(self.target_joint_grandparent_transform_matrix)
        # print("ga:", global_pos_a)

        eps = 0.0001
        len_ab = np.linalg.norm(global_pos_b - global_pos_a)
        len_bc = np.linalg.norm(global_pos_c - global_pos_b)
        len_ca = np.linalg.norm(global_pos_c - global_pos_a)
        len_at = np.clip(np.linalg.norm(desired_position - global_pos_a), len_ab - len_bc + eps, len_ab + len_bc - eps)


        #calc alpha
        alpha_degree_before = np.arccos(np.clip((len_ab*len_ab + len_ca*len_ca - len_bc*len_bc) / (2*len_ab*len_ca), -1+eps, 1-eps))
        alpha_degree_after = np.arccos(np.clip((len_ab*len_ab + len_at*len_at - len_bc*len_bc) / (2*len_ab*len_at),-1+eps,1-eps))

        self.alpha_degree = np.rad2deg(alpha_degree_after - alpha_degree_before)
        # print(np.clip((len_ab*len_ab + len_at*len_at - len_bc*len_bc) / (2*len_ab*len_at),-1,1))

        global_alpha_axis = np.zeros((4,), dtype=np.float32)
        global_alpha_axis[:3] = np.cross(global_pos_c[:3] - global_pos_a[:3], global_pos_b[:3] - global_pos_a[:3])
        self.global_alpha_axis = global_alpha_axis

        #calc beta
        beta_degree_before = np.arccos(np.clip((len_ab*len_ab + len_bc*len_bc - len_ca*len_ca) / (2*len_ab*len_bc), -1+eps, 1-eps))
        beta_degree_after = np.arccos(np.clip((len_ab*len_ab + len_bc*len_bc - len_at*len_at) / (2*len_ab*len_bc), -1+eps, 1-eps))

        self.beta_degree = np.rad2deg(beta_degree_after - beta_degree_before)

        # global_beta_axis = np.zeros((4,), dtype=np.float32)
        # global_beta_axis[:3] = np.cross(global_pos_c[:3] - global_pos_a[:3], global_pos_b[:3] - global_pos_a[:3])
        self.global_beta_axis = global_alpha_axis

        #calc tau
        self.tau_degree = np.rad2deg(np.arccos(np.clip(np.dot(utils.numpy_get_unit(global_pos_c - global_pos_a), utils.numpy_get_unit(desired_position - global_pos_a)), -1+eps, 1-eps)))
        global_tau_axis = np.zeros((4,), dtype=np.float32)
        global_tau_axis[:3] = np.cross(global_pos_c[:3] - global_pos_a[:3], desired_position[:3] - global_pos_a[:3])
        self.global_tau_axis = global_tau_axis

        self.get_and_set_local_transformation_recursive(posture, ik_target_joint, self.ik_target_skeleton.root)
