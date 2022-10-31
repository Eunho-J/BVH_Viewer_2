from typing import Optional

from obj import Skeleton


class RenderObject:
    def __init__(self, skeleton: Optional[Skeleton] = None) -> None:
        self.skeleton = skeleton
        
class Renderer:
    def __init__(self) -> None:
        pass