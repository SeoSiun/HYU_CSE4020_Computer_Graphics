import numpy as np

np.set_printoptions(linewidth=np.inf)
M = np.arange(2,27)
print(M,"\n")

M = M.reshape(5,5)
print(M,"\n")

for i in range(1,4):
    for j in range(1,4):
        M[i,j]=0
print(M,"\n")

M=M@M
print(M,"\n")
        
v=M[0]
print(np.sqrt(v@v))
