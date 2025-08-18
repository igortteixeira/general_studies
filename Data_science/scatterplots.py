from matplotlib import pyplot as plt
import numpy as np
import pandas as pd


dataset = pd.read_csv(".\\Datasets\\diabetes2.csv")
df = dataset

glucose = df["Glucose"]
blood_pressure = df["BloodPressure"]
age = df["Age"]

plt.scatter(glucose, blood_pressure, c=age, cmap='summer',edgecolor='black', linewidth=1, alpha=0.75)

cbar = plt.colorbar()
cbar.set_label('')

#plt.xscale('log')
#plt.yscale('log')

plt.title('Age-bloodpressure-glucose Relation')
plt.xlabel('BloodPressure')
plt.ylabel('Glucose')

# Log=True is useful when there are big difference between certains hists. When this happen
#It's difficult to see those who have far less aperance than others

plt.legend()

#plt.grid(True)
plt.tight_layout()
plt.show()