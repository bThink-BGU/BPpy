import numpy as np
from gym import spaces

low = np.array([-100, -46, -26.66, -46, -26.66, 0])
high = np.array([100, 46, 26.66, 46, 26.66, 360])

observation_space = spaces.Box(low, high, dtype=np.float32)
