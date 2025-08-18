from matplotlib import pyplot as plt
import numpy as np
import pandas as pd


time_interval = [1,2,3,4,5,6,7,8,9,10,11,12]
my_income = [1,4,8,10,9,5,2,0,1,4,6,7]
rival_income = [8,7,7,7,10,10,9,9,8,9,10,10]
x_indexes = np.arange(1,len(time_interval) + 1)
print(x_indexes)

plt.title('Companies Income')
plt.ylabel("Income")
plt.xlabel("Days")

plt.plot(time_interval,my_income,label="my_income",color='#FFB400',linestyle='-',marker='.',linewidth='2')
plt.plot(time_interval,rival_income,label="rival_income",color='#3346FF',linestyle='-',marker='.')
plt.fill_between(time_interval,my_income,rival_income,alpha=0.09)
plt.xticks(ticks=x_indexes,labels=time_interval)
plt.legend()

plt.grid(True)
plt.tight_layout()
plt.show()
