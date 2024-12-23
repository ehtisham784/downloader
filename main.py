import numpy as np

# Without a seed
print(np.random.randint(1, 100, 5))  # Random output each time you run this script.

# With a seed
np.random.seed(2)
print(np.random.randint(1, 100, 5))  # Same output every time you use seed 42.
