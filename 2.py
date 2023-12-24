import csv
import os
import numpy as np
import matplotlib.pyplot as plt
import scipy.special as sci
import requests as r

if not os.path.exists("result"):
    os.mkdir("result")

url = 'https://jenyay.net/uploads/Student/Modelling/task_02.csv'

try:
    res = r.get(url)

    with open("task_02.csv", "wb") as file:
        file.write(res.content)
except Exception as _ex:
    print('Someting went wrong')

data = []

with open("task_02.csv", "r") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[0] == '19':
            data = list(map(float, row))[1:4]

D = data[0]
fmin = data[1]
fmax = data[2]
c = 3*10**8

count = 200
step = 25
flist = np.linspace(fmin, fmax, count)

k = []
for i in range(count):
    k.append(2 * np.pi * flist[i]/c)

def JOrd(order, countt):
    jblist = (sci.spherical_jn(order, k[countt] * D / 2))
    return jblist

def HOrd(order, countt):
    yblist = (sci.spherical_yn(order, k[countt] * D / 2))
    hblist = (complex(JOrd(order, countt), yblist))
    return hblist

def AOrd(order, countt):
    anlist = (JOrd(order, countt) / HOrd(order, countt))
    return anlist

def BOrd(order, countt):
    bnlist = (((k[countt] * (D / 2) * JOrd(order - 1, countt) - order * JOrd(order, countt)) / (k[countt] * (D / 2) * HOrd(order - 1, countt) - order * HOrd(order, countt))))
    return bnlist

j = 1
func = [0]*count
while j <= step:
    for i in range(count):
        func[i] += ((-1)**j * (j+0.5) * (BOrd(j, i) - AOrd(j, i)))
    j += 1

epr = []
lam = []
for i in range(count):
    epr.append((c ** 2 / (np.pi * flist[i] ** 2)) * (abs(func[i]) ** 2))
    lam.append(c/flist[i])

plt.plot(flist, epr)
plt.ylabel("ЭПР, $м^2$")
plt.xlabel("Частота, ГГц")
plt.show()

import json

resultData = []

for i in range(count):
    resultData.append({"freq": flist[i],
                       "lambda": lam[i],
                       "rsc": epr[i]
                       })

with open("result/data2.json", "w") as file:
    json.dump({"data": resultData}, file)
