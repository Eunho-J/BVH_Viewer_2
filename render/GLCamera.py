from OpenGL.GLU import *
from OpenGL.GL import *

from np import *

from utils import *

class GLCamera:
    def __init__(self) -> None:
        self.initial_cam = np.identity(4)
        self.initial_cam[:,-1] = 1
        self.initial_cam[-1,2] = 1
        self.viewport_height = 640
        self.viewport_width = 640
        
        self.current_cam = self.initial_cam
        
        self.xang = -np.radians(30)
        self.yang = np.radians(45)
        self._update_cam_rotation()
        
        self.zoom = 3.0
        self.is_ortho = False
        self.target = np.array([0., 0., 0.], dtype=np.float64)
        
    def lookAt(self):
        glViewport(0, 0, self.viewport_width, self.viewport_height)
        aspect = self.viewport_width / float(self.viewport_height)
        if not self.is_ortho:
            glLoadIdentity()
            gluPerspective(45, aspect, 1, 1000)
        
        if self.is_ortho:
            glLoadIdentity()
            zoom_tmp = np.max([0.01, self.zoom])
            if self.zoom < 0:
                zoom_tmp = np.min([-0.01, self.zoom])
            zoom_tmp *= np.tan(np.radians(22.5))  
            glOrtho(-zoom_tmp*aspect, zoom_tmp*aspect, -zoom_tmp, zoom_tmp, -50 * np.abs(zoom_tmp), 50 * np.abs(zoom_tmp))
            
        gluLookAt(self.zoom * self.current_cam[-1,0] + self.target[0], 
                  self.zoom * self.current_cam[-1,1] + self.target[1], 
                  self.zoom * self.current_cam[-1,2] + self.target[2],
                  self.target[0], 
                  self.target[1], 
                  self.target[2],
                  self.current_cam[1,0], 
                  self.current_cam[1,1], 
                  self.current_cam[1,2])
        
    def orbit(self, x, y, sensitivity):        
        self.xang += y * sensitivity
        self.yang += x * sensitivity
        self._update_cam_rotation()
        
    def panning(self, x, y, sensitivity):
        self.target = np.copy(self.target)
        self.target += self.current_cam[0,:3] * x * sensitivity * self.zoom + self.current_cam[1,:3] * -y * sensitivity * self.zoom
        
    def zoomming(self, zoom):
        self.zoom -= zoom
    
    def set_target(self, target):
        self.target = target

    def view_target_at(self, x, y, target=None):
        self.xang = x
        self.yang = y
        if target is not None:
            self.target = target
        self._update_cam_rotation()
        
    def _update_cam_rotation(self):
        M = np.identity(4)
        Rx = np.array([[1,0,0],
                    [0, np.cos(self.xang), -np.sin(self.xang)],
                    [0, np.sin(self.xang), np.cos(self.xang)]])
        Ry = np.array([[np.cos(self.yang), 0, np.sin(self.yang)],
                    [0,1,0],
                    [-np.sin(self.yang), 0, np.cos(self.yang)]])
        R = Ry @ Rx 
        M[:3,:3] = R
        self.current_cam = M @ self.initial_cam.T
        self.current_cam = self.current_cam.T
        
    def change_orth(self, is_ortho):
        self.is_ortho = is_ortho
        # print("ortho in cam:", self.is_ortho)