from typing import List, Optional
from typing_extensions import Self


class Joint:
    def __init__(self, name: Optional[str] = None, 
                 parent: Optional[Self] = None, 
                 symbol: Optional[str] = None) -> None:
        self.name = "anonymous" if name is None else name
        self.offsets = []
        self.children: List[Self] = []
        self.parent: Self = None
        self.symbol: str = symbol
        self.parent_depth: int = 0

        if parent is not None:
            self.set_parent(parent)

    def _add_child(self, child: Self) -> None:
        self.children.append(child)
        child.parent_depth = self.parent_depth + 1
    
    def set_parent(self, parent: Self) -> None:
        self.parent = parent
        parent._add_child(self)
    
    def number_of_children(self) -> int:
        return len(self.children)
    
    def get_joints_recursive(self) -> List[Self]:
        joint_list: List[Self] = []
        joint_list.append(self)
        for i in range(len(self.children)):
            joint_list.extend(self.children[i].get_joints_recursive())
        return joint_list

    def has_child_or_parent(self, target:Self) -> bool:
        if self.name == target.name:
            return True
        for child in self.children:
            if child.has_child_or_parent(target):
                return True
        parent = self.parent
        while parent is not None:
            if parent.name == target.name:
                return True
            parent = parent.parent
        return False

    def has_child(self, target:Self) -> bool:
        if self.name == target.name:
            return True
        for child in self.children:
            if child.has_child_or_parent(target):
                return True
        return False

    def has_parent(self, target:Self) -> bool:
        parent = self.parent
        while parent is not None:
            if parent.name == target.name:
                return True
            parent = parent.parent
        return False

        