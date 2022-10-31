from typing import List
import pytest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from obj import Skeleton, Joint


@pytest.fixture
def root_joint():
    root = Joint("root")
    first = Joint("first", root)

    second = Joint("second", root)
    
    child_1 = Joint("child_1", first)
    child_2 = Joint("child_2", second)
    names = ['root', 'first', 'child_1', 'second', 'child_2']
    depths = [0, 1, 2, 1, 2]
    return root, names, depths

def test_skeleton_set_root(root_joint):
    skeleton = Skeleton("test skel")
    assert skeleton.root == None

    root, names, depths = root_joint
    skeleton.set_root(root)
    assert skeleton.root.name == 'root'

def test_skeleton_get_all_joints(root_joint):
    skeleton = Skeleton("test skel")
    root, names, depths = root_joint
    skeleton.set_root(root)

    list_all: List[Joint] = skeleton.get_joint_list()
    
    assert len(list_all) == 5
    for i in range(len(list_all)):
        assert list_all[i].name == names[i]
        assert list_all[i].parent_depth == depths[i]