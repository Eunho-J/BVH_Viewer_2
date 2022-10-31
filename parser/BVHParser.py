from curses.ascii import isalpha
import re
import os
from typing import Dict, List, Optional, Tuple
from typing_extensions import override

from parser import Parser
from obj import Joint, Skeleton, BVHPosture, BVHMotion
import motion_formats.BVH_formats as bvh_formats

class BVHParser(Parser):
    def __init__(self):
        super().__init__()
        self.parsed_bvh_motion: Optional[BVHMotion] = None
        self.parsed_channels_per_joint: Optional[Dict[str, List[bvh_formats.Transformation]]] = None

    
    @staticmethod
    def parse_hierarchy(content:str, name:str) -> Tuple[Skeleton, 
                                                        Dict[str, List[bvh_formats.Transformation]]]:

        root: Optional[Joint] = None
        channels_per_joint: Dict[str, List[bvh_formats.Transformation]] = {}

        lines = re.split('\\s*\\n+\\s*', content)

        current_joint: Optional[Joint] = None

        for line in lines:
            words = re.split('\\s+', line)
            symbol = words[0]

            if symbol == "}":
                if channels_per_joint.get(current_joint.name) is None:
                    channels_per_joint[current_joint.name] = []
                current_joint = current_joint.parent
                continue

            if not symbol.isalpha():
                continue
            
            symbol = bvh_formats.Symbol.get(symbol.lower())
            if symbol is None:
                continue
            
            if symbol == bvh_formats.Symbol.root:
                assert current_joint is None

                joint_name = words[1]
                current_joint = Joint(joint_name, current_joint, symbol)
                print("|", current_joint.parent_depth * "  |", "-", joint_name, sep='')

                root = current_joint

            elif symbol == bvh_formats.Symbol.joint:
                joint_name = words[1]
                current_joint = Joint(joint_name, current_joint, symbol)
                print("|", current_joint.parent_depth * "  |", "-", joint_name, sep='')

            elif symbol == bvh_formats.Symbol.end:
                joint_name = current_joint.name + "_" + words[1]
                current_joint = Joint(joint_name, current_joint, symbol)
                print("|", current_joint.parent_depth * "  |", "-", joint_name, sep='')

            elif symbol == bvh_formats.Symbol.offset:
                current_joint.offsets.extend(map(float, words[1:]))

            elif symbol == bvh_formats.Symbol.channels:
                channels: List[bvh_formats.Transformation] = []
                num_channel = int(words[1])

                channels.extend([bvh_formats.Channel[channel.lower()] for channel in words[2:2+num_channel]])
                
                channels_per_joint[current_joint.name] = channels
        
        skeleton = Skeleton(name)
        skeleton.set_root(root)
        return skeleton, channels_per_joint


    @staticmethod
    def parse_bvh_motion(content:str, 
                         name:str, 
                         skeleton: Skeleton, 
                         channels_per_joint: Dict[str, List[bvh_formats.Transformation]]
                         ) -> BVHMotion:
        
        bvh_motion = BVHMotion(name, channels_per_joint)
        joint_list: List[Joint] = skeleton.get_joint_list()
        lines = re.split('\\s*\\n+\\s*', content)


        for line in lines:
            if line == '':
                continue
            
            words = re.split('\\s+', line)

            if line.lower().startswith("frame time:"):
                bvh_motion.frame_interval = float(words[2])
                print("frame time:", bvh_motion.frame_interval)
            elif line.lower().startswith("frames:"):
                bvh_motion.max_frame = int(words[1])
                print("frames:", bvh_motion.max_frame)
            else:
                words.reverse() #to use as queue
                inputs_per_joint: Dict[str, List[float]] = {}
                for joint in joint_list:
                    inputs_per_joint[joint.name] = [float(words.pop()) for i in range(len(channels_per_joint[joint.name]))]
                bvh_motion.append_posture(BVHPosture(channels_per_joint, inputs_per_joint))
        
        return bvh_motion

    @override
    def parse_file(self, filepath: str) -> Tuple[Skeleton, BVHMotion]:
        
        self.parsed_file = filepath
        self.changed = False

        file = open(filepath, 'r')
        file_content = file.read()
        file.close()

        name, _ = os.path.splitext(re.split('\\/+', file_content)[-1])

        hierarchy_content, motion_content = file_content.split("MOTION")

        self.parsed_skeleton, self.parsed_channels_per_joint = self.parse_hierarchy(hierarchy_content, name)
        
        self.parsed_bvh_motion = self.parse_bvh_motion(motion_content, 
                                                       name, 
                                                       self.parsed_skeleton,  
                                                       self.parsed_channels_per_joint)
        return self.parsed_skeleton, self.parsed_bvh_motion

    @override
    def save_as(self, filepath: str) -> None:
        pass