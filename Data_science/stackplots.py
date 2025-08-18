from matplotlib import pyplot as plt
import numpy as np
import pandas as pd


days = [1,2,3,4,5,6,7,8,9]
steve = [20,15,17,19,13,10,9,20,18]
marx = [3,4,7,9,0,11,10,6,5]
names = ["Steve","Marx"]

plt.stackplot(days,steve,marx,labels=names)

plt.legend(loc='upper left')
plt.grid(True)
plt.title('Productivity of employess')
plt.tight_layout()
plt.show()