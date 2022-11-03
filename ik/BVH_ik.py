from typing import Optional, Tuple, List

from np import *
from obj import *
import utils
import motion_formats.BVH_formats as bvh

class BVH_ik:
    def __init__(self) -> None:
        self.target_posture: Optional[BVHPosture] = None
        self.target_joint: Optional[Joint] = None
        self.target_point: Optional[np.ndarray] = None

    def get_positions(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        #returns a, b, c, t global positions
        position = np.array([0, 0, 0, 1], dtype=np.float32)
        current_joint = self.target_joint
        
        transformation_stack: List[Tuple[bvh.Transformation, float]] = []
        
        while current_joint is not None:
            pass

