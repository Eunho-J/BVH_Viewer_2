from typing import List, Optional

from obj import Joint

class Skeleton:
    def __init__(self, name: Optional[str] = None) -> None:
        self.name: Optional[str] = name
        self.root: Optional[Joint] = None

    def set_name(self, name: str) -> None:
        self.name = name

    def set_root(self, root: Optional[Joint] = None) -> None:
        self.root = root

    def get_joint_list(self) -> List[Joint]:
        if self.root is not None:
            return self.root.get_joints_recursive()
        else:
            empty_list: List[Joint] = []
            return empty_list

    
