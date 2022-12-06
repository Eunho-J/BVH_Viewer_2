from attrdict import AttrDict
import pytest

import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from np import *
from obj import Joint, Skeleton, BVHPosture
import motion_formats.BVH_formats as bvh
from customparser import BVHParser


@pytest.fixture
def parse_test_file():
    file = os.path.dirname(os.path.realpath(__file__)) + "/test_bvh_never_change"
    bvh_parser = BVHParser()

    parsed_skeleton, parsed_motion = bvh_parser.parse_file(file)

    true_joint_names = [
        "Hips",
        "Chest",
        "Neck",
        "Head",
        "Head_Site",
        "LeftCollar",
        "LeftUpArm",
        "LeftLowArm",
        "LeftHand",
        "LeftHand_Site",
        "RightCollar",
        "RightUpArm",
        "RightLowArm",
        "RightHand",
        "RightHand_Site",
        "LeftUpLeg",
        "LeftLowLeg",
        "LeftFoot",
        "LeftFoot_Site",
        "RightUpLeg",
        "RightLowLeg",
        "RightFoot",
        "RightFoot_Site"
    ]

    true_neck_joint_names = [
        "Neck",
        "Head",
        "Head_Site",
    ]

    true_channels = AttrDict({
        'root': ['xposition', 'yposition', 'zposition', 'zrotation', 'xrotation', 'yrotation'],
        'else': ['zrotation', 'xrotation', 'yrotation']
    })

    true_amount_at_first = [8.03, 35.01, 88.36, -3.41, 14.78, -164.35]

    return parsed_skeleton, parsed_motion, true_joint_names, true_neck_joint_names, true_channels, true_amount_at_first

def test_parsed_names(parse_test_file):
    parsed_skeleton, _, true_joint_names, _, _, _ = parse_test_file

    parsed_joint_name_list = [joint.name for joint in parsed_skeleton.get_joint_list()]
    for i in range(len(parsed_joint_name_list)):
        assert parsed_joint_name_list[i] == true_joint_names[i]

def test_parsed_tree_simple(parse_test_file):
    parsed_skeleton, _, _, true_neck_joint_names, _, _ = parse_test_file

    neck_joint = parsed_skeleton.root.children[0].children[0]
    neck_joint_names = [joint.name for joint in neck_joint.get_joints_recursive()]
    for i in range(len(true_neck_joint_names)):
        assert true_neck_joint_names[i] == neck_joint_names[i]

def test_parsed_motion_channel(parse_test_file):
    parsed_skeleton, parsed_motion, _, _, true_channels, _ = parse_test_file

    joint_list = parsed_skeleton.get_joint_list()
    parsed_channels_and_amounts = parsed_motion.postures[0].channels_and_transformation_amounts
    for joint in joint_list:
        is_root = False
        if joint.symbol == 'ROOT':
            is_root = True
        parsed_channel_list = [transformation.name for transformation, _ in parsed_channels_and_amounts.get(joint.name)]
        for i in range(len(parsed_channel_list)):
            assert parsed_channel_list[i] == true_channels['root' if is_root else 'else'][i]

def test_parsed_motion_amount_simple(parse_test_file):
    parsed_skeleton, parsed_motion, _, _, _, true_amount = parse_test_file

    root_joint_name = parsed_skeleton.root.name
    parsed_root_channels_and_amounts = parsed_motion.postures[0].channels_and_transformation_amounts.get(root_joint_name)
    for i in range(len(parsed_root_channels_and_amounts)):
        _, parsed_amount = parsed_root_channels_and_amounts[i]
        assert parsed_amount == true_amount[i]
    




