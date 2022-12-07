from attrdict import AttrDict

from np import *
from motion_formats.Common_formats import *

Channel = AttrDict({
    'xrotation': Rotation('xrotation', np.array([1,0,0], dtype=np.float64)),
    'yrotation': Rotation('yrotation', np.array([0,1,0], dtype=np.float64)),
    'zrotation': Rotation('zrotation', np.array([0,0,1], dtype=np.float64)),
    'xposition': Translation('xposition', np.array([1,0,0], dtype=np.float64)),
    'yposition': Translation('yposition', np.array([0,1,0], dtype=np.float64)),
    'zposition': Translation('zposition', np.array([0,0,1], dtype=np.float64))
})

Symbol = AttrDict({
    'root': "ROOT",
    'joint': "JOINT",
    'end': "End",
    'offset': "OFFSET",
    'channels': "CHANNELS",
})