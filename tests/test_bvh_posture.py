from typing import Dict, List, Optional, Tuple
import pytest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from np import *
from obj import Joint, Skeleton, BVHPosture
import motion_formats.BVH_formats as bvh


@pytest.fixture
def posture():

    list_of_channels = [
        "xrotation",
        "yrotation",
        "zrotation",
        "xposition",
        "yposition",
        "zposition",
        "yrotation",
        "zposition",
        "xposition",
        "yposition"]
        
    channels_per_joint: Dict[str, List[bvh.Transformation]] = {}
    inputs_per_joint: Dict[str, float] = {}
    list_of_joint: List[Joint] = []

    for i in range(10):
        joint = Joint(str(i))
        list_of_joint.append(joint)
        channels_per_joint[joint.name] = [bvh.Channel[list_of_channels[i]]]

        input = 0.0
        if list_of_channels[i].endswith("rotation"):
            input = np.radians(90)
        else:
            input = float(i)
        inputs_per_joint[joint.name] = [input]

    posture = BVHPosture(channels_per_joint, inputs_per_joint)
    return posture, list_of_joint, list_of_channels

def test_posture_items(posture):
    pos: Optional[BVHPosture] = None
    pos, list_joint, list_channel = posture

    for idx, joint in enumerate(list_joint):
        list_of_tuples: List[Tuple[bvh.Transformation, float]] = pos.channels_and_transformation_amounts[joint.name]

        bvh_channel, input_float = list_of_tuples[0]

        x = np.array([1,1,1,1], dtype=np.float64)
        affine = bvh_channel.get_affine_matrix(input_float)
        if list_channel[idx] == 'xrotation':
            np.testing.assert_array_almost_equal(x@affine, np.array([1,-1,1,1],dtype=np.float64))
            assert bvh_channel.name == 'xrotation'
        if list_channel[idx] == 'yrotation':
            np.testing.assert_array_almost_equal(x@affine, np.array([1,1,-1,1],dtype=np.float64))
            assert bvh_channel.name == 'yrotation'
        if list_channel[idx] == 'zrotation':
            np.testing.assert_array_almost_equal(x@affine, np.array([-1,1,1,1],dtype=np.float64))
            assert bvh_channel.name == 'zrotation'
        if list_channel[idx] == 'xposition':
            np.testing.assert_array_almost_equal(x@affine, np.array([1+idx,1,1,1],dtype=np.float64))
            assert bvh_channel.name == 'xposition'
        if list_channel[idx] == 'yposition':
            np.testing.assert_array_almost_equal(x@affine, np.array([1,1+idx,1,1],dtype=np.float64))
            assert bvh_channel.name == 'yposition'
        if list_channel[idx] == 'zposition':
            np.testing.assert_array_almost_equal(x@affine, np.array([1,1,1+idx,1],dtype=np.float64))
            assert bvh_channel.name == 'zposition'
