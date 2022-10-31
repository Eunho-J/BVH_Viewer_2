
import sys
cupy_module_name = 'cupy'
if cupy_module_name in sys.modules:
    import cupy as np
else:
    import numpy as np
    
def numpy_get_unit(array: np.ndarray) -> np.ndarray:
    result: np.ndarray = array / np.linalg.norm(array)
    return result