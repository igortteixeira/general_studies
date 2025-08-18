from matplotlib import pyplot as plt
import numpy as np
import pandas as pd


people = np.array([10,22,2,43,12,30,25,6,70,76,54,89,60,73,74,60,54,80,88,90,65,62,])
age_median = np.median(people)
print(age_median)
bins = [0,10,20,40,60,90]

#What I want: 0-5-10-20-30-50-90 

plt.title('Covid death rate by age')
plt.ylabel("People")
plt.xlabel("Age")

plt.hist(people,bins=bins,edgecolor="#000000",log=True)
plt.axvline(age_median,color="#FFCE00",label="Age_median")

# Log=True is useful when there are big difference between certains hists. When this happen
#It's difficult to see those who have far less aperance than others

plt.legend()

#plt.grid(True)
plt.tight_layout()
plt.show()