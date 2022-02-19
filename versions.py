# pylint: disable=import-error
"""short test of found versions in your env
to verify against requirements.txt"""

import platform

import chess
import docx
import numpy as np
import pandas as pd

print(f'#python=={platform.python_version()}')

print(f'numpy=={np.__version__}')
print(f'pandas=={pd.__version__}')
print(f'chess=={chess.__version__}')
print(f'docx=={docx.__version__}')
