import os
import sys
from pathlib import Path
import numpy as np
import pandas as pd

import pytest

@pytest.fixture
def edgelist1():
    return [[1,2,3],[4],[5,6],[6,7,8]]

@pytest.fixture
def edgelist2():
    return [[1,2],[3,4],[4,5,6]]

@pytest.fixture
def edgelist3():
    return [[1,2,3],[3,4],[4,5,6]]

@pytest.fixture
def edgelist4():
    return [[1,2,3],[2,3,4,5],[3,4,5]]

@pytest.fixture
def edgelist5():
    return [[0,1,2,3],[4],[5,6],[6,7,8]]

@pytest.fixture
def dict5():
    return {0 : [0,1,2,3], 1 : [4], 2 : [5,6], 3 : [6,7,8]}

@pytest.fixture
def incidence5():
    I = np.zeros((9, 4))
    I[0, 0] = I[1, 0] = I[2, 0] = I[3, 0] = I[4, 1] = I[5, 2] = I[6, 2] \
    = I[6, 3] = I[7, 3] = I[8, 3] = 1
    return I

@pytest.fixture
def dataframe5():
    data = [[0, 0], [1, 0], [2, 0], [3, 0], [4, 1], [5, 2], [6, 2], [6, 3], [7, 3], [8, 3]]
    return pd.DataFrame(data)