import numpy as np
import matplotlib.pyplot as plt
import os

A = 10
x = np.arange(1,10,0.1)
print(len(x))

def f(x):
    sum = 0
    for i in range(1,11):
        ti = 0.1*i
        yi = np.exp(-ti) - 5*np.exp(10*ti)
        sum += (np.exp(-ti*x) - 5*np.exp(-ti*A) - yi)**2
    return sum

y = f(x)
plt.plot(x,y)
plt.show()

if not os.path.exists("result"):
    os.mkdir("result")


file = open('result/res.txt', 'w')
for i in range(0, len(x)):
    file.write(str(x[i]) + "    " + str(y[i]) + '\n')
file.close()