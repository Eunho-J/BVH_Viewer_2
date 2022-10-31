import pytest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from obj import Joint


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


def test_joint_get_child_recursive(root_joint):
    list_all = []
    root, names, depths = root_joint
    list_all.extend(root.get_joints_recursive())

    assert len(list_all) == 5
    for i in range(len(list_all)):
        assert list_all[i].name == names[i]
        assert list_all[i].parent_depth == depths[i]


def test_joint_tree(root_joint):
    root, _, _ = root_joint
    assert len(root.children) == 2
    
    first = root.children[0]
    second = root.children[1]
    assert first.name == 'first'
    assert first.parent_depth == 1
    assert second.name == 'second'
    assert second.parent_depth == 1
    assert len(first.children) == 1
    assert len(second.children) == 1
    assert first.children[0].name == 'child_1'
    assert first.children[0].parent_depth == 2
    assert second.children[0].name == 'child_2'
    assert second.children[0].parent_depth == 2