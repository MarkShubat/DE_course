import numpy as np
import os

VAR = 16

matrix = np.load('matrix_16_2.npy')
x, y = np.where(matrix > 500 + VAR)
z = matrix[matrix > 500 + VAR]
np.savez('t2_result.npz', x=x, y=y, z=z)
np.savez_compressed('t2_result_compressed.npz', x=x, y=y, z=z)

print("Размер оригинального файла: " + str(os.path.getsize('t2_result.npz')))
print("Размер сжатого файла: " + str(os.path.getsize('t2_result_compressed.npz')))
