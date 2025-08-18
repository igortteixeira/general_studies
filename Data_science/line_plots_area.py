from matplotlib import pyplot as plt
import numpy as np
import pandas as pd


time_interval = np.array([1,2,3,4,5,6,7,8,9,10,11,12])
my_income = np.array([1,4,8,10,9,5,2,0,1,4,6,7])
x_indexes = np.arange(1,len(time_interval) + 1)

low_income_limit = 4
high_income = 8

plt.title('Companies Income')
plt.ylabel("Income")
plt.xlabel("Days")

plt.plot(time_interval,my_income,label="my_income",linestyle='-')

plt.fill_between(time_interval,my_income,low_income_limit,
where=(my_income < low_income_limit),
label="Very low income",interpolate=True,color='#FF0000')

plt.fill_between(time_interval,my_income,low_income_limit,
where=(my_income > low_income_limit),
label="Good Income",interpolate=True,color='#FFD100')


plt.fill_between(
time_interval,my_income,high_income,
where=(my_income > high_income),label="High Income",interpolate=True,color='#0CFF00')


print(x_indexes)
plt.xticks(ticks=x_indexes,labels=time_interval)
plt.legend()

plt.grid(True)
plt.tight_layout()
plt.show()
