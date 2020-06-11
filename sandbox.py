import numpy as np

#print(np.__version__)

#l = np.zeros(10, dtype=np.int16)

np.random.seed(0)
x1 = np.random.randint(10, size=6)  # One-dimensional array
x2 = np.random.randint(10, size=(3, 4))  # Two-dimensional array
x3 = np.random.randint(10, size=(3, 4, 5))  # Three-dimensional array




#print(x1)
print(x2[0,2])
print("\n")
print(x2[:2, :3])  #:2 -> two rows; :3 -> three columns
print("\n")
print(x2[:3, ::2])  # all rows, every other column
#print(x3)
