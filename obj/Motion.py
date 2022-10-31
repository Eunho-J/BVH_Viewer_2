from typing import Dict, List, Optional
import motion_formats.BVH_formats as bvh

from np import *
from obj import BVHPosture

class BVHMotion:
    def __init__(self, name:str, channels_per_joint: Dict[str, List[bvh.Transformation]]) -> None:
        self.name: str = name
        self.max_frame = 0
        self.frame_interval: float = 0.0
        self.postures: List[BVHPosture] = []
        self.channels_per_joint: Dict[str, List[bvh.Transformation]] = channels_per_joint
        
    def get_max_frame(self) -> int:
        return len(self.postures)
    
    def get_posture_at(self, frame:int) -> BVHPosture:
        return self.postures[frame]

    def append_posture(self, posture:BVHPosture) -> None:
        self.postures.append(posture)

    def extend_postures(self, postures: List[BVHPosture]) -> None:
        self.postures.extend(postures)

