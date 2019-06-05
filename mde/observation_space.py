import numpy as np
from gym import spaces

low = np.array([-100, -48.25, -28.75, -48.25, -28.75, 0])
high = np.array([100, 48.25, 28.75, 48.25, 28.75, 360])

observation_space = spaces.Box(low, high, dtype=np.float32)
