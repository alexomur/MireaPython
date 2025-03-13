import numpy as np
import matplotlib.pyplot as plt

mat = np.random.choice(2, 5*3).reshape(5, 3)
print("5x3:")
print(mat)
sym_part = np.fliplr(mat[:, :2])
print("Symm:")
print(sym_part)

extended_mat = np.concatenate((mat, sym_part), axis=1)
print("5x5:")
print(extended_mat)

plt.imshow(extended_mat, cmap='gray')
plt.show()
