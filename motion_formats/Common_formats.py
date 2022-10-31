from abc import abstractmethod
from typing import Optional
from typing_extensions import override

import OpenGL.GL as gl

from np import *

import utils

class Transformation:
    def __init__(self, name: str, axis: np.ndarray) -> None:
        assert np.linalg.norm(axis) >= 0.0001
        assert axis.shape == (3,) or axis.shape == (4,)
        if axis.shape == (4,):
            assert axis[-1] == 0
            
        self.name: str = name
        self.unit_axis: np.ndarray = utils.numpy_get_unit(axis[:3])
    
    @abstractmethod
    def get_affine_matrix(self, amount: Optional[float]) -> np.ndarray:
        pass
    
    @abstractmethod
    def gl_apply(self, amount: Optional[float]) -> None:
        pass

     

class Rotation(Transformation):
    def __init__(self, name: str, axis: np.ndarray) -> None:
        super().__init__(name, axis)
    
    @override
    def get_affine_matrix(self, amount: Optional[float]) -> np.ndarray:
        x = self.unit_axis[0] * np.sin(amount / 2)
        y = self.unit_axis[1] * np.sin(amount / 2)
        z = self.unit_axis[2] * np.sin(amount / 2)
        s = np.cos(amount / 2)

        M = np.identity(4)
        M[:3,:3] = np.array([[1 - 2*y*y - 2*z*z,    2*x*y + 2*s*z,      2*x*z - 2*s*y],
                             [2*x*y - 2*s*z,        1 - 2*x*x -2*z*z,   2*y*z + 2*s*x],
                             [2*x*z + 2*s*y,        2*y*z - 2*s*x,      1 - 2*x*x - 2*y*y]])
        return M
    
    @override
    def gl_apply(self, amount: Optional[float]) -> None:
        gl.glRotatef(amount, self.unit_axis[0], self.unit_axis[1], self.unit_axis[2])

    
class Translation(Transformation):
    def __init__(self, name: str, axis: np.ndarray) -> None:
        super().__init__(name, axis)
    
    @override
    def get_affine_matrix(self, amount: Optional[float]) -> np.ndarray:
        M = np.identity(4)
        M[-1,:3] = self.unit_axis * amount
        return M
    
    @override
    def gl_apply(self, amount: Optional[float]) -> None:
        translation: np.ndarray = self.unit_axis * amount
        gl.glTranslatef(translation[0], translation[1], translation[2])

