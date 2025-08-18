from matplotlib import pyplot as plt
import numpy as np
import pandas as pd


time_interval = [1,2,3,4,5,6,7,8,9,10,11,12]
my_income = [1,4,8,10,9,5,2,0,1,4,6,7]
rival_income = [8,7,7,7,10,10,9,9,8,9,10,10]
google_income = [20,20,15,17,18,19,20,16,17,19,15,20]
x_indexes = np.arange(1,len(time_interval) + 1)


fig,(ax1,ax2) = plt.subplots(nrows=2,ncols=1,sharex=True)
fig1,ax3 = plt.subplots()

#By default, subplots are nrows=1,ncols = 1

ax1.plot(time_interval,my_income,label="my_income",linestyle='-')
ax2.plot(time_interval,rival_income,label="rival_income",linestyle='-',color='#F00000')
ax3.plot(time_interval,my_income,label="google_income",linestyle='-',color='#F3FF33')

plt.xticks(ticks=x_indexes,labels=time_interval)

ax1.set_title('Companies Income')
ax1.set_ylabel("Income")
ax2.set_ylabel("Income")
ax3.set_ylabel("Income")
ax1.set_xlabel("Time")

ax1.legend()
ax2.legend()
ax3.legend()
ax1.grid(True)
ax2.grid(True)
ax3.grid(True)

plt.tight_layout()
plt.show()

#fig.savefig("test.png")
#fig1.savefig("test1.png")