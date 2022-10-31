from typing import Dict, List, Tuple

import motion_formats.BVH_formats as bvh

class BVHPosture:
    def __init__(self, 
                 channels_per_joint: Dict[str, List[bvh.Transformation]], 
                 inputs_per_joint: Dict[str, List[float]]
                ) -> None:

        self.channels_and_transformation_amounts: Dict[str, List[Tuple[bvh.Transformation, float]]] = {}

        for joint_name, list_of_channel in channels_per_joint.items():
            list_of_tuples: List[Tuple[bvh.Transformation, float]] = []

            list_of_inputs: List[float] = inputs_per_joint[joint_name]

            for idx, bvh_channel in enumerate(list_of_channel):
                list_of_tuples.append((bvh_channel, list_of_inputs[idx]))

            self.channels_and_transformation_amounts[joint_name] = list_of_tuples

    def get_channels_and_amounts(self, joint_name:str) -> List[Tuple[bvh.Transformation, float]]:
        return self.channels_and_transformation_amounts[joint_name]

# BVHPosture has dictionary of channel_and_transformation_amount with name of joint as key.
# key is name of joint to make Posture can adopted to other skeletons that has same joint-name bindings.