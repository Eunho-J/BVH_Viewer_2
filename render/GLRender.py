from abc import abstractmethod
from typing import List, Optional
from xmlrpc.client import boolean
import OpenGL.GL as gl
from np import *

from obj import *
from render import *

class GLRenderObject(RenderObject):
    def __init__(self, skeleton: Optional[Skeleton] = None) -> None:
        super().__init__(skeleton)
        
    @abstractmethod
    def gl_render_object(self, frame:int, render_axis:bool) -> None:
        pass

    @abstractmethod
    def get_frame_time(self) -> float:
        pass

    @abstractmethod
    def get_max_frame(self) -> int:
        pass


class GLRenderer:
    def __init__(self) -> None:
        self.objects: List[GLRenderObject] = []
        self.gl_camera: GLCamera = GLCamera()
        
        self.render_abs_axis = True
        self.render_joint_axis = False

    def append_object(self, object:GLRenderObject) -> int:
        self.objects.append(object)
        return len(self.objects)

    def clear_and_append_object(self, object:GLRenderObject) -> int:
        self.objects.clear()
        self.objects.append(object)
        return len(self.objects)
    
    def gl_render_objects(self, frame:Optional[int]) -> None:
        for object in self.objects:
            object.gl_render_object(frame, self.render_joint_axis)
    
    @staticmethod
    def gl_render_axis(scale:float) -> None:
        gl.glPushMatrix()
        gl.glLineWidth(3*scale)
        gl.glBegin(gl.GL_LINES)
        gl.glColor3ub(255,0,0)
        gl.glVertex3fv(np.array([0.,0.,0.]))
        gl.glVertex3fv(np.array([scale,0.,0.]))
        gl.glColor3ub(0,255,0)
        gl.glVertex3fv(np.array([0.,0.,0.]))
        gl.glVertex3fv(np.array([0.,scale,0.]))
        gl.glColor3ub(0,0,255)
        gl.glVertex3fv(np.array([0.,0.,0.]))
        gl.glVertex3fv(np.array([0.,0.,scale]))
        gl.glEnd()
        gl.glLineWidth(1)
        gl.glColor3ub(255,255,255)
        gl.glPopMatrix()

    @staticmethod
    def gl_render_grid(row, col) -> None:
        gl.glBegin(gl.GL_LINES)   
        gl.glColor3ub(255,255,255)
        for i in range(row + 1):
            gl.glVertex3f(i - row / 2, 0, -col/2)
            gl.glVertex3f(i - row / 2, 0, col/2)
        for i in range(col + 1):
            gl.glVertex3f(-row/2, 0, i - col / 2)
            gl.glVertex3f(row/2, 0, i - col / 2)
        gl.glEnd()

    def gl_render(self, frame:int) -> None:
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT|gl.GL_DEPTH_BUFFER_BIT)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)
        self.gl_camera.lookAt()
        if self.render_abs_axis:
            GLRenderer.gl_render_axis(1)
        GLRenderer.gl_render_grid(30,30)
        self.gl_render_objects(frame)

    def set_viewport_size(self, w:int, h:int) -> None:
        self.gl_camera.viewport_width, self.gl_camera.viewport_height = w, h

    def set_view_ortho(self, is_ortho: boolean) -> None:
        self.gl_camera.change_orth(is_ortho)

    def show_abs_axis(self, show: bool) -> None:
        self.render_abs_axis = show

    def show_joint_axis(self, show:bool) -> None:
        self.render_joint_axis = show

    def get_min_frame_time(self) -> float:
        min_frame_time:float = 100.0
        for object in self.objects:
            if object.get_frame_time() < min_frame_time:
                min_frame_time = object.get_frame_time()
        return min_frame_time

    def get_max_frame(self) -> int:
        max_frame = 0
        for object in self.objects:
            frame = object.get_max_frame()
            if frame > max_frame:
                max_frame = frame

        return max_frame