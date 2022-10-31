from typing import Optional
from typing_extensions import override
from render import *
from obj import *

import OpenGL.GL as gl
import OpenGL.GLU as glu

import motion_formats.BVH_formats as bvh

class BVH_GLRenderObject(GLRenderObject):
    def __init__(self, bvh_motion:BVHMotion, skeleton: Optional[Skeleton] = None) -> None:
        super().__init__(skeleton)
        self.bvh_motion: BVHMotion = bvh_motion

    @override 
    def gl_render_object(self, frame:Optional[int], render_axis:bool = False) -> None:
        if frame is not None:
            frame = frame % self.bvh_motion.get_max_frame()
            posture: BVHPosture = self.bvh_motion.get_posture_at(frame)
            BVH_GLRenderObject.gl_render_frame_recursive(self.skeleton.root, posture, render_axis)
        else:
            posture: BVHPosture = self.bvh_motion.get_posture_at(0)
            BVH_GLRenderObject.gl_render_model_recursive(self.skeleton.root, posture, render_axis)

    @override
    def get_frame_time(self) -> float:
        return self.bvh_motion.frame_interval

    @override
    def get_max_frame(self) -> int:
        return self.bvh_motion.max_frame

    @staticmethod
    def gl_render_model_recursive(joint: Joint, posture: BVHPosture, render_axis:bool = False):
        gl.glPushMatrix()
        
        if joint.symbol != bvh.Symbol.root:
            gl.glBegin(gl.GL_LINES)
            gl.glVertex3f(joint.offsets[0], joint.offsets[1], joint.offsets[2])
            gl.glVertex3f(0,0,0)
            gl.glEnd()

        gl.glTranslatef(joint.offsets[0], joint.offsets[1], joint.offsets[2])


        if render_axis:
            GLRenderer.gl_render_axis(1/3)

        for child in joint.children:
            BVH_GLRenderObject.gl_render_model_recursive(child, posture, render_axis)

        gl.glPopMatrix()

    @staticmethod
    def gl_render_frame_recursive(joint: Joint, posture: BVHPosture, render_axis:bool = False):
        gl.glPushMatrix()
        
        if joint.symbol != bvh.Symbol.root:
            gl.glBegin(gl.GL_LINES)
            gl.glVertex3f(joint.offsets[0], joint.offsets[1], joint.offsets[2])
            gl.glVertex3f(0,0,0)
            gl.glEnd()

        
        gl.glTranslatef(joint.offsets[0], joint.offsets[1], joint.offsets[2])


        for transformation, amount in posture.get_channels_and_amounts(joint.name):
            transformation.gl_apply(amount)

        if render_axis:
            GLRenderer.gl_render_axis(1/3)


        for child in joint.children:
            BVH_GLRenderObject.gl_render_frame_recursive(child, posture, render_axis)

        gl.glPopMatrix()

        