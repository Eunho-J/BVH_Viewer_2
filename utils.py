
import sys
cupy_module_name = 'cupy'
if cupy_module_name in sys.modules:
    import cupy as np
else:
    import numpy as np
    
def numpy_get_unit(array: np.ndarray) -> np.ndarray:
    result: np.ndarray = array / np.linalg.norm(array)
    return result

def distance_of(position1: np.ndarray, position2: np.ndarray) -> float:
    distance = np.linalg.norm(position2 - position1)
    return distance

def decompose_by(vector: np.ndarray, direction: np.ndarray) -> np.ndarray:
    unit: np.ndarray = numpy_get_unit(direction)
    decomposed: np.ndarray = np.dot(vector, direction) * unit
    return decomposed